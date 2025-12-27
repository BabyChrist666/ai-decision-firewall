"""
Evidence and grounding checks.
"""
from typing import List, Optional
from ..models import Claim
from ..config import CONFIDENCE_THRESHOLD_EVIDENCE_REQUIRED
from ..utils.logger import logger


class EvidenceChecker:
    """Checks for evidence and grounding of claims."""
    
    def __init__(self):
        """Initialize evidence checker."""
        self.evidence_threshold = CONFIDENCE_THRESHOLD_EVIDENCE_REQUIRED
    
    def check_evidence(
        self,
        claims: List[Claim],
        sources: Optional[List[str]] = None
    ) -> tuple[bool, str, List[str]]:
        """
        Check if factual claims have evidence.
        
        Args:
            claims: List of claims to check
            sources: Optional list of source references
            
        Returns:
            Tuple of (has_evidence, reason, failed_claims)
        """
        if sources is None:
            sources = []
        
        # Filter to factual claims with high confidence
        high_confidence_factual = [
            c for c in claims
            if c.is_factual and c.confidence > self.evidence_threshold
        ]
        
        if not high_confidence_factual:
            return True, "No high-confidence factual claims requiring evidence", []
        
        # Check if sources are provided
        has_sources = len(sources) > 0
        
        if not has_sources:
            failed_claims = [c.text for c in high_confidence_factual]
            return False, "High confidence factual claims require evidence but no sources provided", failed_claims
        
        # Basic validation: sources should be non-empty
        valid_sources = [s for s in sources if s and s.strip()]
        
        if not valid_sources:
            failed_claims = [c.text for c in high_confidence_factual]
            return False, "Sources provided but all are empty", failed_claims
        
        # Check if number of sources is reasonable for number of claims
        # Rule: at least one source per 3 factual claims
        min_sources = max(1, len(high_confidence_factual) // 3)
        
        if len(valid_sources) < min_sources:
            failed_claims = [c.text for c in high_confidence_factual]
            return False, f"Insufficient sources: {len(valid_sources)} provided, {min_sources} required for {len(high_confidence_factual)} factual claims", failed_claims
        
        return True, f"Evidence check passed: {len(valid_sources)} sources for {len(high_confidence_factual)} factual claims", []
    
    def validate_source_quality(self, sources: List[str]) -> tuple[bool, str]:
        """
        Validate the quality of provided sources.
        
        Args:
            sources: List of source strings
            
        Returns:
            Tuple of (is_valid, reason)
        """
        if not sources:
            return True, "No sources to validate"
        
        # Check for empty sources
        empty_count = sum(1 for s in sources if not s or not s.strip())
        if empty_count > 0:
            return False, f"{empty_count} empty source(s) detected"
        
        # Check for minimum length (sources should be meaningful)
        too_short = [s for s in sources if len(s.strip()) < 5]
        if too_short:
            return False, f"{len(too_short)} source(s) are too short to be meaningful"
        
        return True, "Source quality validated"






