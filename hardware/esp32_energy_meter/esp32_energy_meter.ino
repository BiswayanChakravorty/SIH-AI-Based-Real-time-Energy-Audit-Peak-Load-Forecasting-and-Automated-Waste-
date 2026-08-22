#include <WiFi.h>
#include <HTTPClient.h>

const char* WIFI_SSID = "YOUR_WIFI";
const char* WIFI_PASSWORD = "YOUR_PASSWORD";
const char* API_URL = "http://YOUR_SERVER:8000/telemetry";
const char* DEVICE_ID = "esp32-meter-01";

// Replace these demo readings with your calibrated energy/current/voltage sensors.
float readGenerationKW() { return 110.0f; }
float readDemandKW() { return 138.0f; }
float readVoltageV() { return 230.0f; }
float readCurrentA() { return 200.0f; }
float readPowerFactor() { return 0.95f; }
float readTemperatureC() { return 32.0f; }
float readThermalWasteC() { return 25.0f; }

void connectWiFi() {
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  while (WiFi.status() != WL_CONNECTED) delay(500);
}

void setup() {
  Serial.begin(115200);
  connectWiFi();
}

void loop() {
  if (WiFi.status() != WL_CONNECTED) connectWiFi();

  HTTPClient http;
  http.begin(API_URL);
  http.addHeader("Content-Type", "application/json");

  String payload = String("{") +
    "\"device_id\":\"" + DEVICE_ID + "\"," +
    "\"generation_kw\":" + String(readGenerationKW(), 2) + "," +
    "\"demand_kw\":" + String(readDemandKW(), 2) + "," +
    "\"voltage_v\":" + String(readVoltageV(), 2) + "," +
    "\"current_a\":" + String(readCurrentA(), 2) + "," +
    "\"power_factor\":" + String(readPowerFactor(), 3) + "," +
    "\"temperature_c\":" + String(readTemperatureC(), 2) + "," +
    "\"thermal_waste_c\":" + String(readThermalWasteC(), 2) +
    "}";

  int status = http.POST(payload);
  Serial.printf("Telemetry HTTP status: %d\n", status);
  http.end();
  delay(5000);
}
