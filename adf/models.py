"""
Pydantic models for request and response schemas.
"""
from typing import List, Optional, Dict, Any
from enum import Enum
from pydantic import BaseModel, Field, field_validator


class IntendedAction(str, Enum):
    """Valid intended actions."""
    ANSWER = "answer"
    EMAIL = "email"
    TRADE = "trade"
    EXECUTE_CODE = "execute_code"


class Verdict(str, Enum):
    """Firewall verdict types."""
    ALLOW = "ALLOW"
    BLOCK = "BLOCK"
    REQUIRE_EVIDENCE = "REQUIRE_EVIDENCE"
    REQUIRE_HUMAN_REVIEW = "REQUIRE_HUMAN_REVIEW"


class FirewallRequest(BaseModel):
    """Request model for firewall check."""
    ai_output: str = Field(..., description="The AI-generated output to evaluate")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Confidence score (0-1)")
    intended_action: str = Field(..., description="Intended action type")
    sources: Optional[List[str]] = Field(default_factory=list, description="Optional list of source references")

    @field_validator("intended_action")
    @classmethod
    def validate_action(cls, v: str) -> str:
        """Validate intended action."""
        valid_actions = [action.value for action in IntendedAction]
        if v.lower() not in valid_actions:
            raise ValueError(f"intended_action must be one of {valid_actions}")
        return v.lower()


class Claim(BaseModel):
    """Represents an atomic factual claim."""
    text: str = Field(..., description="The claim text")
    is_factual: bool = Field(..., description="Whether this is a factual claim")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Confidence in this claim")


class CheckResult(BaseModel):
    """Result of a single check."""
    check_name: str = Field(..., description="Name of the check")
    passed: bool = Field(..., description="Whether the check passed")
    reason: str = Field(..., description="Reason for pass/fail")


class FirewallResponse(BaseModel):
    """Response model for firewall check."""
    verdict: Verdict = Field(..., description="Final verdict")
    reason: str = Field(..., description="Human-readable reason for verdict")
    risk_score: float = Field(..., ge=0.0, le=1.0, description="Overall risk score (0-1)")
    details: Dict[str, Any] = Field(
        default_factory=dict,
        description="Detailed breakdown of checks and analysis"
    )
    failed_checks: List[str] = Field(
        default_factory=list,
        description="List of failed check names"
    )
    explanation: str = Field(
        ...,
        description="Plain English explanation of the verdict"
    )
    confidence_alignment: bool = Field(
        ...,
        description="True if confidence matches evidence and claim characteristics"
    )
    applied_policies: List[str] = Field(
        default_factory=list,
        description="List of governance policies applied to this decision"
    )
    escalation_reason: Optional[str] = Field(
        default=None,
        description="Reason for escalation to human review (if applicable)"
    )

