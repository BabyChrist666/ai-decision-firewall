"""
Interceptor: Main orchestration layer that coordinates all firewall checks.
"""
from typing import List, Optional
from ..models import (
    FirewallRequest,
    FirewallResponse,
    Claim,
    CheckResult,
    Verdict
)
from ..firewall.claim_parser import ClaimParser
from ..firewall.confidence import ConfidenceChecker
from ..firewall.evidence import EvidenceChecker
from ..firewall.rules import RulesEngine
from ..firewall.risk import RiskScorer
from ..firewall.verdict import VerdictEngine
from ..audit.logger import AuditLogger
from ..metrics.counters import MetricsCounter
from ..learning.memory import LearningMemory
from ..compliance.policy import get_policy_manager
from ..config import ENTERPRISE_MODE
from ..utils.logger import logger


class FirewallInterceptor:
    """Main interceptor that orchestrates all firewall checks."""
    
    def __init__(self):
        """Initialize the firewall interceptor."""
        self.claim_parser = ClaimParser()
        self.confidence_checker = ConfidenceChecker()
        self.evidence_checker = EvidenceChecker()
        self.rules_engine = RulesEngine()
        self.risk_scorer = RiskScorer()
        self.verdict_engine = VerdictEngine()
        
        # Enterprise features
        self.audit_logger = AuditLogger() if ENTERPRISE_MODE else None
        self.metrics = MetricsCounter()
        self.memory = LearningMemory()
    
    def check(self, request: FirewallRequest) -> FirewallResponse:
        """
        Main entry point for firewall check.
        
        Args:
            request: Firewall request with AI output and metadata
            
        Returns:
            Firewall response with verdict and details
        """
        logger.info(
            f"Firewall check initiated: action={request.intended_action}, "
            f"confidence={request.confidence:.2f}"
        )
        
        # Step 1: Parse claims
        claims = self.claim_parser.parse(
            request.ai_output,
            request.confidence
        )
        
        # Step 2: Check confidence alignment
        confidence_aligned, confidence_reason = self.confidence_checker.validate_confidence_alignment(
            request.confidence,
            claims
        )
        confidence_check = CheckResult(
            check_name="confidence_alignment",
            passed=confidence_aligned,
            reason=confidence_reason
        )
        
        # Step 3: Check evidence
        evidence_passed, evidence_reason, failed_evidence_claims = self.evidence_checker.check_evidence(
            claims,
            request.sources
        )
        evidence_check = CheckResult(
            check_name="evidence",
            passed=evidence_passed,
            reason=evidence_reason
        )
        
        # Step 4: Check rules
        rules_passed, rules_reason, failed_rules = self.rules_engine.check_rules(
            claims,
            request.ai_output,
            request.intended_action
        )
        rules_check = CheckResult(
            check_name="rules",
            passed=rules_passed,
            reason=rules_reason
        )
        
        # Step 5: Calculate risk score
        risk_score = self.risk_scorer.calculate_risk_score(
            request.confidence,
            request.intended_action,
            claims,
            has_evidence=evidence_passed
        )
        
        # Step 6: Check governance rules FIRST (before high-impact policy)
        # Governance rules ALWAYS override risk scoring, confidence, and evidence
        policy_manager = get_policy_manager()
        governance_requires_review, governance_reason = policy_manager.requires_mandatory_review(
            request.intended_action
        )
        
        # Step 7: Check high-impact action policy (secondary to governance)
        requires_human_review, review_reason = self.rules_engine.requires_human_review_for_high_impact(
            intended_action=request.intended_action,
            confidence=request.confidence,
            has_evidence=evidence_passed
        )
        
        # Step 8: Determine verdict
        failed_checks = []
        if not evidence_passed:
            failed_checks.append("evidence")
        if not rules_passed:
            failed_checks.append("rules")
        # Evidence Override Rule: confidence_alignment only blocks if evidence is missing
        if not confidence_aligned and not evidence_passed:
            failed_checks.append("confidence_alignment")
        if requires_human_review:
            failed_checks.append("high_impact_review_required")
        if governance_requires_review:
            failed_checks.append("governance_mandatory_review")
        
        verdict, verdict_reason, explanation, applied_policies, escalation_reason = self.verdict_engine.determine_verdict(
            risk_score=risk_score,
            evidence_passed=evidence_passed,
            rules_passed=rules_passed,
            confidence_aligned=confidence_aligned,
            failed_checks=failed_checks,
            intended_action=request.intended_action,
            confidence=request.confidence,
            claims=claims,
            high_impact_review_required=requires_human_review,
            high_impact_review_reason=review_reason,
            governance_review_required=governance_requires_review,
            governance_reason=governance_reason
        )
        
        # Step 7: Build details
        check_results = [confidence_check, evidence_check, rules_check]
        details = self.verdict_engine.build_details(
            claims=claims,
            risk_score=risk_score,
            evidence_passed=evidence_passed,
            rules_passed=rules_passed,
            confidence_aligned=confidence_aligned,
            check_results=check_results,
            sources=request.sources or []
        )
        
        logger.info(
            f"Firewall check completed: verdict={verdict.value}, "
            f"risk_score={risk_score:.3f}, failed_checks={failed_checks}"
        )
        
        # Build response
        response = FirewallResponse(
            verdict=verdict,
            reason=verdict_reason,
            risk_score=risk_score,
            details=details,
            failed_checks=failed_checks,
            explanation=explanation,
            confidence_alignment=confidence_aligned,
            applied_policies=applied_policies,
            escalation_reason=escalation_reason
        )
        
        # Enterprise mode: Audit logging
        if self.audit_logger:
            self.audit_logger.log_decision(request, response)
        
        # Record metrics
        is_hallucination = (
            verdict == Verdict.BLOCK and 
            "evidence" in failed_checks and 
            request.confidence > 0.7
        )
        self.metrics.record_request(
            verdict=verdict,
            intended_action=request.intended_action,
            is_hallucination=is_hallucination
        )
        
        # Record blocked decisions for learning
        if verdict == Verdict.BLOCK:
            self.memory.record_blocked_decision(request, response)
        
        # Enterprise mode: Force human review for high-risk decisions
        if ENTERPRISE_MODE and risk_score >= 0.7 and verdict == Verdict.ALLOW:
            # Override to require human review
            response.verdict = Verdict.REQUIRE_HUMAN_REVIEW
            response.reason = "Enterprise mode: High-risk decision requires human review"
            response.explanation = (
                f"Enterprise mode requires human review for high-risk decisions "
                f"(risk score: {risk_score:.2f}). Original verdict was ALLOW."
            )
        
        return response

