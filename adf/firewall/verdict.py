"""
Verdict engine: determines final decision (ALLOW/BLOCK/etc).
"""
from typing import List, Dict, Any, Optional
from ..models import Verdict, Claim, CheckResult
from ..config import (
    RISK_THRESHOLD_LOW,
    RISK_THRESHOLD_MEDIUM,
    RISK_THRESHOLD_HIGH
)
from ..utils.logger import logger


class VerdictEngine:
    """Determines final verdict based on all checks."""
    
    def __init__(self):
        """Initialize verdict engine."""
        self.risk_low = RISK_THRESHOLD_LOW
        self.risk_medium = RISK_THRESHOLD_MEDIUM
        self.risk_high = RISK_THRESHOLD_HIGH
    
    def determine_verdict(
        self,
        risk_score: float,
        evidence_passed: bool,
        rules_passed: bool,
        confidence_aligned: bool,
        failed_checks: List[str],
        intended_action: str,
        confidence: float,
        claims: List[Claim],
        high_impact_review_required: bool = False,
        high_impact_review_reason: str = "",
        governance_review_required: bool = False,
        governance_reason: str = ""
    ) -> tuple[Verdict, str, str, List[str], Optional[str]]:
        """
        Determine final verdict based on all factors.
        
        CRITICAL: Governance rules are checked FIRST and override all other factors.
        
        Args:
            risk_score: Calculated risk score
            evidence_passed: Whether evidence check passed
            rules_passed: Whether rules check passed
            confidence_aligned: Whether confidence is aligned
            failed_checks: List of failed check names
            intended_action: Intended action type
            confidence: Overall confidence score
            claims: List of parsed claims
            high_impact_review_required: Whether high-impact action requires review
            high_impact_review_reason: Reason for high-impact review requirement
            governance_review_required: Whether governance rule requires mandatory review
            governance_reason: Reason for governance review requirement
            
        Returns:
            Tuple of (verdict, reason, explanation, applied_policies, escalation_reason)
        """
        applied_policies = []
        escalation_reason = None
        
        # PRIORITY 0: GOVERNANCE RULES (HIGHEST PRIORITY - OVERRIDES EVERYTHING)
        # These rules ALWAYS require human review regardless of confidence, evidence, or risk score
        if governance_review_required:
            applied_policies.append("mandatory_governance_review")
            escalation_reason = governance_reason
            explanation = (
                f"This {intended_action} action requires mandatory human review due to governance policy. "
                f"This requirement cannot be overridden by high confidence, evidence, or low risk scores. "
                f"{governance_reason}"
            )
            return Verdict.REQUIRE_HUMAN_REVIEW, "Governance rule: mandatory human review required", explanation, applied_policies, escalation_reason
        
        # Priority 1: Block if rules failed (safety first)
        if not rules_passed:
            applied_policies.append("safety_rules")
            explanation = (
                f"Blocked because the output contains unsafe patterns or harmful actions "
                f"that violate safety rules. The {intended_action} action cannot proceed."
            )
            return Verdict.BLOCK, "Safety rules violated - output contains unsafe patterns or harmful actions", explanation, applied_policies, escalation_reason
        
        # Priority 2: Block if high risk and critical action
        if risk_score >= self.risk_high and intended_action in ["trade", "execute_code"]:
            applied_policies.append("high_risk_block")
            explanation = (
                f"Blocked because the risk score ({risk_score:.2f}) is critical for a high-impact action "
                f"({intended_action}). The system cannot proceed without human oversight."
            )
            return Verdict.BLOCK, f"Critical risk score ({risk_score:.2f}) for high-impact action ({intended_action})", explanation, applied_policies, escalation_reason
        
        # Priority 3: Require evidence if evidence check failed
        if not evidence_passed:
            applied_policies.append("evidence_requirement")
            factual_count = sum(1 for c in claims if c.is_factual)
            if risk_score >= self.risk_medium:
                explanation = (
                    f"Blocked because the model expressed {confidence:.2f} confidence in {factual_count} "
                    f"factual claim(s) without providing evidence, violating grounding rules. "
                    f"Additionally, the risk score ({risk_score:.2f}) exceeds the medium threshold."
                )
                return Verdict.BLOCK, "High confidence factual claims without evidence and medium+ risk", explanation, applied_policies, escalation_reason
            
            explanation = (
                f"Requires evidence because the model expressed {confidence:.2f} confidence in {factual_count} "
                f"factual claim(s) without providing supporting sources. Evidence must be provided before proceeding."
            )
            return Verdict.REQUIRE_EVIDENCE, "High confidence factual claims require evidence", explanation, applied_policies, escalation_reason
        
        # Priority 4: Require human review for medium-high risk
        if risk_score >= self.risk_medium:
            applied_policies.append("risk_based_review")
            if intended_action in ["trade", "execute_code"]:
                escalation_reason = f"Risk score ({risk_score:.2f}) is medium-high for high-impact action ({intended_action})"
                explanation = (
                    f"Requires human review because the risk score ({risk_score:.2f}) is medium-high "
                    f"for a high-impact action ({intended_action}). A human must approve before proceeding."
                )
                return Verdict.REQUIRE_HUMAN_REVIEW, f"Medium-high risk ({risk_score:.2f}) for high-impact action", explanation, applied_policies, escalation_reason
            
            escalation_reason = f"Risk score ({risk_score:.2f}) exceeds medium threshold"
            explanation = (
                f"Requires human review because the risk score ({risk_score:.2f}) exceeds the medium threshold. "
                f"A human must review the output before it can proceed."
            )
            return Verdict.REQUIRE_HUMAN_REVIEW, f"Medium-high risk score ({risk_score:.2f}) requires review", explanation, applied_policies, escalation_reason
        
        # Priority 5: Confidence alignment issues
        # Evidence Override Rule: If evidence exists, confidence_alignment is a warning only
        if not confidence_aligned:
            # Only block if evidence is missing
            if not evidence_passed:
                applied_policies.append("confidence_alignment_check")
                if risk_score >= self.risk_medium:
                    escalation_reason = f"Confidence alignment issues detected with medium+ risk and no evidence"
                    explanation = (
                        f"Requires human review because confidence alignment issues were detected "
                        f"(confidence {confidence:.2f} does not match claim characteristics) and the risk score "
                        f"({risk_score:.2f}) is medium or higher. Evidence is also missing."
                    )
                    return Verdict.REQUIRE_HUMAN_REVIEW, "Confidence alignment issues with medium+ risk and no evidence", explanation, applied_policies, escalation_reason
                
                explanation = (
                    f"Requires evidence because confidence alignment issues were detected. "
                    f"The model's confidence ({confidence:.2f}) does not align with the characteristics of the claims."
                )
                return Verdict.REQUIRE_EVIDENCE, "Confidence alignment issues detected", explanation, applied_policies, escalation_reason
            # If evidence exists, confidence_alignment is a warning only - continue to next priority
        
        # Priority 6: High-impact action policy (BEFORE default ALLOW)
        # Enterprise rule: High-impact actions require human review unless:
        # - confidence >= 0.8 AND evidence is present
        if high_impact_review_required:
            applied_policies.append("high_impact_policy")
            escalation_reason = high_impact_review_reason
            explanation = (
                f"High-impact action requires human review due to insufficient confidence or evidence. "
                f"{high_impact_review_reason}"
            )
            return Verdict.REQUIRE_HUMAN_REVIEW, "High-impact action requires human review", explanation, applied_policies, escalation_reason
        
        # Default: Allow if all checks pass and risk is low
        if risk_score < self.risk_low:
            applied_policies.append("low_risk_allow")
            # Check if we have evidence override for confidence alignment
            if not confidence_aligned and evidence_passed:
                explanation = (
                    f"Allowed despite confidence misalignment because supporting evidence was provided. "
                    f"The risk score ({risk_score:.2f}) is low and all critical checks passed."
                )
            else:
                explanation = (
                    f"Allowed because all checks passed and the risk score ({risk_score:.2f}) is low. "
                    f"The output meets all safety and grounding requirements."
                )
            return Verdict.ALLOW, "All checks passed, low risk", explanation, applied_policies, escalation_reason
        
        # Low-medium risk: allow but log
        applied_policies.append("acceptable_risk_allow")
        # Check if we have evidence override for confidence alignment
        if not confidence_aligned and evidence_passed:
            explanation = (
                f"Allowed despite confidence misalignment because supporting evidence was provided. "
                f"The risk score ({risk_score:.2f}) is acceptable for the {intended_action} action."
            )
        else:
            explanation = (
                f"Allowed because all checks passed. The risk score ({risk_score:.2f}) is acceptable "
                f"for the {intended_action} action."
            )
        return Verdict.ALLOW, f"All checks passed, acceptable risk ({risk_score:.2f})", explanation, applied_policies, escalation_reason
    
    def build_details(
        self,
        claims: List[Claim],
        risk_score: float,
        evidence_passed: bool,
        rules_passed: bool,
        confidence_aligned: bool,
        check_results: List[CheckResult],
        sources: List[str]
    ) -> Dict[str, Any]:
        """
        Build detailed response information.
        
        Args:
            claims: List of parsed claims
            risk_score: Risk score
            evidence_passed: Evidence check result
            rules_passed: Rules check result
            confidence_aligned: Confidence alignment result
            check_results: List of check results
            sources: List of sources
            
        Returns:
            Dictionary with detailed information
        """
        return {
            "claims": [
                {
                    "text": c.text,
                    "is_factual": c.is_factual,
                    "confidence": c.confidence
                }
                for c in claims
            ],
            "claim_count": len(claims),
            "factual_claim_count": sum(1 for c in claims if c.is_factual),
            "risk_score": risk_score,
            "risk_level": self._get_risk_level(risk_score),
            "checks": {
                "evidence": {
                    "passed": evidence_passed,
                    "result": "PASS" if evidence_passed else "FAIL"
                },
                "rules": {
                    "passed": rules_passed,
                    "result": "PASS" if rules_passed else "FAIL"
                },
                "confidence_alignment": {
                    "passed": confidence_aligned,
                    "result": "PASS" if confidence_aligned else "FAIL"
                }
            },
            "check_results": [
                {
                    "check_name": cr.check_name,
                    "passed": cr.passed,
                    "reason": cr.reason
                }
                for cr in check_results
            ],
            "sources": {
                "count": len(sources),
                "provided": len(sources) > 0
            }
        }
    
    def _get_risk_level(self, risk_score: float) -> str:
        """Get risk level category."""
        if risk_score < self.risk_low:
            return "low"
        elif risk_score < self.risk_medium:
            return "medium"
        elif risk_score < self.risk_high:
            return "high"
        else:
            return "critical"

