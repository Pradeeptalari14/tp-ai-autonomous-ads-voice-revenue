"""
FinOps Unit Economics and Algorithmic Circuit Breakers
Calculates CPL, CAC, ROAS, and evaluates KEEP / KILL / SCALE decisions.
"""

from dataclasses import dataclass
from enum import Enum

class Verdict(str, Enum):
    SCALE = "SCALE"
    ITERATE = "ITERATE"
    KILL = "KILL"

@dataclass
class EconomicsReport:
    spend: float
    leads: int
    connected_calls: int
    qualified_deals: int
    revenue: float
    cpl: float
    cost_per_connected_call: float
    cac: float
    roas: float
    verdict: Verdict
    reason: str

class FinOpsCircuitBreaker:
    def __init__(self, target_cpl: float = 18.5, stop_loss_roas: float = 1.8):
        self.target_cpl = target_cpl
        self.stop_loss_roas = stop_loss_roas

    def evaluate(
        self,
        spend: float,
        leads: int,
        connected_calls: int,
        qualified_deals: int,
        revenue: float
    ) -> EconomicsReport:
        cpl = spend / max(leads, 1)
        cost_per_connected = spend / max(connected_calls, 1)
        cac = spend / max(qualified_deals, 1)
        roas = revenue / max(spend, 1.0)

        # 1. Stop-Loss Trigger Check
        if leads >= 5 and qualified_deals == 0 and spend > (self.target_cpl * 3.0):
            return EconomicsReport(
                spend=spend, leads=leads, connected_calls=connected_calls,
                qualified_deals=qualified_deals, revenue=revenue, cpl=cpl,
                cost_per_connected_call=cost_per_connected, cac=cac, roas=roas,
                verdict=Verdict.KILL,
                reason=f"Stop-Loss triggered: Spend (${spend:.2f}) > 3x Target CPL without any qualified calls."
            )

        # 2. Scale Trigger Check
        if roas >= (self.stop_loss_roas * 1.5) and cpl <= self.target_cpl:
            return EconomicsReport(
                spend=spend, leads=leads, connected_calls=connected_calls,
                qualified_deals=qualified_deals, revenue=revenue, cpl=cpl,
                cost_per_connected_call=cost_per_connected, cac=cac, roas=roas,
                verdict=Verdict.SCALE,
                reason=f"Scale triggered: ROAS ({roas:.2f}x) exceeds target by >50% with healthy CPL (${cpl:.2f})."
            )

        # 3. Iterate Baseline
        return EconomicsReport(
            spend=spend, leads=leads, connected_calls=connected_calls,
            qualified_deals=qualified_deals, revenue=revenue, cpl=cpl,
            cost_per_connected_call=cost_per_connected, cac=cac, roas=roas,
            verdict=Verdict.ITERATE,
            reason=f"Healthy baseline: ROAS ({roas:.2f}x) meets minimum threshold. Continue testing creative angles."
        )
