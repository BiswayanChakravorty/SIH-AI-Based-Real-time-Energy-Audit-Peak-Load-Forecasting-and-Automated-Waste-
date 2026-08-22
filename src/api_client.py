import requests
import pandas as pd
import datetime

class GridDataAPI:
    def __init__(self):
        # We will use the free GridStatus.io public API for real-time US grid data
        # Specifically, we'll fetch ERCOT (Texas) real-time load and generation
        self.base_url = "https://api.gridstatus.io/v1"
        # No API key needed for basic public endpoints
        
    def fetch_real_time_telemetry(self):
        """Fetches live grid data from public sources instead of simulating."""
        try:
            # Using a public unauthenticated API for demonstration: 
            # National Grid ESO (UK) Carbon Intensity API (completely free and open, no key required)
            url = "https://api.carbonintensity.org.uk/generation"
            response = requests.get(url, timeout=10)
            data = response.json()
            
            generation_mix = data['data']['generationmix']
            
            # Parse real data into our required format
            total_renewable = sum([item['perc'] for item in generation_mix if item['fuel'] in ['wind', 'solar', 'hydro', 'biomass']])
            total_fossil = sum([item['perc'] for item in generation_mix if item['fuel'] in ['gas', 'coal']])
            
            # Scale percentages to simulated kW for the micro-grid dashboard feel
            generation_kw = total_renewable * 2.5
            demand_kw = (total_renewable + total_fossil) * 2.4
            
            now = datetime.datetime.now()
            time_str = now.strftime("%H:%M:%S")
            
            # Estimate thermal waste based on fossil fuel usage
            waste_heat_index = total_fossil * 0.5
            current_efficiency = 100.0 - (total_fossil * 0.3)
            
            return {
                "timestamp": time_str,
                "generation_kw": round(generation_kw, 2),
                "demand_kw": round(demand_kw, 2),
                "thermal_waste_c": round(waste_heat_index, 2),
                "efficiency_pct": round(current_efficiency, 2),
                "source": "Live UK Grid API"
            }
        except Exception as e:
            # Fallback if API fails
            print(f"API Error: {e}")
            now = datetime.datetime.now()
            return {
                "timestamp": now.strftime("%H:%M:%S"),
                "generation_kw": 0.0,
                "demand_kw": 0.0,
                "thermal_waste_c": 0.0,
                "efficiency_pct": 0.0,
                "source": "API Offline"
            }
