"""
Metrics counters for tracking firewall statistics.
"""
import json
from pathlib import Path
from typing import Dict, Any
from datetime import datetime
from ..config import METRICS_STORAGE_DIR, METRICS_FILE
from ..models import Verdict
from ..utils.logger import logger


class MetricsCounter:
    """Tracks and stores firewall metrics."""
    
    def __init__(self, metrics_file: str = None):
        """
        Initialize metrics counter.
        
        Args:
            metrics_file: Optional custom metrics file path
        """
        self.metrics_file = metrics_file or METRICS_FILE
        self._ensure_metrics_directory()
        self.metrics = self._load_metrics()
    
    def _ensure_metrics_directory(self) -> None:
        """Ensure metrics directory exists."""
        metrics_path = Path(self.metrics_file)
        metrics_path.parent.mkdir(parents=True, exist_ok=True)
    
    def _load_metrics(self) -> Dict[str, Any]:
        """
        Load metrics from disk.
        
        Returns:
            Metrics dictionary
        """
        if not Path(self.metrics_file).exists():
            return {
                "total_requests": 0,
                "blocked_requests": 0,
                "allowed_requests": 0,
                "hallucination_blocks": 0,
                "human_reviews": 0,
                "evidence_required": 0,
                "by_verdict": {},
                "by_action": {},
                "last_updated": None
            }
        
        try:
            with open(self.metrics_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Failed to load metrics: {str(e)}", exc_info=True)
            return {
                "total_requests": 0,
                "blocked_requests": 0,
                "allowed_requests": 0,
                "hallucination_blocks": 0,
                "human_reviews": 0,
                "evidence_required": 0,
                "by_verdict": {},
                "by_action": {},
                "last_updated": None
            }
    
    def _save_metrics(self) -> None:
        """Save metrics to disk."""
        try:
            self.metrics["last_updated"] = datetime.utcnow().isoformat() + "Z"
            with open(self.metrics_file, 'w', encoding='utf-8') as f:
                json.dump(self.metrics, f, indent=2)
        except Exception as e:
            logger.error(f"Failed to save metrics: {str(e)}", exc_info=True)
    
    def record_request(
        self,
        verdict: Verdict,
        intended_action: str,
        is_hallucination: bool = False
    ) -> None:
        """
        Record a firewall request.
        
        Args:
            verdict: Final verdict
            intended_action: Intended action type
            is_hallucination: Whether this was a hallucination block
        """
        self.metrics["total_requests"] += 1
        
        # Update verdict counts
        verdict_key = verdict.value
        self.metrics["by_verdict"][verdict_key] = self.metrics["by_verdict"].get(verdict_key, 0) + 1
        
        # Update action counts
        self.metrics["by_action"][intended_action] = self.metrics["by_action"].get(intended_action, 0) + 1
        
        # Update specific counters
        if verdict == Verdict.BLOCK:
            self.metrics["blocked_requests"] += 1
            if is_hallucination:
                self.metrics["hallucination_blocks"] += 1
        elif verdict == Verdict.ALLOW:
            self.metrics["allowed_requests"] += 1
        elif verdict == Verdict.REQUIRE_HUMAN_REVIEW:
            self.metrics["human_reviews"] += 1
        elif verdict == Verdict.REQUIRE_EVIDENCE:
            self.metrics["evidence_required"] += 1
        
        self._save_metrics()
    
    def get_metrics(self) -> Dict[str, Any]:
        """
        Get current metrics.
        
        Returns:
            Dictionary with all metrics
        """
        total = self.metrics["total_requests"]
        if total == 0:
            return {**self.metrics, "block_rate": 0.0, "allow_rate": 0.0}
        
        return {
            **self.metrics,
            "block_rate": self.metrics["blocked_requests"] / total,
            "allow_rate": self.metrics["allowed_requests"] / total,
            "hallucination_rate": self.metrics["hallucination_blocks"] / total if total > 0 else 0.0,
            "human_review_rate": self.metrics["human_reviews"] / total if total > 0 else 0.0
        }
    
    def reset(self) -> None:
        """Reset all metrics."""
        self.metrics = {
            "total_requests": 0,
            "blocked_requests": 0,
            "allowed_requests": 0,
            "hallucination_blocks": 0,
            "human_reviews": 0,
            "evidence_required": 0,
            "by_verdict": {},
            "by_action": {},
            "last_updated": None
        }
        self._save_metrics()






