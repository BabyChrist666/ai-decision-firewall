"""
Pytest tests for enterprise features.
"""
import pytest
import os
from adf.models import FirewallRequest, Verdict
from adf.firewall.interceptor import FirewallInterceptor
from adf.config import ENTERPRISE_MODE
from adf.audit.storage import AuditStorage
from adf.metrics.counters import MetricsCounter


@pytest.fixture
def firewall():
    """Fixture to provide a FirewallInterceptor instance."""
    return FirewallInterceptor()


@pytest.fixture
def enable_enterprise_mode(monkeypatch):
    """Fixture to enable enterprise mode for testing."""
    monkeypatch.setenv("ADF_ENTERPRISE_MODE", "true")
    # Reload config
    import importlib
    import adf.config
    importlib.reload(adf.config)
    yield
    monkeypatch.delenv("ADF_ENTERPRISE_MODE", raising=False)
    importlib.reload(adf.config)


def test_audit_logging_in_enterprise_mode(firewall, enable_enterprise_mode):
    """Test that audit logging works in enterprise mode."""
    request = FirewallRequest(
        ai_output="Test output for audit",
        confidence=0.8,
        intended_action="answer",
        sources=[]
    )
    
    response = firewall.check(request)
    
    # Check that audit log was created
    audit_storage = AuditStorage()
    stats = audit_storage.get_statistics()
    
    assert stats["total_decisions"] > 0, "Audit log should contain decisions"


def test_metrics_tracking(firewall):
    """Test that metrics are tracked."""
    request = FirewallRequest(
        ai_output="Test metrics",
        confidence=0.7,
        intended_action="answer",
        sources=[]
    )
    
    initial_metrics = firewall.metrics.get_metrics()
    initial_total = initial_metrics["total_requests"]
    
    response = firewall.check(request)
    
    updated_metrics = firewall.metrics.get_metrics()
    assert updated_metrics["total_requests"] == initial_total + 1
    assert updated_metrics["by_verdict"][response.verdict.value] > 0


def test_high_risk_requires_review_in_enterprise_mode(firewall, enable_enterprise_mode):
    """Test that high-risk decisions require review in enterprise mode."""
    request = FirewallRequest(
        ai_output="Execute high-value trade",
        confidence=0.3,  # Low confidence = high uncertainty
        intended_action="trade",  # High impact
        sources=[]
    )
    
    response = firewall.check(request)
    
    # In enterprise mode, high-risk should require review
    if response.risk_score >= 0.7:
        assert response.verdict in [Verdict.REQUIRE_HUMAN_REVIEW, Verdict.BLOCK], \
            "High-risk decisions should require review or be blocked in enterprise mode"






