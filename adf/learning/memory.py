"""
Learning memory system for tracking failures and overrides.
"""
import json
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime
from ..config import MEMORY_STORAGE_DIR, MEMORY_FILE, LEARNING_ENABLED
from ..models import FirewallRequest, FirewallResponse, Verdict
from ..utils.logger import logger


class LearningMemory:
    """Stores and learns from past firewall decisions."""
    
    def __init__(self, memory_file: Optional[str] = None):
        """
        Initialize learning memory.
        
        Args:
            memory_file: Optional custom memory file path
        """
        self.memory_file = memory_file or MEMORY_FILE
        self._ensure_memory_directory()
        self.memory = self._load_memory()
    
    def _ensure_memory_directory(self) -> None:
        """Ensure memory directory exists."""
        memory_path = Path(self.memory_file)
        memory_path.parent.mkdir(parents=True, exist_ok=True)
    
    def _load_memory(self) -> Dict[str, Any]:
        """
        Load memory from disk.
        
        Returns:
            Memory dictionary
        """
        if not Path(self.memory_file).exists():
            return {
                "blocked_decisions": [],
                "human_overrides": [],
                "false_positives": [],
                "false_negatives": [],
                "statistics": {
                    "total_blocks": 0,
                    "total_overrides": 0,
                    "false_positive_count": 0,
                    "false_negative_count": 0
                }
            }
        
        try:
            with open(self.memory_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Failed to load memory: {str(e)}", exc_info=True)
            return {
                "blocked_decisions": [],
                "human_overrides": [],
                "false_positives": [],
                "false_negatives": [],
                "statistics": {
                    "total_blocks": 0,
                    "total_overrides": 0,
                    "false_positive_count": 0,
                    "false_negative_count": 0
                }
            }
    
    def _save_memory(self) -> None:
        """Save memory to disk."""
        try:
            with open(self.memory_file, 'w', encoding='utf-8') as f:
                json.dump(self.memory, f, indent=2)
        except Exception as e:
            logger.error(f"Failed to save memory: {str(e)}", exc_info=True)
    
    def record_blocked_decision(
        self,
        request: FirewallRequest,
        response: FirewallResponse
    ) -> None:
        """
        Record a blocked decision.
        
        Args:
            request: Original request
            response: Firewall response
        """
        if not LEARNING_ENABLED:
            return
        
        record = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "ai_output": request.ai_output[:200],  # Truncate for storage
            "confidence": request.confidence,
            "intended_action": request.intended_action,
            "verdict": response.verdict.value,
            "risk_score": response.risk_score,
            "failed_checks": response.failed_checks,
            "explanation": response.explanation
        }
        
        self.memory["blocked_decisions"].append(record)
        self.memory["statistics"]["total_blocks"] += 1
        self._save_memory()
    
    def record_human_override(
        self,
        original_verdict: Verdict,
        override_verdict: Verdict,
        reason: str,
        request: Optional[FirewallRequest] = None
    ) -> None:
        """
        Record a human override decision.
        
        Args:
            original_verdict: Original firewall verdict
            override_verdict: Human override verdict
            reason: Reason for override
            request: Optional original request
        """
        if not LEARNING_ENABLED:
            return
        
        record = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "original_verdict": original_verdict.value,
            "override_verdict": override_verdict.value,
            "reason": reason,
            "ai_output_preview": request.ai_output[:200] if request else None
        }
        
        self.memory["human_overrides"].append(record)
        self.memory["statistics"]["total_overrides"] += 1
        
        # Track false positives/negatives
        if original_verdict == Verdict.BLOCK and override_verdict == Verdict.ALLOW:
            self.memory["false_positives"].append(record)
            self.memory["statistics"]["false_positive_count"] += 1
        elif original_verdict == Verdict.ALLOW and override_verdict == Verdict.BLOCK:
            self.memory["false_negatives"].append(record)
            self.memory["statistics"]["false_negative_count"] += 1
        
        self._save_memory()
    
    def get_false_positive_rate(self) -> float:
        """
        Calculate false positive rate.
        
        Returns:
            False positive rate (0-1)
        """
        total_blocks = self.memory["statistics"]["total_blocks"]
        if total_blocks == 0:
            return 0.0
        
        false_positives = self.memory["statistics"]["false_positive_count"]
        return false_positives / total_blocks
    
    def get_false_negative_rate(self) -> float:
        """
        Calculate false negative rate.
        
        Returns:
            False negative rate (0-1)
        """
        total_allows = self.memory["statistics"].get("total_allows", 0)
        if total_allows == 0:
            return 0.0
        
        false_negatives = self.memory["statistics"]["false_negative_count"]
        return false_negatives / total_allows if total_allows > 0 else 0.0
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Get learning memory statistics.
        
        Returns:
            Dictionary with statistics
        """
        return {
            **self.memory["statistics"],
            "false_positive_rate": self.get_false_positive_rate(),
            "false_negative_rate": self.get_false_negative_rate(),
            "recent_blocks": len(self.memory["blocked_decisions"][-10:]),
            "recent_overrides": len(self.memory["human_overrides"][-10:])
        }






