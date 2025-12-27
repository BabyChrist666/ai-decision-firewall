"""
Configuration settings for AI Decision Firewall.
"""
from typing import Dict
import os

# Enterprise mode
ENTERPRISE_MODE: bool = os.getenv("ADF_ENTERPRISE_MODE", "False").lower() == "true"

# Audit log settings
AUDIT_LOG_DIR = os.getenv("ADF_AUDIT_LOG_DIR", "./audit_logs")
AUDIT_LOG_FILE = os.path.join(AUDIT_LOG_DIR, "firewall_audit.jsonl")

# Learning/memory settings
MEMORY_STORAGE_DIR = os.getenv("ADF_MEMORY_DIR", "./memory")
MEMORY_FILE = os.path.join(MEMORY_STORAGE_DIR, "learning_memory.json")

# Metrics settings
METRICS_STORAGE_DIR = os.getenv("ADF_METRICS_DIR", "./metrics")
METRICS_FILE = os.path.join(METRICS_STORAGE_DIR, "metrics.json")

# Confidence thresholds
CONFIDENCE_THRESHOLD_EVIDENCE_REQUIRED = 0.6
CONFIDENCE_THRESHOLD_HIGH = 0.8
CONFIDENCE_THRESHOLD_LOW = 0.3

# Action impact levels (0-1 scale)
ACTION_IMPACT: Dict[str, float] = {
    "answer": 0.2,      # Low impact
    "email": 0.5,       # Medium impact
    "trade": 0.9,       # High impact
    "execute_code": 0.95,  # Very high impact
}

# Risk thresholds
RISK_THRESHOLD_LOW = 0.3
RISK_THRESHOLD_MEDIUM = 0.6
RISK_THRESHOLD_HIGH = 0.8

# Default action impact if not specified
DEFAULT_ACTION_IMPACT = 0.5

# Learning parameters
LEARNING_ENABLED = True
ADAPTIVE_STRICTNESS = True
MIN_FALSE_POSITIVES_FOR_RELAX = 10
MIN_FALSE_NEGATIVES_FOR_STRICT = 5

