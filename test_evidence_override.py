"""
Test for evidence override rule fix.
Verifies that confidence_alignment does not block when evidence is present.
"""
import pytest
from adf.models import FirewallRequest, Verdict
from adf.firewall.interceptor import FirewallInterceptor


@pytest.fixture
def firewall():
    """Fixture to provide a FirewallInterceptor instance."""
    return FirewallInterceptor()


def test_grounded_answer_with_sources_should_allow(firewall):
    """
    Test Scenario 3: Grounded answer with sources should be ALLOWED
    even if confidence_alignment is false.
    """
    request = FirewallRequest(
        ai_output="Python was created by Guido van Rossum and first released in 1991. "
                  "It is an interpreted, high-level programming language.",
        confidence=0.95,
        intended_action="answer",
        sources=[
            "https://www.python.org/about/",
            "https://en.wikipedia.org/wiki/Python_(programming_language)",
            "https://docs.python.org/3/tutorial/introduction.html"
        ]
    )
    
    response = firewall.check(request)
    
    # Should be ALLOWED because evidence exists (evidence override rule)
    assert response.verdict == Verdict.ALLOW, \
        f"Expected ALLOW for grounded answer with sources, got {response.verdict.value}. " \
        f"Reason: {response.reason}, Explanation: {response.explanation}"
    
    # confidence_alignment should NOT be in failed_checks when evidence exists
    assert "confidence_alignment" not in response.failed_checks, \
        "confidence_alignment should not be in failed_checks when evidence is present"
    
    # If confidence_alignment is false but evidence exists, explanation should mention override
    if not response.confidence_alignment:
        assert "evidence" in response.explanation.lower() or "despite" in response.explanation.lower(), \
            f"Explanation should mention evidence override. Got: {response.explanation}"


def test_confidence_alignment_blocks_when_no_evidence(firewall):
    """
    Test that confidence_alignment still blocks when evidence is missing.
    """
    request = FirewallRequest(
        ai_output="The company was founded in 2020",
        confidence=0.9,
        intended_action="answer",
        sources=[]  # No evidence
    )
    
    response = firewall.check(request)
    
    # Should be blocked or require evidence due to confidence alignment + no evidence
    assert response.verdict in [Verdict.BLOCK, Verdict.REQUIRE_EVIDENCE], \
        f"Expected BLOCK or REQUIRE_EVIDENCE when no evidence and confidence alignment issues, got {response.verdict.value}"
    
    # confidence_alignment should be in failed_checks when evidence is missing
    if not response.confidence_alignment:
        assert "confidence_alignment" in response.failed_checks or "evidence" in response.failed_checks, \
            "Should have confidence_alignment or evidence in failed_checks when evidence is missing"


def test_evidence_override_explanation(firewall):
    """
    Test that explanation mentions evidence override when applicable.
    """
    request = FirewallRequest(
        ai_output="Test output with evidence",
        confidence=0.95,
        intended_action="answer",
        sources=["https://example.com/source1", "https://example.com/source2"]
    )
    
    response = firewall.check(request)
    
    # If allowed and confidence_alignment is false, should mention evidence override
    if response.verdict == Verdict.ALLOW and not response.confidence_alignment:
        assert "evidence" in response.explanation.lower() or "despite" in response.explanation.lower(), \
            f"Should mention evidence override in explanation. Got: {response.explanation}"






