"""IoT telemetry gateway with simulator and HTTP ingestion support."""
from __future__ import annotations

import datetime as dt
import os
import random
from dataclasses import dataclass, asdict
from typing import Any

try:
    import requests
except ImportError:  # optional for simulation-only deployments
    requests = None


@dataclass
class Telemetry:
    device_id: str
    timestamp: str
    generation_kw: float
    demand_kw: float
    voltage_v: float
    current_a: float
    power_factor: float
    temperature_c: float
    thermal_waste_c: float

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


class IoTTelemetryGateway:
    """Normalizes physical-device payloads or generates demo telemetry."""

    def __init__(self, device_id: str = "demo-meter-01") -> None:
        self.device_id = device_id

    def simulate(self) -> Telemetry:
        hour = dt.datetime.now().hour
        solar = max(0.0, min(1.0, (hour - 5) / 12)) if 5 <= hour <= 18 else 0.0
        generation = max(0.0, 160 * solar + random.uniform(-5, 5))
        demand_base = 65 if hour < 8 or hour > 22 else (135 if 9 <= hour <= 17 else 150)
        demand = max(10.0, demand_base + random.uniform(-18, 18))
        voltage = random.uniform(228, 242)
        current = (demand * 1000) / max(voltage * 3, 1)
        pf = random.uniform(0.90, 0.99)
        temperature = random.uniform(27, 39)
        thermal_waste = max(15.0, demand * 0.14 + random.uniform(0, 8))
        return Telemetry(
            self.device_id,
            dt.datetime.now(dt.timezone.utc).isoformat(),
            round(generation, 2), round(demand, 2), round(voltage, 2),
            round(current, 2), round(pf, 3), round(temperature, 2),
            round(thermal_waste, 2),
        )

    @staticmethod
    def normalize(payload: dict[str, Any]) -> Telemetry:
        required = ["device_id", "generation_kw", "demand_kw"]
        missing = [key for key in required if key not in payload]
        if missing:
            raise ValueError(f"Missing telemetry fields: {', '.join(missing)}")
        demand = float(payload["demand_kw"])
        return Telemetry(
            str(payload["device_id"]),
            str(payload.get("timestamp") or dt.datetime.now(dt.timezone.utc).isoformat()),
            float(payload["generation_kw"]), demand,
            float(payload.get("voltage_v", 230.0)),
            float(payload.get("current_a", demand * 1000 / 690)),
            float(payload.get("power_factor", 0.95)),
            float(payload.get("temperature_c", 30.0)),
            float(payload.get("thermal_waste_c", demand * 0.14)),
        )

    def post(self, payload: dict[str, Any], endpoint: str | None = None) -> dict[str, Any]:
        endpoint = endpoint or os.getenv("IOT_INGEST_URL")
        if not endpoint:
            raise ValueError("Set IOT_INGEST_URL or pass endpoint")
        if requests is None:
            raise RuntimeError("Install requests to use HTTP ingestion")
        response = requests.post(endpoint, json=payload, timeout=5)
        response.raise_for_status()
        return response.json() if response.content else {"status": "accepted"}
