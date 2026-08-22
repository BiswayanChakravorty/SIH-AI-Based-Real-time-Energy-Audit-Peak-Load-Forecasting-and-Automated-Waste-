class AutomationSwitchController:
    @staticmethod
    def evaluate_routing_matrix(current_metrics, predicted_load):
        """Evaluates thresholds to trigger real-time mitigation protocols."""
        decision_logs = []
        action_triggered = False

        # Protocol A: Preemptive Peak Load Mitigation via Battery Banks
        if predicted_load > 140.0:
            decision_logs.append({
                "type": "CRITICAL",
                "message": f"Preemptive Peak Predicted ({predicted_load} kW). Dispatching localized ESS Battery Banks."
            })
            action_triggered = True

        # Protocol B: Automated Thermal Energy Recovery Redirection
        if current_metrics["thermal_waste_c"] > 32.0:
            decision_logs.append({
                "type": "WARNING",
                "message": f"High Thermal Waste ({current_metrics['thermal_waste_c']}°C). Rerouting to absorption chillers."
            })
            action_triggered = True

        # Protocol C: Grid Balancing Surplus Allocation
        if current_metrics["generation_kw"] > current_metrics["demand_kw"]:
            surplus = round(current_metrics["generation_kw"] - current_metrics["demand_kw"], 2)
            decision_logs.append({
                "type": "SUCCESS",
                "message": f"Renewable Surplus Detected (+{surplus} kW). Diverting power to thermal water heating loops."
            })
            action_triggered = True

        return decision_logs, action_triggered
