import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor

class EnergyMLCore:
    def __init__(self):
        self.model = RandomForestRegressor(n_estimators=20, random_state=42)
        self.is_trained = False
        self._pretrain_fallback_model()

    def _pretrain_fallback_model(self):
        """Pre-seeds the engine with mock baseline history to prevent data-starvation faults."""
        hours = np.tile(np.arange(24), 10)
        historical_demand = 80 + 50 * np.sin(hours * np.pi / 12) + np.random.normal(0, 10, len(hours))
        X = pd.DataFrame({"hour": hours})
        self.model.fit(X, historical_demand)
        self.is_trained = True

    def predict_next_hour_load(self, current_hour, current_demand=None):
        """Calculates upcoming energy consumption demand spikes."""
        next_hour = (current_hour + 1) % 24
        X_next = pd.DataFrame({"hour": [next_hour]})
        prediction = self.model.predict(X_next)[0]
        
        # Adjust prediction based on live data if available
        if current_demand is not None:
            prediction = (prediction * 0.3) + (current_demand * 0.7)
            
        return round(prediction, 2)
