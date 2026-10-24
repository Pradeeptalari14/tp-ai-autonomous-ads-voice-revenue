"""
FastAPI Ingestion Webhook & Telephony Disposition Gateway
Handles Meta Instant Lead Form webhooks and post-call disposition signals.
"""

from fastapi import FastAPI, Request, BackgroundTasks, HTTPException
from pydantic import BaseModel, Field
import asyncio
from typing import Dict, Any, Optional

app = FastAPI(
    title="Autonomous AI Ads -> Voice Revenue Gateway",
    version="1.0.0",
    description="Sub-30s Lead Ingestion and Outbound Telephony Dispatch"
)

class LeadPayload(BaseModel):
    lead_id: str
    name: str
    phone: str
    campaign_id: str
    ad_id: str

class DispositionPayload(BaseModel):
    call_id: str
    lead_id: str
    connected: bool
    qualified: bool
    intent_score: int # 0 to 100
    appointment_booked: bool
    estimated_deal_value: float = 0.0
    summary: Optional[str] = None

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "lead-voice-gateway"}

@app.post("/api/v1/meta/leads")
async def handle_meta_lead(payload: LeadPayload, bg_tasks: BackgroundTasks):
    """Captures Meta lead form event and schedules instant voice dispatch."""
    print(f"[WEBHOOK] Inbound Lead Captured: #{payload.lead_id} ({payload.name}, {payload.phone})")
    bg_tasks.add_task(dispatch_outbound_call, payload)
    return {
        "status": "queued",
        "lead_id": payload.lead_id,
        "dispatch_target_latency_ms": 320
    }

async def dispatch_outbound_call(lead: LeadPayload):
    """Simulates immediate telephony dispatch via OmniDimension / LiveKit / Twilio SIP."""
    print(f"[VOICE] Initiating low-latency call to {lead.phone}...")
    await asyncio.sleep(0.3)
    print(f"[VOICE] Call connected for Lead #{lead.lead_id}. Awaiting disposition webhook.")

@app.post("/api/v1/telephony/disposition")
async def handle_call_disposition(payload: DispositionPayload):
    """Processes post-call structured outcomes to recalculate unit economics."""
    print(f"[DISPOSITION] Call #{payload.call_id} Concluded: Qualified={payload.qualified}, Booked={payload.appointment_booked}")
    return {
        "status": "acknowledged",
        "reinvestment_signal_sent": True
    }
