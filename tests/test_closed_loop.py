"""
Unit test suite for Autonomous Ads-to-Voice Revenue closed loop.
"""

import pytest
import sys
import os

# Include src directory
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from economics import FinOpsCircuitBreaker, Verdict
from orchestrator import ClosedLoopOrchestrator

def test_circuit_breaker_scale():
    cb = FinOpsCircuitBreaker(target_cpl=20.0, stop_loss_roas=2.0)
    # High revenue, low CPL
    report = cb.evaluate(spend=100.0, leads=10, connected_calls=8, qualified_deals=2, revenue=800.0)
    assert report.verdict == Verdict.SCALE
    assert report.roas == 8.0
    assert report.cpl == 10.0

def test_circuit_breaker_kill():
    cb = FinOpsCircuitBreaker(target_cpl=20.0, stop_loss_roas=2.0)
    # Exceeded 3x Target CPL without a single qualified deal
    report = cb.evaluate(spend=80.0, leads=6, connected_calls=4, qualified_deals=0, revenue=0.0)
    assert report.verdict == Verdict.KILL
    assert report.roas == 0.0

def test_circuit_breaker_iterate():
    cb = FinOpsCircuitBreaker(target_cpl=20.0, stop_loss_roas=2.0)
    # Acceptable ROAS, but above target CPL
    report = cb.evaluate(spend=100.0, leads=4, connected_calls=3, qualified_deals=1, revenue=220.0)
    assert report.verdict == Verdict.ITERATE

@pytest.mark.asyncio
async def test_orchestrator_cycle():
    orchestrator = ClosedLoopOrchestrator(daily_budget=100.0, target_cpl=15.0, stop_loss_roas=1.5)
    result = await orchestrator.simulate_48h_cycle()
    assert "roas" in result
    assert result["spend"] == 200.0
    assert result["verdict"] in ["SCALE", "ITERATE", "KILL"]
