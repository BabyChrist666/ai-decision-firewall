# AI Decision Firewall (ADF)

**Runtime Governance and Policy Enforcement for AI Systems**

AI Decision Firewall is an enterprise-grade runtime enforcement layer that sits between AI systems and real-world actions. ADF intercepts AI-generated outputs before execution and evaluates them against governance rules, evidence requirements, risk thresholds, and compliance policies. It provides deterministic verdicts that determine whether AI outputs may proceed, require additional evidence, escalate to human review, or must be blocked.

---

## Problem Statement

AI systems in production face critical challenges that traditional monitoring and post-hoc analysis cannot address:

**Hallucinations and Ungrounded Claims**
AI models often express high confidence in factual claims without providing supporting evidence. These outputs propagate misinformation and erode trust when deployed in production systems.

**Overconfident Predictions**
AI systems may assign high confidence scores to speculative or uncertain outputs, creating false certainty that leads to poor decision-making.

**High-Risk Autonomous Actions**
AI systems executing financial trades, medical recommendations, legal advice, or code execution without human oversight present unacceptable risks to organizations and end users.

**Lack of Auditability**
Most AI systems operate as black boxes, providing no explanation for decisions and no immutable audit trail for compliance and regulatory requirements.

ADF addresses these problems by enforcing governance rules at runtime, before AI outputs execute real-world actions.

---

## What ADF Does

ADF intercepts AI outputs and evaluates them across multiple dimensions:

1. **Evidence Validation**: Requires supporting sources for high-confidence factual claims
2. **Confidence Alignment**: Validates that confidence scores match the characteristics of claims
3. **Risk Assessment**: Calculates risk scores based on confidence, action impact, and evidence presence
4. **Policy Enforcement**: Applies governance rules that cannot be bypassed (e.g., all trades require human review)
5. **Safety Rules**: Blocks unsafe patterns, contradictions, and harmful actions

ADF returns deterministic verdicts:

- **ALLOW**: Output may proceed; all checks passed and risk is acceptable
- **REQUIRE_EVIDENCE**: Evidence must be provided before proceeding
- **REQUIRE_HUMAN_REVIEW**: Human approval required before proceeding (mandatory for certain actions)
- **BLOCK**: Output violates safety rules and cannot proceed

---

## Architecture Overview

```
┌─────────────────┐
│   AI System     │
│  (LLM/Model)    │
└────────┬────────┘
         │
         │ AI Output + Metadata
         │ (confidence, action, sources)
         │
         ▼
┌─────────────────────────────────────┐
│      AI Decision Firewall (ADF)     │
│                                      │
│  ┌──────────────────────────────┐  │
│  │  Policy Manager              │  │
│  │  (Governance Rules)          │  │
│  └────────────┬─────────────────┘  │
│               │                     │
│  ┌────────────▼─────────────────┐  │
│  │  Firewall Interceptor        │  │
│  │  - Claim Parser              │  │
│  │  - Evidence Checker          │  │
│  │  - Confidence Validator      │  │
│  │  - Risk Scorer               │  │
│  │  - Rules Engine              │  │
│  │  - Verdict Engine            │  │
│  └────────────┬─────────────────┘  │
│               │                     │
│  ┌────────────▼─────────────────┐  │
│  │  Audit & Metrics             │  │
│  │  - Immutable Logs            │  │
│  │  - Decision Tracking         │  │
│  └──────────────────────────────┘  │
└────────────┬────────────────────────┘
             │
             │ Verdict + Explanation
             │
         ┌───┴────┐
         │        │
    ┌────▼───┐ ┌─▼────────┐
    │ ALLOW  │ │ ESCALATE │
    │        │ │ / BLOCK  │
    └────────┘ └──────────┘
         │            │
         ▼            ▼
    ┌────────────────────┐
    │  Real-World Action │
    │  (if allowed)      │
    └────────────────────┘
```

---

## Governance and Policy Modes

ADF enforces governance rules that cannot be bypassed by confidence scores, evidence presence, or risk calculations. These rules define mandatory human review requirements for specific action types.

**GENERAL_AI Mode**
Default policy mode with conservative defaults. Requires human review for financial trades and code execution actions.

**FINANCIAL_SERVICES Mode**
All financial trades require mandatory human review. This requirement cannot be overridden regardless of confidence, evidence, or risk score. Stricter evidence thresholds and lower risk tolerance.

**HEALTHCARE Mode**
Medical actions require mandatory human review. Highest evidence requirements and strictest risk enforcement for healthcare applications.

**LEGAL Mode**
Legal actions require mandatory human review. Highest evidence requirements and strictest risk enforcement for legal applications.

Policy modes are set via API and apply to all firewall evaluations:

```python
POST /policy/mode
{
  "mode": "FINANCIAL_SERVICES"
}
```

---

## Quick Start

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Installation

```bash
# Clone the repository
git clone <repository-url>
cd ai-decision-firewall

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Start the API Server

```bash
# Run with uvicorn
uvicorn adf.main:app --reload --host 0.0.0.0 --port 8000

