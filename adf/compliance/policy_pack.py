"""
Industry-specific policy packs for compliance.
"""
from typing import Dict, List, Any
from enum import Enum


class IndustryType(str, Enum):
    """Supported industry types."""
    FINANCE = "finance"
    HEALTHCARE = "healthcare"
    LEGAL = "legal"
    GENERAL = "general"


class PolicyPack:
    """Industry-specific policy configuration."""
    
    def __init__(
        self,
        industry: IndustryType,
        strictness: str = "medium",
        custom_rules: List[Dict[str, Any]] = None
    ):
        """
        Initialize policy pack.
        
        Args:
            industry: Industry type
            strictness: Strictness level (low, medium, high)
            custom_rules: Optional custom rules
        """
        self.industry = industry
        self.strictness = strictness
        self.custom_rules = custom_rules or []
        self.policies = self._load_policies()
    
    def _load_policies(self) -> Dict[str, Any]:
        """
        Load industry-specific policies.
        
        Returns:
            Policy configuration dictionary
        """
        base_policies = {
            IndustryType.FINANCE: {
                "confidence_threshold": 0.7,
                "risk_threshold_medium": 0.5,
                "risk_threshold_high": 0.75,
                "require_evidence_for": ["trade", "execute_code"],
                "mandatory_human_review_for": ["trade"],
                "action_impact_multipliers": {
                    "trade": 1.2,
                    "execute_code": 1.3
                }
            },
            IndustryType.HEALTHCARE: {
                "confidence_threshold": 0.85,
                "risk_threshold_medium": 0.4,
                "risk_threshold_high": 0.7,
                "require_evidence_for": ["answer", "email"],
                "mandatory_human_review_for": ["answer"],
                "action_impact_multipliers": {
                    "answer": 1.5,
                    "email": 1.2
                }
            },
            IndustryType.LEGAL: {
                "confidence_threshold": 0.8,
                "risk_threshold_medium": 0.5,
                "risk_threshold_high": 0.75,
                "require_evidence_for": ["answer", "email"],
                "mandatory_human_review_for": ["answer", "email"],
                "action_impact_multipliers": {
                    "answer": 1.4,
                    "email": 1.3
                }
            },
            IndustryType.GENERAL: {
                "confidence_threshold": 0.6,
                "risk_threshold_medium": 0.6,
                "risk_threshold_high": 0.8,
                "require_evidence_for": [],
                "mandatory_human_review_for": [],
                "action_impact_multipliers": {}
            }
        }
        
        policies = base_policies.get(self.industry, base_policies[IndustryType.GENERAL])
        
        # Adjust for strictness
        if self.strictness == "high":
            policies["confidence_threshold"] = min(0.9, policies["confidence_threshold"] + 0.1)
            policies["risk_threshold_medium"] = max(0.3, policies["risk_threshold_medium"] - 0.1)
        elif self.strictness == "low":
            policies["confidence_threshold"] = max(0.4, policies["confidence_threshold"] - 0.1)
            policies["risk_threshold_medium"] = min(0.8, policies["risk_threshold_medium"] + 0.1)
        
        return policies
    
    def get_confidence_threshold(self) -> float:
        """Get confidence threshold for this policy."""
        return self.policies["confidence_threshold"]
    
    def get_risk_threshold_medium(self) -> float:
        """Get medium risk threshold."""
        return self.policies["risk_threshold_medium"]
    
    def get_risk_threshold_high(self) -> float:
        """Get high risk threshold."""
        return self.policies["risk_threshold_high"]
    
    def requires_evidence_for(self, action: str) -> bool:
        """Check if evidence is required for action."""
        return action in self.policies["require_evidence_for"]
    
    def requires_human_review_for(self, action: str) -> bool:
        """Check if human review is required for action."""
        return action in self.policies["mandatory_human_review_for"]
    
    def get_action_impact_multiplier(self, action: str) -> float:
        """Get impact multiplier for action."""
        return self.policies["action_impact_multipliers"].get(action, 1.0)


# Pre-configured policy packs
FINANCE_POLICY = PolicyPack(IndustryType.FINANCE, strictness="high")
HEALTHCARE_POLICY = PolicyPack(IndustryType.HEALTHCARE, strictness="high")
LEGAL_POLICY = PolicyPack(IndustryType.LEGAL, strictness="high")
GENERAL_POLICY = PolicyPack(IndustryType.GENERAL, strictness="medium")






