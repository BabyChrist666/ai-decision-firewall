"""
Risk scoring engine.
"""
from typing import List
from ..models import Claim
from ..config import ACTION_IMPACT, DEFAULT_ACTION_IMPACT
from ..firewall.confidence import ConfidenceChecker
from ..utils.logger import logger


class RiskScorer:
    """Calculates risk scores based on uncertainty and action impact."""
    
    def __init__(self):
        """Initialize risk scorer."""
        self.confidence_checker = ConfidenceChecker()
    
    def calculate_risk_score(
        self,
        confidence: float,
        intended_action: str,
        claims: List[Claim],
        has_evidence: bool = True
    ) -> float:
        """
        Calculate overall risk score.
        
        Risk = uncertainty × action_impact × evidence_factor
        
        Args:
            confidence: Overall confidence score
            intended_action: Intended action type
            claims: List of parsed claims
            has_evidence: Whether evidence is available
            
        Returns:
            Risk score (0-1), where 1 = maximum risk
        """
        # Calculate uncertainty (inverse of confidence)
        uncertainty = self.confidence_checker.calculate_uncertainty(confidence)
        
        # Get action impact
        action_impact = ACTION_IMPACT.get(intended_action.lower(), DEFAULT_ACTION_IMPACT)
        
        # Evidence factor: increases risk if no evidence for factual claims
        evidence_factor = 1.0
        if not has_evidence:
            factual_claims = [c for c in claims if c.is_factual]
            if factual_claims:
                # High confidence factual claims without evidence = high risk
                high_conf_factual = [
                    c for c in factual_claims
                    if c.confidence > 0.6
                ]
                if high_conf_factual:
                    evidence_factor = 1.5  # Increase risk by 50%
        
        # Calculate base risk
        base_risk = uncertainty * action_impact * evidence_factor
        
        # Apply additional factors
        # More claims = slightly higher risk (more things to verify)
        claim_factor = 1.0 + (len(claims) * 0.05)  # +5% per claim, capped
        claim_factor = min(claim_factor, 1.3)  # Cap at 30% increase
        
        risk_score = base_risk * claim_factor
        
        # Normalize to 0-1 range
        risk_score = min(1.0, max(0.0, risk_score))
        
        logger.info(
            f"Risk score calculated: {risk_score:.3f} "
            f"(uncertainty={uncertainty:.3f}, impact={action_impact:.3f}, "
            f"evidence_factor={evidence_factor:.3f}, claim_factor={claim_factor:.3f})"
        )
        
        return risk_score
    
    def get_risk_level(self, risk_score: float) -> str:
        """
        Get risk level category.
        
        Args:
            risk_score: Risk score (0-1)
            
        Returns:
            Risk level: "low", "medium", "high", "critical"
        """
        if risk_score < 0.3:
            return "low"
        elif risk_score < 0.6:
            return "medium"
        elif risk_score < 0.8:
            return "high"
        else:
            return "critical"






