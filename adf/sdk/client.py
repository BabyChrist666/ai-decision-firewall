"""
Python SDK client for AI Decision Firewall.
"""
from typing import Callable, Any, Optional, List
from functools import wraps
from ..models import FirewallRequest, FirewallResponse, Verdict
from ..firewall.interceptor import FirewallInterceptor
from ..utils.logger import logger


class FirewallClient:
    """Python SDK client for firewall integration."""
    
    def __init__(self, interceptor: Optional[FirewallInterceptor] = None):
        """
        Initialize firewall client.
        
        Args:
            interceptor: Optional firewall interceptor instance
        """
        self.interceptor = interceptor or FirewallInterceptor()
    
    def check(
        self,
        ai_output: str,
        confidence: float,
        intended_action: str,
        sources: Optional[List[str]] = None
    ) -> FirewallResponse:
        """
        Check AI output through firewall.
        
        Args:
            ai_output: AI-generated output
            confidence: Confidence score (0-1)
            intended_action: Intended action type
            sources: Optional list of sources
            
        Returns:
            Firewall response
        """
        request = FirewallRequest(
            ai_output=ai_output,
            confidence=confidence,
            intended_action=intended_action,
            sources=sources or []
        )
        
        return self.interceptor.check(request)
    
    def is_allowed(
        self,
        ai_output: str,
        confidence: float,
        intended_action: str,
        sources: Optional[List[str]] = None
    ) -> bool:
        """
        Check if AI output is allowed (convenience method).
        
        Args:
            ai_output: AI-generated output
            confidence: Confidence score (0-1)
            intended_action: Intended action type
            sources: Optional list of sources
            
        Returns:
            True if allowed, False otherwise
        """
        response = self.check(ai_output, confidence, intended_action, sources)
        return response.verdict == Verdict.ALLOW


# Global client instance
_default_client = None


def get_client() -> FirewallClient:
    """
    Get default firewall client instance.
    
    Returns:
        Firewall client
    """
    global _default_client
    if _default_client is None:
        _default_client = FirewallClient()
    return _default_client


def firewalled(
    intended_action: str,
    confidence: Optional[float] = None,
    sources: Optional[List[str]] = None,
    raise_on_block: bool = False
):
    """
    Decorator to firewall-protect a function that returns AI output.
    
    Args:
        intended_action: Intended action type
        confidence: Optional confidence score (if not provided, function should return tuple)
        sources: Optional list of sources
        raise_on_block: Whether to raise exception on block (default: return None)
        
    Returns:
        Decorated function
        
    Example:
        @firewalled(intended_action="trade")
        def ai_decision():
            return llm_output, 0.9, ["source1", "source2"]
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            client = get_client()
            
            # Call original function
            result = func(*args, **kwargs)
            
            # Handle different return formats
            if isinstance(result, tuple) and len(result) >= 2:
                # Function returns (output, confidence, ...)
                ai_output = result[0]
                func_confidence = result[1] if len(result) > 1 else confidence
                func_sources = result[2] if len(result) > 2 else sources
            else:
                # Function returns just output
                if confidence is None:
                    raise ValueError("confidence must be provided if function doesn't return it")
                ai_output = result
                func_confidence = confidence
                func_sources = sources or []
            
            # Check through firewall
            response = client.check(
                ai_output=ai_output,
                confidence=func_confidence,
                intended_action=intended_action,
                sources=func_sources
            )
            
            # Handle verdict
            if response.verdict == Verdict.ALLOW:
                return result
            elif response.verdict == Verdict.BLOCK:
                logger.warning(f"Firewall blocked execution: {response.explanation}")
                if raise_on_block:
                    raise RuntimeError(f"Firewall blocked: {response.explanation}")
                return None
            elif response.verdict == Verdict.REQUIRE_HUMAN_REVIEW:
                logger.warning(f"Firewall requires human review: {response.explanation}")
                if raise_on_block:
                    raise RuntimeError(f"Firewall requires review: {response.explanation}")
                return None
            elif response.verdict == Verdict.REQUIRE_EVIDENCE:
                logger.warning(f"Firewall requires evidence: {response.explanation}")
                if raise_on_block:
                    raise RuntimeError(f"Firewall requires evidence: {response.explanation}")
                return None
            
            return result
        
        return wrapper
    return decorator






