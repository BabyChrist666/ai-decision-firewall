"""
Test for high-impact action policy fix.
Verifies that high-impact actions with low confidence or no evidence require human review.
"""
import pytest
from adf.models import FirewallRequest, Verdict
from adf.firewall.interceptor import FirewallInterceptor


@pytest.fixture
def firewall():
    """Fixture to provide a FirewallInterceptor instance."""
    return FirewallInterceptor()


def test_trade_action_low_confidence_no_evidence_requires_review(firewall):
    """
    Test the exact scenario from the bug report:
    - intended_action = "trade"
    - confidence = 0.45
    - no evidence provided
    - Expected: REQUIRE_HUMAN_REVIEW (not ALLOW)
    """
    request = FirewallRequest(
        ai_output="Execute trade: BUY 50,000 shares of AAPL at market price.",
        confidence=0.45,
        intended_action="trade",
        sources=[]
    )
    
    response = firewall.check(request)
    
    # Should require human review due to high-impact action policy
    assert response.verdict == Verdict.REQUIRE_HUMAN_REVIEW, \
        f"Expected REQUIRE_HUMAN_REVIEW, got {response.verdict.value}. " \
        f"Reason: {response.reason}, Explanation: {response.explanation}"
    
    assert "human_review_required" in response.failed_checks, \
        "Should have 'human_review_required' in failed_checks"
    
    assert "high-impact" in response.explanation.lower() or "human review" in response.explanation.lower(), \
        f"Explanation should mention high-impact action or human review. Got: {response.explanation}"


def test_trade_action_high_confidence_with_evidence_allowed(firewall):
    """
    Test that trade action with high confidence AND evidence can be allowed.
    """
    request = FirewallRequest(
        ai_output="Execute trade: BUY 1000 shares of AAPL based on verified market analysis.",
        confidence=0.85,  # Above 0.8 threshold
        intended_action="trade",
        sources=[
            "https://example.com/market-analysis",
            "https://example.com/technical-indicators"
        ]
    )
    
    response = firewall.check(request)
    
    # With high confidence (>=0.8) AND evidence, should not trigger high-impact rule
    # May still require review based on risk, but not due to high-impact policy
    assert response.verdict in [Verdict.ALLOW, Verdict.REQUIRE_HUMAN_REVIEW], \
        f"Should be ALLOW or REQUIRE_HUMAN_REVIEW, got {response.verdict.value}"
    
    # Should NOT have human_review_required due to high-impact policy
    # (may have it for other reasons like risk)
    if "human_review_required" in response.failed_checks:
        # If present, it should be for risk reasons, not high-impact policy
        assert response.risk_score >= 0.6, \
            "If human_review_required, should be due to risk, not high-impact policy"


def test_execute_code_low_confidence_requires_review(firewall):
    """
    Test that execute_code action with low confidence requires review.
    """
    request = FirewallRequest(
        ai_output="Execute Python script to process data",
        confidence=0.5,  # Below 0.8 threshold
        intended_action="execute_code",
        sources=[]
    )
    
    response = firewall.check(request)
    
    assert response.verdict == Verdict.REQUIRE_HUMAN_REVIEW, \
        f"Expected REQUIRE_HUMAN_REVIEW for execute_code with low confidence, got {response.verdict.value}"
    
    assert "human_review_required" in response.failed_checks, \
        "Should have 'human_review_required' in failed_checks"


def test_answer_action_not_affected_by_high_impact_policy(firewall):
    """
    Test that non-high-impact actions (like "answer") are not affected by this policy.
    """
    request = FirewallRequest(
        ai_output="Hello, how can I help you?",
        confidence=0.5,
        intended_action="answer",
        sources=[]
    )
    
    response = firewall.check(request)
    
    # Answer action should not trigger high-impact policy
    # Should be ALLOW (low risk, non-factual)
    assert response.verdict == Verdict.ALLOW, \
        f"Answer action should not be affected by high-impact policy, got {response.verdict.value}"
    
    assert "human_review_required" not in response.failed_checks, \
        "Answer action should not have human_review_required"






