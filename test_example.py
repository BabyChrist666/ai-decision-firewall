"""
Pytest-based tests for AI Decision Firewall.
Run with: pytest test_example.py
"""
import pytest
from adf.models import FirewallRequest, Verdict
from adf.firewall.interceptor import FirewallInterceptor


@pytest.fixture
def firewall():
    """Fixture to provide a FirewallInterceptor instance."""
    return FirewallInterceptor()


def test_high_confidence_factual_claim_without_evidence_should_block(firewall):
    """
    Test 1: High confidence factual claim without evidence → BLOCK
    
    A high confidence (0.9) factual claim about a company founding date
    without sources should be blocked.
    """
    request = FirewallRequest(
        ai_output="Apple was founded in 1976 and makes the iPhone",
        confidence=0.9,
        intended_action="answer",
        sources=[]
    )
    
    response = firewall.check(request)
    
    # Assertions
    assert response.verdict == Verdict.BLOCK, f"Expected BLOCK, got {response.verdict.value}"
    assert "evidence" in response.failed_checks, "Evidence check should have failed"
    assert response.confidence_alignment is not None, "Confidence alignment should be set"
    assert len(response.explanation) > 0, "Explanation should be provided"
    assert "confidence" in response.explanation.lower() or "evidence" in response.explanation.lower(), \
        "Explanation should mention confidence or evidence"


def test_low_confidence_speculative_claim_should_allow(firewall):
    """
    Test 2: Low confidence speculative claim → ALLOW
    
    A low confidence (0.3) speculative/non-factual statement should be allowed
    as it doesn't make strong factual claims.
    """
    request = FirewallRequest(
        ai_output="I think the market might go up next week, but I'm not sure.",
        confidence=0.3,
        intended_action="answer",
        sources=[]
    )
    
    response = firewall.check(request)
    
    # Assertions
    assert response.verdict == Verdict.ALLOW, f"Expected ALLOW, got {response.verdict.value}"
    assert response.risk_score < 0.5, f"Risk score should be low, got {response.risk_score}"
    assert len(response.explanation) > 0, "Explanation should be provided"
    assert response.confidence_alignment is not None, "Confidence alignment should be set"


def test_high_confidence_claim_with_sources_should_allow(firewall):
    """
    Test 3: High confidence claim with sources → ALLOW
    
    A high confidence (0.9) factual claim with proper sources should be allowed.
    """
    request = FirewallRequest(
        ai_output="Apple was founded in 1976 and makes the iPhone",
        confidence=0.9,
        intended_action="answer",
        sources=[
            "https://www.apple.com/about/",
            "https://en.wikipedia.org/wiki/Apple_Inc.",
            "https://www.britannica.com/topic/Apple-Inc"
        ]
    )
    
    response = firewall.check(request)
    
    # Assertions
    assert response.verdict == Verdict.ALLOW, f"Expected ALLOW, got {response.verdict.value}"
    assert "evidence" not in response.failed_checks, "Evidence check should have passed"
    assert response.details.get("sources", {}).get("count", 0) > 0, "Sources should be present in details"
    assert response.confidence_alignment is not None, "Confidence alignment should be set"
    assert len(response.explanation) > 0, "Explanation should be provided"


def test_high_risk_action_with_uncertainty_should_require_human_review(firewall):
    """
    Test 4: High-risk action with uncertainty → REQUIRE_HUMAN_REVIEW
    
    A high-impact action (trade) with low confidence (high uncertainty) 
    should require human review due to risk score exceeding medium threshold.
    """
    request = FirewallRequest(
        ai_output="Execute trade: BUY 10000 shares of AAPL based on technical analysis. "
                  "The stock price has been volatile recently. Market conditions suggest caution.",
        confidence=0.35,  # Low confidence = high uncertainty (0.65)
        intended_action="trade",  # High-impact action (0.9 impact)
        sources=[]
    )
    
    response = firewall.check(request)
    
    # Assertions
    # For trade actions with medium+ risk, should require human review
    assert response.verdict == Verdict.REQUIRE_HUMAN_REVIEW, \
        f"Expected REQUIRE_HUMAN_REVIEW, got {response.verdict.value}. " \
        f"Risk score: {response.risk_score:.3f}, Reason: {response.reason}, " \
        f"Explanation: {response.explanation}"
    assert response.risk_score >= 0.3, \
        f"Risk score should be medium or higher for trade action, got {response.risk_score}"
    assert len(response.explanation) > 0, "Explanation should be provided"
    assert "human" in response.explanation.lower() or "review" in response.explanation.lower(), \
        f"Explanation should mention human review. Got: {response.explanation}"
    assert response.confidence_alignment is not None, "Confidence alignment should be set"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
