# AI Decision Firewall (ADF)

**Enterprise-Grade Runtime Governance for Artificial Intelligence**

ADF is a production-ready governance layer that sits between AI systems and real-world actions. ADF does NOT generate AI outputs—it **governs** whether AI outputs may proceed based on safety, evidence, and compliance requirements.

---

## 🎯 What ADF IS

ADF is a **runtime governance and enforcement system** that:

- ✅ **Evaluates** AI-generated outputs before they execute
- ✅ **Enforces** mandatory governance rules (e.g., trades require human review)
- ✅ **Validates** evidence requirements for high-confidence claims
- ✅ **Escalates** high-risk decisions to humans
- ✅ **Provides** explainable, auditable governance decisions
- ✅ **Learns** from past decisions to improve over time

## ❌ What ADF IS NOT

ADF is NOT:
- ❌ An AI model (it does not generate text, answers, or decisions)
- ❌ A replacement for human judgment
- ❌ A prompt engineering tool
- ❌ A risk scoring system without enforcement
- ❌ A post-hoc analysis tool

**ADF governs outputs—it does not generate them.**

---

## 🔒 Why ADF Exists

### The Problem: Unchecked AI Outputs

AI systems today suffer from critical failures:

1. **Hallucinations**: High-confidence factual claims without evidence
   - Example: "Apple was founded in 1976" (claimed with 95% confidence, no sources)

2. **Overconfidence**: Confidence scores that don't match reality
   - Example: 90% confidence on speculative claims presented as facts

3. **Risk Blindness**: High-impact actions executed without safeguards
   - Example: Automatic trading decisions, medical recommendations, legal advice

4. **Lack of Governance**: No enforcement layer between AI and real-world actions
   - Example: AI systems making financial trades without human oversight

### The Solution: Governance That Enforces

ADF provides **mandatory governance rules** that:

- **Never auto-approve** certain actions (trades, medical, legal) regardless of AI confidence
- **Require evidence** for high-confidence factual claims
- **Escalate** medium+ risk decisions to humans
- **Block** unsafe patterns and contradictions
- **Provide** explainable reasons for every decision

---

## 🏢 How Customers Use ADF

### Typical Integration Pattern

```python
from adf.sdk import firewalled

@firewalled(intended_action="trade")
def execute_trading_strategy():
    # Your AI model generates output
    ai_output = llm.generate("Should I buy AAPL?")
    confidence = 0.85
    sources = ["https://financial-analysis.com/report"]
    
    return ai_output, confidence, sources

# ADF automatically evaluates before execution
try:
    result = execute_trading_strategy()
    # Only executes if ADF allows
except RuntimeError as e:
    # ADF blocked the output
    print(f"Governance decision: {e}")
```

### Governance Workflow

1. **AI System** generates output (confidence, sources, intended action)
2. **ADF Evaluates** against governance rules:
   - Is evidence provided for high-confidence claims?
   - Does the intended action require mandatory human review?
   - What is the risk score?
   - Are there unsafe patterns?
3. **ADF Returns Verdict**:
   - `ALLOW`: Output may proceed
   - `REQUIRE_EVIDENCE`: Evidence must be provided
   - `REQUIRE_HUMAN_REVIEW`: Human must approve (mandatory for certain actions)
   - `BLOCK`: Output violates safety rules
4. **Your System** acts on the verdict

---

## 🛡️ What ADF Prevents

### 1. Unsafe Actions Without Oversight

**Problem**: AI systems executing high-impact actions automatically.

**ADF Solution**: Governance rules that **ALWAYS** require human review for:
- Financial trades
- Medical recommendations
- Legal advice
- Code execution
- User data deletion

**Example**:
```
Input: Action="trade", Confidence=0.95, Evidence=provided, Risk=0.2
ADF Verdict: REQUIRE_HUMAN_REVIEW
Reason: "Governance rule: trade actions require mandatory human review"
```

### 2. Hallucinated Facts

**Problem**: AI makes confident factual claims without evidence.

**ADF Solution**: Evidence requirements for high-confidence factual claims.

**Example**:
```
Input: "Apple was founded in 1976" (Confidence=0.92, Sources=[])
ADF Verdict: BLOCK
Reason: "High confidence factual claims without evidence"
```

### 3. Overconfidence on Ungrounded Claims

**Problem**: AI expresses high confidence on speculative or uncertain claims.

**ADF Solution**: Confidence-evidence alignment checks.

**Example**:
```
Input: "The market might go up" (Confidence=0.9, Sources=[])
ADF Verdict: REQUIRE_EVIDENCE
Reason: "Confidence (0.9) exceeds threshold for ungrounded claim"
```

### 4. High-Risk Decisions Without Review

**Problem**: Medium-high risk decisions auto-approved.

**ADF Solution**: Risk-based escalation to human review.

**Example**:
```
Input: Risk Score=0.65, Action="answer"
ADF Verdict: REQUIRE_HUMAN_REVIEW
Reason: "Risk score (0.65) exceeds medium threshold"
```

---

## 📊 Governance Policy Modes

