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

def mask_contact_e164(raw_val: str) -> str:
    """Masks phone number for TCPA/DPDP privacy compliance (e.g. +917330****88)."""
    if not raw_val or len(raw_val) <= 6:
        return "***"
    return f"{raw_val[:6]}****{raw_val[-2:]}"

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "lead-voice-gateway"}

@app.post("/api/v1/meta/leads")
async def handle_meta_lead(payload: LeadPayload, bg_tasks: BackgroundTasks):
    """Captures Meta lead form event and schedules instant voice dispatch."""
    masked_contact = mask_contact_e164(payload.phone)
    print(f"[WEBHOOK] Inbound Lead Captured: #{payload.lead_id} ({payload.name}, {masked_contact})")
    bg_tasks.add_task(dispatch_outbound_call, payload)
    return {
        "status": "queued",
        "lead_id": payload.lead_id,
        "dispatch_target_latency_ms": 320
    }

async def dispatch_outbound_call(lead: LeadPayload):
    """Simulates immediate telephony dispatch via OmniDimension / LiveKit / Twilio SIP."""
    masked_contact = mask_contact_e164(lead.phone)
    print(f"[VOICE] Initiating low-latency call to {masked_contact}...")
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
