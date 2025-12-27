"""
Test that governance rules are properly enforced.

CRITICAL TEST: Trade actions must ALWAYS require human review,
regardless of confidence, evidence, or risk score.
"""
import pytest
from adf.models import FirewallRequest
from adf.firewall.interceptor import FirewallInterceptor
from adf.compliance.policy import set_policy_mode, PolicyMode, get_policy_manager
from adf.models import Verdict


@pytest.fixture
def firewall():
    """Fixture to provide a FirewallInterceptor instance."""
    return FirewallInterceptor()


def test_trade_action_always_requires_human_review_regardless_of_confidence(firewall):
    """
    CRITICAL TEST: Trade action with high confidence, evidence, low risk
    must STILL require human review due to governance rules.
    
    This test validates that governance rules override all other factors.
    """
    # Set to FINANCIAL_SERVICES mode (strictest trade enforcement)
    set_policy_mode(PolicyMode.FINANCIAL_SERVICES)
    
    request = FirewallRequest(
        ai_output="Execute trade: BUY 10000 shares of AAPL. Market analysis suggests strong growth potential.",
        confidence=0.95,  # Very high confidence
        intended_action="trade",  # Trade action
        sources=["https://financial-analysis.com/report"]  # Evidence provided
    )
    
    response = firewall.check(request)
    
    # CRITICAL ASSERTION: Must require human review regardless of confidence/evidence
    assert response.verdict == Verdict.REQUIRE_HUMAN_REVIEW, \
        f"Expected REQUIRE_HUMAN_REVIEW, got {response.verdict.value}. " \
        f"This indicates governance rules are not being enforced. " \
        f"Reason: {response.reason}, Explanation: {response.explanation}"
    
    # Verify governance rule was applied
    assert "governance_mandatory_review" in response.failed_checks or "mandatory_governance_review" in response.applied_policies, \
        f"Governance rule not applied. Failed checks: {response.failed_checks}, Applied policies: {response.applied_policies}"
    
    # Verify escalation reason explains governance rule
    assert response.escalation_reason is not None, \
        "Escalation reason should explain governance rule requirement"
    assert "governance" in response.escalation_reason.lower() or "mandatory" in response.escalation_reason.lower(), \
        f"Escalation reason should mention governance: {response.escalation_reason}"


def test_trade_action_in_general_mode_also_requires_review(firewall):
    """
    Even in GENERAL_AI mode, trade actions should require human review.
    """
    set_policy_mode(PolicyMode.GENERAL_AI)
    
    request = FirewallRequest(
        ai_output="Buy 5000 shares of TSLA",
        confidence=0.99,  # Maximum confidence
        intended_action="trade",
        sources=["https://example.com/analysis"]  # Evidence provided
    )
    
    response = firewall.check(request)
    
    # Trade actions require review even in general mode
    assert response.verdict == Verdict.REQUIRE_HUMAN_REVIEW, \
        f"Expected REQUIRE_HUMAN_REVIEW for trade action, got {response.verdict.value}"


def test_governance_rules_override_risk_scoring(firewall):
    """
    Governance rules must override risk scoring.
    
    Even if risk score is very low, governance rules still apply.
    """
    set_policy_mode(PolicyMode.FINANCIAL_SERVICES)
    
    request = FirewallRequest(
        ai_output="Small trade: BUY 10 shares of a stable ETF",
        confidence=0.50,  # Medium confidence
        intended_action="trade",
        sources=["https://market-data.com/etf-info"]  # Evidence
    )
    
    response = firewall.check(request)
    
    # Must require review regardless of risk score
    assert response.verdict == Verdict.REQUIRE_HUMAN_REVIEW, \
        f"Governance rules must override risk scoring. " \
        f"Got verdict: {response.verdict.value}, Risk score: {response.risk_score}"


def test_answer_action_not_blocked_by_governance(firewall):
    """
    Non-governed actions (like "answer") should not be blocked by governance rules.
    """
    set_policy_mode(PolicyMode.GENERAL_AI)
    
    request = FirewallRequest(
        ai_output="Apple was founded in 1976",
        confidence=0.85,
        intended_action="answer",
        sources=["https://www.apple.com/about/"]  # Evidence provided
    )
    
    response = firewall.check(request)
    
    # Answer actions are not subject to mandatory governance review
    # Should be allowed if evidence is provided and risk is low
    assert response.verdict != Verdict.BLOCK, \
        f"Answer action with evidence should not be blocked. Got: {response.verdict.value}"


def test_governance_policy_modes(firewall):
    """
    Test that different policy modes enforce appropriate governance rules.
    """
    # Test FINANCIAL_SERVICES mode
    set_policy_mode(PolicyMode.FINANCIAL_SERVICES)
    policy_manager = get_policy_manager()
    assert "trade" in policy_manager.mandatory_review_actions, \
        "FINANCIAL_SERVICES mode must include trade in mandatory review actions"
    
    # Test GENERAL_AI mode
    set_policy_mode(PolicyMode.GENERAL_AI)
    policy_manager = get_policy_manager()
    assert "trade" in policy_manager.mandatory_review_actions, \
        "GENERAL_AI mode should also require trade review"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])