ADF supports industry-specific governance profiles:

### GENERAL_AI (Default)
- Trades require human review
- Code execution requires human review
- Conservative evidence thresholds

### FINANCIAL_SERVICES
- **ALL trades require mandatory human review** (cannot be overridden)
- Stricter evidence requirements
- Lower risk thresholds

### HEALTHCARE
- Medical actions require human review
- Highest evidence thresholds
- Strictest risk enforcement

### LEGAL
- Legal actions require human review
- Highest evidence thresholds
- Strictest risk enforcement

### Setting Policy Mode

```python
# Via API
POST /policy/mode
{
  "mode": "FINANCIAL_SERVICES"
}

# Check current policy
GET /policy/mode
```

---

## 🔧 Installation & Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Start API server
python -m adf.main
# or
uvicorn adf.main:app --reload

# Run demo scenarios
python -m adf.demo.investor_demo

# Open dashboard (double-click)
# adf_dashboard.html
```

---

## 📡 API Endpoints

### Core Endpoint

**POST** `/firewall/check`

Evaluates AI output against governance rules.

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
  "failed_checks": ["governance_mandatory_review"]
}
```

### Policy Management

**GET** `/policy/mode` - Get current policy configuration

**POST** `/policy/mode` - Set policy mode
```json
{
  "mode": "FINANCIAL_SERVICES"
}
```

### Audit & Compliance

**GET** `/audit/logs` - Query audit logs

**GET** `/metrics` - Get governance statistics

---

## 🎨 Dashboard (Demo Mode)

Open `adf_dashboard.html` in your browser to see:

- **Governance Input**: Submit simulated AI outputs for evaluation
- **Demo Scenarios**: Pre-configured examples (Hallucinated Fact, High-Risk Trade, Grounded Answer)
- **Governance Verdict**: Color-coded decision with explanation
- **Applied Policies**: Which governance rules were triggered
- **System Log**: Real-time governance decisions

**Note**: The dashboard is for demonstration and testing. Production use should integrate via API/SDK.

---

## 🔐 Governance Rules (Non-Negotiable)

ADF enforces these rules **regardless** of confidence, evidence, or risk scores:

1. **Trade actions** → ALWAYS require human review
2. **Medical actions** → ALWAYS require human review (Healthcare mode)
3. **Legal actions** → ALWAYS require human review (Legal mode)
4. **Code execution** → ALWAYS require human review
5. **Unsafe patterns** → ALWAYS blocked
6. **High-confidence factual claims without evidence** → Blocked or evidence required

These rules **cannot be overridden** by:
- High confidence scores
- Presence of evidence
- Low risk scores
- Manual configuration

---

## 📈 Enterprise Features

### Audit Logging (Enterprise Mode)

Enable with environment variable:
```bash
export ADF_ENTERPRISE_MODE=true
```

Features:
- Immutable JSONL audit logs
- All decisions logged with hashes
- Tamper-resistant storage
- Compliance-ready audit trail

### Self-Learning

ADF learns from past decisions:
- Tracks false positives (humans override blocks)
- Tracks false negatives (humans block allowed outputs)
- Adapts thresholds based on performance
- No code changes required—only parameter tuning

---

## 🧪 Testing & Validation

### Critical Test Case

**Scenario**: Trade action with high confidence, evidence provided, low risk score

```
Input:
  - Action: "trade"
  - Confidence: 0.95
  - Evidence: provided
  - Risk Score: 0.2

Expected Verdict: REQUIRE_HUMAN_REVIEW

Reason: Governance rule enforcement (trade actions always require human review)
```

This test **must pass** to ensure governance rules are properly enforced.

---

## 🚀 SDK Usage

```python
from adf.sdk import FirewallClient

client = FirewallClient()

response = client.check(
    ai_output="Buy 1000 shares of AAPL",
    confidence=0.9,
    intended_action="trade",
    sources=["https://analysis.com/report"]
)

if response.verdict == "ALLOW":
    print("Output approved!")
elif response.verdict == "REQUIRE_HUMAN_REVIEW":
    print(f"Human review required: {response.explanation}")
else:
    print(f"Blocked: {response.explanation}")
```

---

## 📚 Additional Resources

- **Dashboard**: `adf_dashboard.html` (double-click to open)
- **Demo Scenarios**: `python -m adf.demo.investor_demo`
- **API Documentation**: http://127.0.0.1:8000/docs (when server is running)

---

## ⚖️ Compliance & Governance

ADF is designed for enterprises that need:

- **Regulatory Compliance**: Audit trails, mandatory review workflows
- **Risk Management**: Governance before execution, not after
- **Explainability**: Plain English reasons for every decision
- **Determinism**: Same input → same output (auditable)
- **Non-Bypassable Rules**: Governance rules that cannot be overridden

---

## 📝 License

[Your License Here]

---

## 🤝 Support

For questions, issues, or contributions, please [contact information].

---

**Remember**: ADF governs AI outputs—it does not generate them. ADF ensures that AI systems operate within governance boundaries before they execute real-world actions.