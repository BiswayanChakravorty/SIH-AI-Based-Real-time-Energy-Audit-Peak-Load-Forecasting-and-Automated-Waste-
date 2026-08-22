# SIH AI Real-Time Energy Audit + IoT

IoT-ready energy monitoring, load forecasting, waste detection and automated mitigation platform. The original architecture separates telemetry, ML inference, automation and dashboard concerns. fileciteturn2file0L14-L18

## Architecture

`ESP32 / smart meter / simulator → FastAPI IoT gateway → ML forecast → automation rules → Streamlit dashboard`

The gateway accepts normalized JSON telemetry and also provides `/telemetry/demo` for development without hardware.

## Run locally

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
pip install -r requirements.txt

uvicorn src.api:app --reload --port 8000
streamlit run src/app.py
```

## IoT API

### Health
`GET /health`

### Send device telemetry
`POST /telemetry`

Example payload:

```json
{
  "device_id": "esp32-meter-01",
  "generation_kw": 112.4,
  "demand_kw": 138.7,
  "voltage_v": 231.2,
  "current_a": 200.1,
  "power_factor": 0.94,
  "temperature_c": 34.5,
  "thermal_waste_c": 27.2
}
```

### Demo telemetry
`POST /telemetry/demo`

### Read recent telemetry
`GET /telemetry?limit=50`

## Hardware integration

For an ESP32, smart meter, PLC gateway or Raspberry Pi, publish the measured values to `/telemetry`. Keep actual relay switching behind a hardware safety layer; the automation engine currently emits recommended actions rather than energizing physical circuits directly.

## Existing ML + automation

The supplied design uses Random Forest inference for the next-hour demand estimate and threshold-based routing decisions. fileciteturn2file0L139-L162 fileciteturn2file0L173-L205
