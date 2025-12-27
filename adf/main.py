"""
FastAPI entry point for AI Decision Firewall.
"""
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field
from .models import FirewallRequest, FirewallResponse, Verdict
from .firewall.interceptor import FirewallInterceptor
from .audit.storage import AuditStorage
from .metrics.counters import MetricsCounter
from .metrics.benchmark import HallucinationBenchmark
from .learning.memory import LearningMemory
from .compliance.policy import PolicyMode, get_policy_manager, set_policy_mode
from .utils.logger import logger

# Initialize FastAPI app
app = FastAPI(
    title="AI Decision Firewall",
    description="Runtime enforcement layer for LLM outputs",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize firewall interceptor
firewall = FirewallInterceptor()

# Initialize enterprise components
audit_storage = AuditStorage()
metrics_counter = MetricsCounter()
learning_memory = LearningMemory()


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "service": "AI Decision Firewall",
        "version": "1.0.0",
        "status": "operational"
    }


@app.get("/health")
async def health():
    """Health check endpoint."""
    return {"status": "healthy"}


@app.post("/firewall/check", response_model=FirewallResponse)
async def check_firewall(request: FirewallRequest) -> FirewallResponse:
    """
    Main firewall check endpoint.
    
    Evaluates AI output against evidence, confidence, rules, and risk thresholds.
    
    Args:
        request: Firewall request with AI output and metadata
        
    Returns:
        Firewall response with verdict and analysis
    """
    try:
        logger.info(f"Received firewall check request: action={request.intended_action}")
        
        # Process through firewall
        response = firewall.check(request)
        
        return response
    
    except ValueError as e:
        logger.error(f"Validation error: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@app.get("/metrics")
async def get_metrics() -> Dict[str, Any]:
    """
    Get firewall metrics.
    
    Returns:
        Dictionary with metrics statistics
    """
    return metrics_counter.get_metrics()


@app.get("/audit/logs")
async def get_audit_logs(
    limit: int = Query(100, ge=1, le=1000),
    verdict: Optional[str] = None,
    action: Optional[str] = None
) -> Dict[str, Any]:
    """
    Get audit logs.
    
    Args:
        limit: Maximum number of records to return
        verdict: Optional filter by verdict
        action: Optional filter by action
        
    Returns:
        Dictionary with audit logs
    """
    if verdict:
        logs = audit_storage.query_by_verdict(verdict, limit=limit)
    elif action:
        logs = audit_storage.query_by_action(action, limit=limit)
    else:
        logs = audit_storage.logger.read_logs(limit=limit)
    
    return {
        "count": len(logs),
        "logs": logs
    }


@app.get("/audit/stats")
async def get_audit_stats() -> Dict[str, Any]:
    """
    Get audit statistics.
    
    Returns:
        Dictionary with audit statistics
    """
    return audit_storage.get_statistics()


class PolicyUpdateRequest(BaseModel):
    """Request model for policy update."""
    override_verdict: str
    original_verdict: str
    reason: str
    request_id: Optional[str] = None


@app.post("/policy/update")
async def update_policy(update: PolicyUpdateRequest) -> Dict[str, Any]:
    """
    Record a human policy override for learning.
    
    Args:
        update: Policy update request
        
    Returns:
        Confirmation message
    """
    try:
        original = Verdict(update.original_verdict)
        override = Verdict(update.override_verdict)
        
        learning_memory.record_human_override(
            original_verdict=original,
            override_verdict=override,
            reason=update.reason
        )
        
        return {
            "status": "success",
            "message": "Policy override recorded",
            "learning_stats": learning_memory.get_statistics()
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid verdict: {str(e)}")


class PolicyModeRequest(BaseModel):
    """Request model for policy mode selection."""
    mode: str = Field(..., description="Policy mode: GENERAL_AI, FINANCIAL_SERVICES, HEALTHCARE, LEGAL")


@app.post("/policy/mode")
async def set_policy_mode_endpoint(request: PolicyModeRequest) -> Dict[str, Any]:
    """
    Set the governance policy mode.
    
    Policy modes define which actions require mandatory human review.
    This is a governance setting that affects all firewall checks.
    
    Args:
        request: Policy mode request
        
    Returns:
        Current policy configuration
    """
    try:
        mode = PolicyMode(request.mode.upper())
        set_policy_mode(mode)
        policy_manager = get_policy_manager()
        
        return {
            "status": "success",
            "message": f"Policy mode set to {mode.value}",
            "policy": policy_manager.get_policy_info()
        }
    except ValueError:
        valid_modes = [mode.value for mode in PolicyMode]
        raise HTTPException(
            status_code=400,
            detail=f"Invalid policy mode. Must be one of: {', '.join(valid_modes)}"
        )


@app.get("/policy/mode")
async def get_policy_mode() -> Dict[str, Any]:
    """
    Get the current governance policy mode configuration.
    
    Returns:
        Current policy configuration
    """
    policy_manager = get_policy_manager()
    return {
        "status": "success",
        "policy": policy_manager.get_policy_info()
    }


@app.post("/demo/run")
async def run_demo() -> Dict[str, Any]:
    """
    Run investor demo scenarios.
    
    Returns:
        Demo results
    """
    try:
        from .demo.investor_demo import run_demo as run_demo_func
        import io
        import sys
        
        # Capture demo output
        old_stdout = sys.stdout
        sys.stdout = captured_output = io.StringIO()
        
        try:
            run_demo_func()
            output = captured_output.getvalue()
        finally:
            sys.stdout = old_stdout
        
        return {
            "status": "success",
            "output": output,
            "message": "Demo completed successfully"
        }
    except Exception as e:
        logger.error(f"Demo execution failed: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Demo failed: {str(e)}")


@app.get("/learning/stats")
async def get_learning_stats() -> Dict[str, Any]:
    """
    Get learning memory statistics.
    
    Returns:
        Dictionary with learning statistics
    """
    return learning_memory.get_statistics()


@app.post("/benchmark/run")
async def run_benchmark() -> Dict[str, Any]:
    """
    Run hallucination detection benchmark.
    
    Returns:
        Benchmark results
    """
    benchmark = HallucinationBenchmark(firewall)
    results = benchmark.run_benchmark()
    return results


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

