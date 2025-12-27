"""
Policy modes and governance rules for AI Decision Firewall.

Governance rules are MANDATORY and override risk scoring.
They define which actions ALWAYS require human review regardless of confidence or evidence.
"""
from typing import List, Set, Dict
from enum import Enum


class PolicyMode(str, Enum):
    """Policy compliance modes for different industry contexts."""
    GENERAL_AI = "GENERAL_AI"
    FINANCIAL_SERVICES = "FINANCIAL_SERVICES"
    HEALTHCARE = "HEALTHCARE"
    LEGAL = "LEGAL"


class PolicyManager:
    """
    Manages governance policies and mandatory escalation rules.
    
    CRITICAL: Governance rules override ALL other factors including:
    - High confidence
    - Presence of evidence
    - Low risk scores
    
    These rules enforce that certain actions MUST NEVER be auto-approved.
    """
    
    def __init__(self, mode: PolicyMode = PolicyMode.GENERAL_AI):
        """
        Initialize policy manager.
        
        Args:
            mode: Policy compliance mode
        """
        self.mode = mode
        self._setup_policies()
    
    def _setup_policies(self):
        """Setup policy configurations for each mode."""
        # Actions that ALWAYS require human review (governance override)
        # These override risk scoring, confidence, and evidence
        self.mandatory_review_actions: Set[str] = set()
        
        # Mode-specific configurations
        if self.mode == PolicyMode.GENERAL_AI:
            # General mode: conservative defaults
            self.mandatory_review_actions = {"trade", "execute_code"}
            self.confidence_threshold_evidence_required = 0.6
            self.risk_threshold_medium = 0.6
            
        elif self.mode == PolicyMode.FINANCIAL_SERVICES:
            # Financial services: strict trade enforcement
            self.mandatory_review_actions = {"trade", "execute_code"}
            self.confidence_threshold_evidence_required = 0.7
            self.risk_threshold_medium = 0.5
            
        elif self.mode == PolicyMode.HEALTHCARE:
            # Healthcare: medical actions require review
            self.mandatory_review_actions = {"medical", "execute_code", "trade"}
            self.confidence_threshold_evidence_required = 0.8
            self.risk_threshold_medium = 0.4
            
        elif self.mode == PolicyMode.LEGAL:
            # Legal: legal actions require review
            self.mandatory_review_actions = {"legal", "execute_code", "trade"}
            self.confidence_threshold_evidence_required = 0.8
            self.risk_threshold_medium = 0.4
    
    def requires_mandatory_review(self, intended_action: str) -> tuple[bool, str]:
        """
        Check if action requires mandatory human review (governance rule).
        
        This is a HARD GOVERNANCE RULE that overrides all other factors.
        
        Args:
            intended_action: Intended action type
            
        Returns:
            Tuple of (requires_review, reason)
        """
        action_lower = intended_action.lower()
        
        if action_lower in self.mandatory_review_actions:
            reason = (
                f"Governance rule: {intended_action} actions require mandatory human review "
                f"in {self.mode.value} policy mode. This requirement cannot be overridden by "
                f"high confidence or evidence presence."
            )
            return True, reason
        
        return False, ""
    
    def get_policy_info(self) -> Dict:
        """
        Get current policy configuration information.
        
        Returns:
            Dictionary with policy details
        """
        return {
            "mode": self.mode.value,
            "mandatory_review_actions": list(self.mandatory_review_actions),
            "confidence_threshold_evidence_required": self.confidence_threshold_evidence_required,
            "risk_threshold_medium": self.risk_threshold_medium,
            "description": self._get_mode_description()
        }
    
    def _get_mode_description(self) -> str:
        """Get human-readable description of current policy mode."""
        descriptions = {
            PolicyMode.GENERAL_AI: "General AI governance with conservative defaults",
            PolicyMode.FINANCIAL_SERVICES: "Financial services compliance - all trades require human review",
            PolicyMode.HEALTHCARE: "Healthcare compliance - medical actions require human review",
            PolicyMode.LEGAL: "Legal compliance - legal actions require human review"
        }
        return descriptions.get(self.mode, "Unknown policy mode")


# Global policy manager instance (initialized with default mode)
_policy_manager: PolicyManager = PolicyManager(PolicyMode.GENERAL_AI)


def get_policy_manager() -> PolicyManager:
    """Get the global policy manager instance."""
    return _policy_manager


def set_policy_mode(mode: PolicyMode):
    """Set the global policy mode."""
    global _policy_manager
    _policy_manager = PolicyManager(mode)


