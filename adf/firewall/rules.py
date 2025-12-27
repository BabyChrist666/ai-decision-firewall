"""
Policy and logic rules engine.
"""
from typing import List, Dict, Any
from ..models import Claim
from ..utils.logger import logger


class RulesEngine:
    """Applies policy and logic rules to claims."""
    
    # High-impact actions that require special scrutiny
    HIGH_IMPACT_ACTIONS = {"trade", "execute_code"}
    
    # Minimum confidence threshold for high-impact actions to bypass human review
    HIGH_IMPACT_CONFIDENCE_THRESHOLD = 0.8
    
    def __init__(self):
        """Initialize rules engine."""
        # Define unsafe patterns
        self.unsafe_patterns = [
            r'\b(?:delete|drop|truncate|format|rm\s+-rf)\s+',
            r'\b(?:sudo|admin|root)\s+',
            r'\b(?:password|secret|key|token)\s*=\s*["\']',
            r'<script[^>]*>',
            r'eval\s*\(',
            r'exec\s*\(',
        ]
        
        # Define potentially harmful action patterns
        self.harmful_patterns = [
            r'\b(?:kill|terminate|destroy|remove)\s+',
            r'\b(?:transfer|send|move)\s+\$\d+',
            r'\b(?:execute|run|call)\s+.*\b(?:dangerous|unsafe|risky)',
        ]
    
    def check_rules(
        self,
        claims: List[Claim],
        ai_output: str,
        intended_action: str
    ) -> tuple[bool, str, List[str]]:
        """
        Apply all rules to claims and output.
        
        Args:
            claims: List of claims
            ai_output: Full AI output text
            intended_action: Intended action type
            
        Returns:
            Tuple of (passed, reason, failed_rules)
        """
        failed_rules = []
        
        # Check for unsafe patterns in output
        unsafe_check = self._check_unsafe_patterns(ai_output)
        if not unsafe_check[0]:
            failed_rules.append("unsafe_patterns")
            logger.warning(f"Unsafe patterns detected: {unsafe_check[1]}")
        
        # Check for harmful actions based on action type
        if intended_action in ["trade", "execute_code"]:
            harmful_check = self._check_harmful_actions(ai_output, intended_action)
            if not harmful_check[0]:
                failed_rules.append("harmful_actions")
                logger.warning(f"Harmful actions detected: {harmful_check[1]}")
        
        # Check for contradictory claims
        contradiction_check = self._check_contradictions(claims)
        if not contradiction_check[0]:
            failed_rules.append("contradictions")
            logger.warning(f"Contradictions detected: {contradiction_check[1]}")
        
        if failed_rules:
            return False, f"Rules violated: {', '.join(failed_rules)}", failed_rules
        
        return True, "All rules passed", []
    
    def _check_unsafe_patterns(self, text: str) -> tuple[bool, str]:
        """
        Check for unsafe code/command patterns.
        
        Args:
            text: Text to check
            
        Returns:
            Tuple of (is_safe, reason)
        """
        import re
        
        for pattern in self.unsafe_patterns:
            if re.search(pattern, text, re.IGNORECASE):
                return False, f"Unsafe pattern detected: {pattern}"
        
        return True, "No unsafe patterns detected"
    
    def _check_harmful_actions(self, text: str, action_type: str) -> tuple[bool, str]:
        """
        Check for potentially harmful actions.
        
        Args:
            text: Text to check
            action_type: Type of action being performed
            
        Returns:
            Tuple of (is_safe, reason)
        """
        import re
        
        for pattern in self.harmful_patterns:
            if re.search(pattern, text, re.IGNORECASE):
                return False, f"Potentially harmful action detected: {pattern}"
        
        # Additional checks for specific action types
        if action_type == "trade":
            # Check for large amounts or risky trades
            large_amount = re.search(r'\$\s*\d{6,}', text)  # $1000000+
            if large_amount:
                return False, "Large trade amount detected without proper safeguards"
        
        if action_type == "execute_code":
            # Check for system-level operations
            system_ops = re.search(r'\b(?:system|os|subprocess|shell)\s*\.', text, re.IGNORECASE)
            if system_ops:
                return False, "System-level operations detected in code execution"
        
        return True, "No harmful actions detected"
    
    def _check_contradictions(self, claims: List[Claim]) -> tuple[bool, str]:
        """
        Check for contradictory claims.
        
        Args:
            claims: List of claims to check
            
        Returns:
            Tuple of (is_consistent, reason)
        """
        # Simple contradiction detection based on keywords
        # In a production system, this would use more sophisticated NLP
        
        factual_claims = [c.text.lower() for c in claims if c.is_factual]
        
        # Check for common contradictions
        contradiction_pairs = [
            ("is", "is not"),
            ("was", "was not"),
            ("has", "has not"),
            ("founded in", "founded in"),  # Same date mentioned twice differently
        ]
        
        # For now, just check if we have very similar claims that might contradict
        # This is a simplified version
        if len(factual_claims) > 1:
            # Check for duplicate claims (might indicate issues)
            if len(factual_claims) != len(set(factual_claims)):
                return False, "Duplicate claims detected"
        
        return True, "No contradictions detected"
    
    def requires_human_review_for_high_impact(
        self,
        intended_action: str,
        confidence: float,
        has_evidence: bool
    ) -> tuple[bool, str]:
        """
        Check if high-impact action requires human review.
        
        Enterprise rule: High-impact actions require human review unless:
        - confidence >= 0.8
        - AND evidence is present
        
        Args:
            intended_action: Intended action type
            confidence: Confidence score (0-1)
            has_evidence: Whether evidence is present
            
        Returns:
            Tuple of (requires_review, reason)
        """
        if intended_action.lower() not in self.HIGH_IMPACT_ACTIONS:
            return False, "Not a high-impact action"
        
        # High-impact actions require human review unless both conditions met
        if confidence < self.HIGH_IMPACT_CONFIDENCE_THRESHOLD or not has_evidence:
            reason = (
                f"High-impact action ({intended_action}) requires human review. "
                f"Confidence ({confidence:.2f}) is below threshold ({self.HIGH_IMPACT_CONFIDENCE_THRESHOLD}) "
                f"or evidence is missing."
            )
            return True, reason
        
        return False, "High-impact action meets confidence and evidence requirements"

