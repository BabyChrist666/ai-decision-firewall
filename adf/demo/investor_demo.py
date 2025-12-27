"""
Investor demo script showcasing AI Decision Firewall capabilities.
Run with: python -m adf.demo.investor_demo
"""
from ..models import FirewallRequest, Verdict
from ..firewall.interceptor import FirewallInterceptor


def print_separator():
    """Print visual separator."""
    print("\n" + "="*70 + "\n")


def print_scenario_header(scenario_num: int, title: str):
    """Print scenario header."""
    print(f"SCENARIO {scenario_num}: {title}")
    print("-" * 70)


def print_result(request: FirewallRequest, response, scenario_title: str):
    """Print formatted result."""
    print(f"\n📊 {scenario_title}")
    print(f"Input: {request.ai_output[:80]}...")
    print(f"Confidence: {request.confidence}")
    print(f"Action: {request.intended_action}")
    print(f"Sources: {len(request.sources) if request.sources else 0}")
    
    print(f"\n✅ Verdict: {response.verdict.value}")
    print(f"📈 Risk Score: {response.risk_score:.3f}")
    print(f"🔍 Failed Checks: {response.failed_checks if response.failed_checks else 'None'}")
    print(f"⚖️  Confidence Alignment: {response.confidence_alignment}")
    print(f"\n💡 Explanation:\n   {response.explanation}")


def run_demo():
    """Run the investor demo."""
    firewall = FirewallInterceptor()
    
    print_separator()
    print("🚀 AI DECISION FIREWALL - INVESTOR DEMO")
    print_separator()
    print("Demonstrating runtime enforcement of AI outputs")
    print("Preventing hallucinations, enforcing evidence, escalating risk")
    print_separator()
    
    # Scenario 1: Hallucinated fact → BLOCKED
    print_scenario_header(1, "Hallucinated Fact → BLOCKED")
    request1 = FirewallRequest(
        ai_output="The Eiffel Tower was built in 1889 and is located in London, England.",
        confidence=0.92,
        intended_action="answer",
        sources=[]
    )
    response1 = firewall.check(request1)
    print_result(request1, response1, "Hallucination Detection")
    assert response1.verdict == Verdict.BLOCK or response1.verdict == Verdict.REQUIRE_EVIDENCE, \
        "Expected BLOCK or REQUIRE_EVIDENCE for hallucination"
    
    print_separator()
    
    # Scenario 2: High-risk trade → HUMAN REVIEW
    print_scenario_header(2, "High-Risk Trade → HUMAN REVIEW")
    request2 = FirewallRequest(
        ai_output="Execute trade: BUY 50,000 shares of AAPL at market price. "
                  "Based on technical analysis, the stock is expected to rise 15% in the next week.",
        confidence=0.45,
        intended_action="trade",
        sources=[]
    )
    response2 = firewall.check(request2)
    print_result(request2, response2, "High-Risk Action Escalation")
    assert response2.verdict == Verdict.REQUIRE_HUMAN_REVIEW, \
        "Expected REQUIRE_HUMAN_REVIEW for high-risk trade"
    
    print_separator()
    
    # Scenario 3: Grounded answer → ALLOWED
    print_scenario_header(3, "Grounded Answer → ALLOWED")
    request3 = FirewallRequest(
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
    response3 = firewall.check(request3)
    print_result(request3, response3, "Grounded Response")
    assert response3.verdict == Verdict.ALLOW, "Expected ALLOW for grounded answer with sources"
    
    print_separator()
    
    # Summary
    print("📋 DEMO SUMMARY")
    print("-" * 70)
    print(f"Scenario 1: {response1.verdict.value} - Hallucination prevented")
    print(f"Scenario 2: {response2.verdict.value} - Risk escalated to human")
    print(f"Scenario 3: {response3.verdict.value} - Grounded answer approved")
    print_separator()
    print("✨ Key Features Demonstrated:")
    print("   • Evidence enforcement for high-confidence claims")
    print("   • Risk-based escalation for high-impact actions")
    print("   • Explainable decisions with clear reasoning")
    print("   • Confidence-evidence alignment validation")
    print_separator()
    print("🎯 ADF protects against:")
    print("   • Hallucinations and ungrounded claims")
    print("   • Overconfident predictions without evidence")
    print("   • High-risk actions without proper safeguards")
    print("   • Confidence misalignment with claim characteristics")
    print_separator()


if __name__ == "__main__":
    run_demo()

