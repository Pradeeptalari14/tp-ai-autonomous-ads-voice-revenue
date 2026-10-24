"""
Autonomous Growth & Revenue Closed-Loop Orchestrator
"""

import os
import sys
import asyncio
from typing import Dict, Any
from datetime import datetime

# Local imports
try:
    from .economics import FinOpsCircuitBreaker, Verdict
except ImportError:
    from economics import FinOpsCircuitBreaker, Verdict

class ClosedLoopOrchestrator:
    def __init__(self, daily_budget: float = 150.0, target_cpl: float = 18.5, stop_loss_roas: float = 1.8):
        self.daily_budget = daily_budget
        self.circuit_breaker = FinOpsCircuitBreaker(target_cpl=target_cpl, stop_loss_roas=stop_loss_roas)

    def generate_campaign_brief(self, niche: str) -> Dict[str, Any]:
        """Synthesizes high-converting hooks and 9:16 safe-zone creative angles."""
        return {
            "niche": niche,
            "daily_cap_usd": self.daily_budget,
            "creative_angles": [
                {
                    "angle": "Pain & SRE Vulnerability",
                    "hook": "Are your cloud bills doubling because unmonitored LLM agents are caught in recursive loops?",
                    "format": "9:16 Vertical Reel"
                },
                {
                    "angle": "Mechanism & Uptime",
                    "hook": "How to achieve 99.95% LLM uptime and cut token latency by 40% using vLLM PagedAttention.",
                    "format": "9:16 Vertical Reel"
                }
            ],
            "cta": "Claim Instant 15-Minute Senior AI Architecture Review"
        }

    async def simulate_48h_cycle(self) -> Dict[str, Any]:
        """Simulates complete cold impression to closed revenue closed loop."""
        print(f"[ORCHESTRATOR] Starting 48-hour closed-loop test with daily budget ${self.daily_budget:.2f}...")
        total_spend = self.daily_budget * 2.0
        leads = 18
        connected = 15
        qualified = 4
        revenue = qualified * 2400.0 # B2B AI consulting deal value

        report = self.circuit_breaker.evaluate(
            spend=total_spend,
            leads=leads,
            connected_calls=connected,
            qualified_deals=qualified,
            revenue=revenue
        )

        print("\n--- 48-HOUR CLOSED-LOOP REPORT ---")
        print(f"Total Ad Spend:      ${report.spend:.2f}")
        print(f"Leads Captured:      {report.leads} (CPL: ${report.cpl:.2f})")
        print(f"Calls Connected:     {report.connected_calls} (Cost/Connect: ${report.cost_per_connected_call:.2f})")
        print(f"Deals Converted:     {report.qualified_deals} (CAC: ${report.cac:.2f})")
        print(f"Total Gross Revenue: ${report.revenue:.2f}")
        print(f"Observed ROAS:       {report.roas:.2f}x")
        print(f"Algorithmic Action:  [{report.verdict.value}] - {report.reason}\n")

        return {
            "spend": report.spend,
            "leads": report.leads,
            "deals": report.qualified_deals,
            "roas": report.roas,
            "verdict": report.verdict.value
        }

if __name__ == "__main__":
    orchestrator = ClosedLoopOrchestrator(daily_budget=150.0, target_cpl=18.5, stop_loss_roas=1.8)
    brief = orchestrator.generate_campaign_brief("b2b_ai_consulting")
    print(f"Brief Created: {brief['cta']}")
    asyncio.run(orchestrator.simulate_48h_cycle())
