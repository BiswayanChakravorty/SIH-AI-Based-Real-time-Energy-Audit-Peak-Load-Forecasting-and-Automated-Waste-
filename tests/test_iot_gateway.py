import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1] / "src"))

from iot_gateway import IoTTelemetryGateway


def test_normalize_defaults():
    t = IoTTelemetryGateway.normalize({
        "device_id": "meter-1",
        "generation_kw": 100,
        "demand_kw": 120,
    })
    assert t.device_id == "meter-1"
    assert t.demand_kw == 120
    assert t.voltage_v == 230


def test_normalize_rejects_missing_fields():
    try:
        IoTTelemetryGateway.normalize({"device_id": "meter-1"})
    except ValueError as exc:
        assert "generation_kw" in str(exc)
        assert "demand_kw" in str(exc)
    else:
        raise AssertionError("Expected ValueError")
