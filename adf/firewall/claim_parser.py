"""
Parses AI output into atomic factual claims.
"""
import re
from typing import List
from ..models import Claim
from ..utils.logger import logger


class ClaimParser:
    """Parses text into atomic factual claims."""
    
    # Patterns to identify factual claims
    FACTUAL_PATTERNS = [
        r'\b(?:was|were|is|are|has|have|had)\s+(?:founded|created|established|invented|discovered|made|built)',
        r'\b(?:in|on|at|during)\s+\d{4}',  # Dates
        r'\b(?:founded|created|established|invented|discovered)\s+(?:in|on|at)',
        r'\b(?:makes|produces|manufactures|sells|owns)',
        r'\b(?:according to|based on|per|as stated in)',
        r'\b(?:the|a|an)\s+\w+\s+(?:is|was|are|were)',
    ]
    
    # Sentence delimiters
    SENTENCE_DELIMITERS = r'[.!?]+(?:\s+|$)'
    
    def __init__(self):
        """Initialize the claim parser."""
        self.factual_regex = re.compile(
            '|'.join(self.FACTUAL_PATTERNS),
            re.IGNORECASE
        )
    
    def parse(self, text: str, overall_confidence: float) -> List[Claim]:
        """
        Parse text into atomic claims.
        
        Args:
            text: The AI output text
            overall_confidence: Overall confidence score from the request
            
        Returns:
            List of Claim objects
        """
        if not text or not text.strip():
            logger.warning("Empty text provided to claim parser")
            return []
        
        # Split into sentences
        sentences = re.split(self.SENTENCE_DELIMITERS, text)
        sentences = [s.strip() for s in sentences if s.strip()]
        
        claims = []
        for sentence in sentences:
            if not sentence:
                continue
            
            # Check if sentence contains factual patterns
            is_factual = bool(self.factual_regex.search(sentence))
            
            # For now, use overall confidence for each claim
            # In a more sophisticated version, we could analyze each claim separately
            claim_confidence = overall_confidence
            
            # Additional heuristics for factual detection
            if not is_factual:
                # Check for numbers (often indicate facts)
                if re.search(r'\d+', sentence):
                    is_factual = True
            
            # Skip very short sentences (likely not claims)
            if len(sentence.split()) < 3:
                continue
            
            claim = Claim(
                text=sentence,
                is_factual=is_factual,
                confidence=claim_confidence
            )
            claims.append(claim)
        
        logger.info(f"Parsed {len(claims)} claims from text (factual: {sum(1 for c in claims if c.is_factual)})")
        return claims
    
    def is_factual_claim(self, text: str) -> bool:
        """
        Check if a text segment is likely a factual claim.
        
        Args:
            text: Text to check
            
        Returns:
            True if likely factual
        """
        return bool(self.factual_regex.search(text))






