"""
Confidence scoring and validation.
"""
from typing import List
from ..models import Claim
from ..config import (
    CONFIDENCE_THRESHOLD_EVIDENCE_REQUIRED,
    CONFIDENCE_THRESHOLD_HIGH,
    CONFIDENCE_THRESHOLD_LOW
)
from ..utils.logger import logger


class ConfidenceChecker:
    """Validates and analyzes confidence scores."""
    
    def __init__(self):
        """Initialize confidence checker."""
        self.evidence_threshold = CONFIDENCE_THRESHOLD_EVIDENCE_REQUIRED
        self.high_threshold = CONFIDENCE_THRESHOLD_HIGH
        self.low_threshold = CONFIDENCE_THRESHOLD_LOW
    
    def requires_evidence(self, confidence: float) -> bool:
        """
        Check if confidence level requires evidence.
        
        Args:
            confidence: Confidence score (0-1)
            
        Returns:
            True if evidence is required
        """
        return confidence > self.evidence_threshold
    
    def is_high_confidence(self, confidence: float) -> bool:
        """
        Check if confidence is high.
        
        Args:
            confidence: Confidence score (0-1)
            
        Returns:
            True if high confidence
        """
        return confidence >= self.high_threshold
    
    def is_low_confidence(self, confidence: float) -> bool:
        """
        Check if confidence is low.
        
        Args:
            confidence: Confidence score (0-1)
            
        Returns:
            True if low confidence
        """
        return confidence < self.low_threshold
    
    def validate_confidence_alignment(
        self,
        overall_confidence: float,
        claims: List[Claim]
    ) -> tuple[bool, str]:
        """
        Validate that confidence aligns with claim characteristics.
        
        Args:
            overall_confidence: Overall confidence from request
            claims: List of parsed claims
            
        Returns:
            Tuple of (is_valid, reason)
        """
        if not claims:
            return True, "No claims to validate"
        
        # Check if high confidence claims exist without evidence
        high_confidence_factual = [
            c for c in claims
            if c.is_factual and c.confidence > self.evidence_threshold
        ]
        
        if high_confidence_factual and overall_confidence > self.evidence_threshold:
            # High confidence factual claims should have evidence
            return False, "High confidence factual claims detected"
        
        # Check for confidence mismatch
        if overall_confidence > self.high_threshold:
            # Very high confidence should be justified
            factual_count = sum(1 for c in claims if c.is_factual)
            if factual_count == 0:
                return True, "High confidence on non-factual content is acceptable"
        
        return True, "Confidence alignment validated"
    
    def calculate_uncertainty(self, confidence: float) -> float:
        """
        Calculate uncertainty from confidence.
        
        Args:
            confidence: Confidence score (0-1)
            
        Returns:
            Uncertainty score (0-1), where 1 = maximum uncertainty
        """
        return 1.0 - confidence






