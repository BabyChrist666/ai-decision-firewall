"""
Immutable audit logging for firewall decisions.
"""
import json
import hashlib
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional
from ..models import FirewallRequest, FirewallResponse
from ..config import AUDIT_LOG_DIR, AUDIT_LOG_FILE, ENTERPRISE_MODE
from ..utils.logger import logger


class AuditLogger:
    """Handles immutable audit logging of firewall decisions."""
    
    def __init__(self, log_file: Optional[str] = None):
        """
        Initialize audit logger.
        
        Args:
            log_file: Optional custom log file path
        """
        self.log_file = log_file or AUDIT_LOG_FILE
        self._ensure_log_directory()
    
    def _ensure_log_directory(self) -> None:
        """Ensure audit log directory exists."""
        log_path = Path(self.log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)
    
    def _hash_output(self, ai_output: str) -> str:
        """
        Generate hash of AI output for tamper detection.
        
        Args:
            ai_output: The AI output text
            
        Returns:
            SHA256 hash of the output
        """
        return hashlib.sha256(ai_output.encode('utf-8')).hexdigest()
    
    def log_decision(
        self,
        request: FirewallRequest,
        response: FirewallResponse,
        metadata: Optional[Dict[str, Any]] = None
    ) -> None:
        """
        Log a firewall decision to the audit log.
        
        Args:
            request: Original firewall request
            response: Firewall response
            metadata: Optional additional metadata
        """
        if not ENTERPRISE_MODE:
            return
        
        try:
            audit_record = {
                "timestamp": datetime.utcnow().isoformat() + "Z",
                "ai_output_hash": self._hash_output(request.ai_output),
                "ai_output_length": len(request.ai_output),
                "confidence": request.confidence,
                "intended_action": request.intended_action,
                "verdict": response.verdict.value,
                "risk_score": response.risk_score,
                "failed_checks": response.failed_checks,
                "explanation": response.explanation,
                "confidence_alignment": response.confidence_alignment,
                "sources_count": len(request.sources) if request.sources else 0,
                "metadata": metadata or {}
            }
            
            # Append-only write
            with open(self.log_file, 'a', encoding='utf-8') as f:
                f.write(json.dumps(audit_record) + '\n')
            
            logger.debug(f"Audit log entry written: {response.verdict.value}")
        
        except Exception as e:
            logger.error(f"Failed to write audit log: {str(e)}", exc_info=True)
    
    def read_logs(self, limit: Optional[int] = None) -> list[Dict[str, Any]]:
        """
        Read audit logs.
        
        Args:
            limit: Optional limit on number of records to return
            
        Returns:
            List of audit records
        """
        if not Path(self.log_file).exists():
            return []
        
        records = []
        try:
            with open(self.log_file, 'r', encoding='utf-8') as f:
                for line in f:
                    if line.strip():
                        records.append(json.loads(line))
                        if limit and len(records) >= limit:
                            break
        except Exception as e:
            logger.error(f"Failed to read audit logs: {str(e)}", exc_info=True)
        
        return records
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Get statistics from audit logs.
        
        Returns:
            Dictionary with audit statistics
        """
        records = self.read_logs()
        if not records:
            return {
                "total_decisions": 0,
                "by_verdict": {},
                "by_action": {},
                "avg_risk_score": 0.0
            }
        
        verdict_counts = {}
        action_counts = {}
        risk_scores = []
        
        for record in records:
            verdict = record.get("verdict", "UNKNOWN")
            verdict_counts[verdict] = verdict_counts.get(verdict, 0) + 1
            
            action = record.get("intended_action", "UNKNOWN")
            action_counts[action] = action_counts.get(action, 0) + 1
            
            risk_scores.append(record.get("risk_score", 0.0))
        
        return {
            "total_decisions": len(records),
            "by_verdict": verdict_counts,
            "by_action": action_counts,
            "avg_risk_score": sum(risk_scores) / len(risk_scores) if risk_scores else 0.0,
            "min_risk_score": min(risk_scores) if risk_scores else 0.0,
            "max_risk_score": max(risk_scores) if risk_scores else 0.0
        }