# Or use Python module
python -m adf.main
```

### Verify Installation

Access the API documentation at:
- Interactive API docs: http://localhost:8000/docs
- Alternative docs: http://localhost:8000/redoc

Test the health endpoint:
```bash
curl http://localhost:8000/health
```

---

## Key API Endpoints

### POST /firewall/check

Main endpoint for evaluating AI outputs. Returns a verdict with explanation.

**Request:**
```json
{
  "ai_output": "Apple was founded in 1976",
  "confidence": 0.92,
  "intended_action": "answer",
  "sources": []
}
```

**Response:**
```json
{
  "verdict": "REQUIRE_HUMAN_REVIEW",
  "reason": "Governance rule: trade actions require mandatory human review",
  "risk_score": 0.75,
  "explanation": "This trade action requires mandatory human review due to governance policy...",
  "applied_policies": ["mandatory_governance_review"],
  "escalation_reason": "Governance rule: trade actions require mandatory human review in FINANCIAL_SERVICES policy mode",
  "confidence_alignment": false,
  "failed_checks": ["governance_mandatory_review"],
  "details": {
    "claims": [...],
    "risk_level": "high",
    "checks": {...}
  }
}
```

### POST /policy/mode

Set the governance policy mode for all firewall evaluations.

**Request:**
```json
{
  "mode": "FINANCIAL_SERVICES"
}
```

**Response:**
```json
{
  "status": "success",
  "message": "Policy mode set to FINANCIAL_SERVICES",
  "policy": {
    "mode": "FINANCIAL_SERVICES",
    "mandatory_review_actions": ["trade", "execute_code"],
    "confidence_threshold_evidence_required": 0.7,
    "risk_threshold_medium": 0.5,
    "description": "Financial services compliance - all trades require human review"
  }
}
```

### GET /policy/mode

Get the current policy mode configuration.

### GET /audit/logs

Query audit logs for compliance and analysis. Requires enterprise mode.

**Query Parameters:**
- `limit`: Maximum number of records (1-1000, default: 100)
- `verdict`: Filter by verdict type
- `action`: Filter by intended action

### GET /metrics

Get firewall statistics including request counts, block rates, and verdict distributions.

### POST /demo/run

Execute predefined demo scenarios for testing and demonstration.

---

## Dashboard (Demo and Visualization)

The repository includes `adf_dashboard.html`, a self-contained HTML dashboard that visualizes ADF's governance decisions. This dashboard is intended for:

- Demonstration and visualization of ADF capabilities
- Testing and experimentation
- Understanding verdict explanations and risk scores

The dashboard is not required for production use. Production deployments should integrate ADF via the API or Python SDK.

To use the dashboard:
1. Start the ADF API server (see Quick Start)
2. Open `adf_dashboard.html` in a web browser
3. Submit simulated AI outputs to see governance verdicts

---

## Python SDK Usage

### Basic Usage

```python
from adf.sdk import FirewallClient

client = FirewallClient()

response = client.check(
    ai_output="Execute trade: BUY 1000 shares of AAPL",
    confidence=0.9,
    intended_action="trade",
    sources=["https://analysis.com/report"]
)

if response.verdict == "ALLOW":
    # Proceed with action
    execute_trade(response.ai_output)
elif response.verdict == "REQUIRE_HUMAN_REVIEW":
    # Escalate to human
    escalate_for_review(response)
else:
    # Block or require evidence
    handle_blocked_output(response)
```

### Decorator Pattern

```python
from adf.sdk import firewalled

@firewalled(intended_action="trade", raise_on_block=True)
def execute_trading_strategy():
    # Your AI model generates output
    ai_output = llm.generate("Should I buy AAPL?")
    confidence = 0.85
    sources = ["https://financial-analysis.com/report"]
    
    return ai_output, confidence, sources

try:
    result = execute_trading_strategy()
    # Only executes if ADF allows
except RuntimeError as e:
    # ADF blocked the output
    print(f"Governance decision: {e}")
```

---

## Target Audience

AI Decision Firewall is designed for:

**Enterprises**
Organizations deploying AI systems that require governance, auditability, and risk management before AI outputs execute real-world actions.

**Regulated Industries**
Financial services, healthcare, legal, and other industries with compliance requirements that mandate human oversight and immutable audit trails.

**AI Product Teams**
Engineering teams building AI-powered products that need runtime enforcement of safety rules, evidence requirements, and policy compliance.

---

## Enterprise Features

**Audit Logging**
Immutable JSONL audit logs capture all governance decisions with timestamps, verdicts, risk scores, and explanations. Enterprise mode enables tamper-resistant logging suitable for compliance requirements.

**Metrics and Analytics**
Track governance decisions, block rates, evidence requirements, and human review escalations. Monitor system performance and policy effectiveness over time.

**Self-Learning**
ADF tracks false positives and false negatives from human overrides, enabling adaptive threshold tuning without code changes.

**Policy Modes**
Industry-specific governance profiles with non-bypassable rules for financial services, healthcare, legal, and general AI use cases.

---

## Configuration

ADF configuration is managed through environment variables and the `adf/config.py` file:

**Environment Variables:**
- `ADF_ENTERPRISE_MODE`: Enable enterprise features (audit logging, enhanced metrics)
- `ADF_AUDIT_LOG_DIR`: Directory for audit log storage
- `ADF_MEMORY_DIR`: Directory for learning memory storage
- `ADF_METRICS_DIR`: Directory for metrics storage

**Configuration File:**
Edit `adf/config.py` to adjust confidence thresholds, risk thresholds, action impact levels, and learning parameters.

---

## Testing

Run the test suite:

```bash
pytest test_example.py test_enterprise.py test_governance_rules.py -v
```

Key test coverage:
- Governance rules enforcement (trade actions always require review)
- Evidence requirements for high-confidence claims
- Risk-based escalation
- Policy mode configurations
- Audit logging in enterprise mode

---

## License

[Specify your license here]

---

## Support and Contributing

For questions, issues, or contributions, please [provide contact information or contribution guidelines].

---

**AI must be governed, not just optimized. ADF provides the runtime enforcement layer that enterprises need to deploy AI systems safely, accountably, and in compliance with regulatory requirements.**