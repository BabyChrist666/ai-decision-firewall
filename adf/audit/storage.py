"""
Storage utilities for audit logs.
"""
from pathlib import Path
from typing import List, Dict, Any
import json
from datetime import datetime
from .logger import AuditLogger


class AuditStorage:
    """Manages audit log storage and retrieval."""
    
    def __init__(self, log_file: str = None):
        """
        Initialize audit storage.
        
        Args:
            log_file: Optional custom log file path
        """
        self.logger = AuditLogger(log_file)
    
    def store_decision(
        self,
        request: "FirewallRequest",
        response: "FirewallResponse",
        metadata: Dict[str, Any] = None
    ) -> None:
        """
        Store a firewall decision.
        
        Args:
            request: Firewall request
            response: Firewall response
            metadata: Optional metadata
        """
        self.logger.log_decision(request, response, metadata)
    
    def query_by_verdict(self, verdict: str, limit: int = 100) -> List[Dict[str, Any]]:
        """
        Query audit logs by verdict.
        
        Args:
            verdict: Verdict to filter by
            limit: Maximum number of results
            
        Returns:
            List of matching audit records
        """
        all_logs = self.logger.read_logs(limit=None)
        filtered = [log for log in all_logs if log.get("verdict") == verdict]
        return filtered[:limit]
    
    def query_by_action(self, action: str, limit: int = 100) -> List[Dict[str, Any]]:
        """
        Query audit logs by intended action.
        
        Args:
            action: Action to filter by
            limit: Maximum number of results
            
        Returns:
            List of matching audit records
        """
        all_logs = self.logger.read_logs(limit=None)
        filtered = [log for log in all_logs if log.get("intended_action") == action]
        return filtered[:limit]
    
    def query_high_risk(self, min_risk: float = 0.7, limit: int = 100) -> List[Dict[str, Any]]:
        """
        Query high-risk decisions.
        
        Args:
            min_risk: Minimum risk score
            limit: Maximum number of results
            
        Returns:
            List of matching audit records
        """
        all_logs = self.logger.read_logs(limit=None)
        filtered = [log for log in all_logs if log.get("risk_score", 0.0) >= min_risk]
        return filtered[:limit]
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Get audit statistics.
        
        Returns:
            Dictionary with statistics
        """
        return self.logger.get_stats()






