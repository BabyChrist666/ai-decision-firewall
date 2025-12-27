"""
Adaptive policy tuning based on learning memory.
"""
from typing import Dict, Any
from ..config import (
    CONFIDENCE_THRESHOLD_EVIDENCE_REQUIRED,
    RISK_THRESHOLD_MEDIUM,
    ADAPTIVE_STRICTNESS,
    MIN_FALSE_POSITIVES_FOR_RELAX,
    MIN_FALSE_NEGATIVES_FOR_STRICT
)
from .memory import LearningMemory
from ..utils.logger import logger


class PolicyUpdater:
    """Adapts firewall policy based on past performance."""
    
    def __init__(self, memory: LearningMemory):
        """
        Initialize policy updater.
        
        Args:
            memory: Learning memory instance
        """
        self.memory = memory
        self.base_confidence_threshold = CONFIDENCE_THRESHOLD_EVIDENCE_REQUIRED
        self.base_risk_threshold = RISK_THRESHOLD_MEDIUM
    
    def get_adaptive_thresholds(self) -> Dict[str, float]:
        """
        Get adaptive thresholds based on learning.
        
        Returns:
            Dictionary with adjusted thresholds
        """
        if not ADAPTIVE_STRICTNESS:
            return {
                "confidence_threshold": self.base_confidence_threshold,
                "risk_threshold_medium": self.base_risk_threshold
            }
        
        stats = self.memory.get_statistics()
        false_positive_rate = stats.get("false_positive_rate", 0.0)
        false_negative_rate = stats.get("false_negative_rate", 0.0)
        false_positives = stats.get("false_positive_count", 0)
        false_negatives = stats.get("false_negative_count", 0)
        
        # Adjust confidence threshold
        confidence_threshold = self.base_confidence_threshold
        
        # If many false positives, relax (increase threshold = less strict)
        if false_positives >= MIN_FALSE_POSITIVES_FOR_RELAX and false_positive_rate > 0.2:
            confidence_threshold = min(0.8, confidence_threshold + 0.05)
            logger.info(f"Relaxing confidence threshold to {confidence_threshold} due to false positives")
        
        # If many false negatives, tighten (decrease threshold = more strict)
        if false_negatives >= MIN_FALSE_NEGATIVES_FOR_STRICT and false_negative_rate > 0.1:
            confidence_threshold = max(0.4, confidence_threshold - 0.05)
            logger.info(f"Tightening confidence threshold to {confidence_threshold} due to false negatives")
        
        # Adjust risk threshold
        risk_threshold = self.base_risk_threshold
        
        # Similar adjustments for risk
        if false_positives >= MIN_FALSE_POSITIVES_FOR_RELAX and false_positive_rate > 0.2:
            risk_threshold = min(0.8, risk_threshold + 0.05)
        
        if false_negatives >= MIN_FALSE_NEGATIVES_FOR_STRICT and false_negative_rate > 0.1:
            risk_threshold = max(0.4, risk_threshold - 0.05)
        
        return {
            "confidence_threshold": confidence_threshold,
            "risk_threshold_medium": risk_threshold,
            "adjustment_reason": self._get_adjustment_reason(false_positives, false_negatives)
        }
    
    def _get_adjustment_reason(self, false_positives: int, false_negatives: int) -> str:
        """
        Get reason for threshold adjustments.
        
        Args:
            false_positives: Number of false positives
            false_negatives: Number of false negatives
            
        Returns:
            Reason string
        """
        if false_positives >= MIN_FALSE_POSITIVES_FOR_RELAX:
            return f"Relaxing due to {false_positives} false positives"
        elif false_negatives >= MIN_FALSE_NEGATIVES_FOR_STRICT:
            return f"Tightening due to {false_negatives} false negatives"
        return "No adjustment needed"






