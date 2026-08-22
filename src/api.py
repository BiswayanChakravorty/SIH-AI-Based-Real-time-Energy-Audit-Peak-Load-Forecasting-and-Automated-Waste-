"""FastAPI service for real-time energy telemetry."""
from __future__ import annotations

from collections import deque
from datetime import datetime, timezone
from pathlib import Path
import sys

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

sys.path.append(str(Path(__file__).resolve().parent))
from iot_gateway import IoTTelemetryGateway
from ML_engine import EnergyMLCore
from automation import AutomationSwitchController

app = FastAPI(title="EcoPulse IoT Gateway", version="1.0.0")
gateway = IoTTelemetryGateway()
ml = EnergyMLCore()
telemetry_buffer = deque(maxlen=200)


class TelemetryIn(BaseModel):
    device_id: str = Field(min_length=1)
    generation_kw: float = Field(ge=0)
    demand_kw: float = Field(ge=0)
    voltage_v: float = Field(default=230, gt=0)
    current_a: float = Field(default=0, ge=0)
    power_factor: float = Field(default=0.95, gt=0, le=1)
    temperature_c: float = 30
    thermal_waste_c: float = Field(default=20, ge=0)
    timestamp: str | None = None


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "ecopulse-iot"}


@app.post("/telemetry")
def ingest(data: TelemetryIn) -> dict:
    telemetry = gateway.normalize(data.model_dump())
    payload = telemetry.to_dict()
    predicted = ml.predict_next_hour_load(datetime.now(timezone.utc).hour)
    actions, triggered = AutomationSwitchController.evaluate_routing_matrix(payload, predicted)
    payload["predicted_next_hour_kw"] = predicted
    payload["actions"] = actions
    payload["automation_triggered"] = triggered
    telemetry_buffer.append(payload)
    return payload


@app.post("/telemetry/demo")
def demo() -> dict:
    telemetry = gateway.simulate()
    payload = telemetry.to_dict()
    predicted = ml.predict_next_hour_load(datetime.now(timezone.utc).hour)
    actions, triggered = AutomationSwitchController.evaluate_routing_matrix(payload, predicted)
    payload.update(predicted_next_hour_kw=predicted, actions=actions, automation_triggered=triggered)
    telemetry_buffer.append(payload)
    return payload


@app.get("/telemetry")
def latest(limit: int = 50) -> list[dict]:
    if limit < 1 or limit > 200:
        raise HTTPException(400, "limit must be between 1 and 200")
    return list(telemetry_buffer)[-limit:]
