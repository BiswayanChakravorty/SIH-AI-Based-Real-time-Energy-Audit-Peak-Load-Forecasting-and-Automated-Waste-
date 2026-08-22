import datetime
import time
import streamlit as st
import pandas as pd
import plotly.graph_objects as go

from api_client import GridDataAPI
from ML_engine import EnergyMLCore
from automation import AutomationSwitchController

# Streamlit UI Configuration Setup
st.set_page_config(page_title="Live Energy Audit Console", layout="wide")
st.title("🌍 Real-Time Grid Data Energy Audit & Waste Optimization")
st.caption("Powered by Live Public APIs (No IoT Hardware Required)")

# Initialize long-term persistent runtime components
if "api_client" not in st.session_state:
    st.session_state.api_client = GridDataAPI()
    st.session_state.ml_core = EnergyMLCore()
    st.session_state.history_buffer = []
    st.session_state.event_logs = []

# Render Dashboard KPI Layout blocks
kpi_space = st.columns(5)
chart_space = st.empty()
log_space = st.empty()

# Persistent Execution Tracking Iteration Loop
while True:
    # Fetch LIVE data from public API instead of simulating
    current_tick_data = st.session_state.api_client.fetch_real_time_telemetry()
    st.session_state.history_buffer.append(current_tick_data)
    
    if len(st.session_state.history_buffer) > 40:
        st.session_state.history_buffer.pop(0)

    # ML Inference Step Execution
    current_hour_int = datetime.datetime.now().hour
    load_prediction_kw = st.session_state.ml_core.predict_next_hour_load(current_hour_int, current_tick_data['demand_kw'])

    # Automation Engine Switching Evaluation Execution
    active_routing_logs, event_flag = AutomationSwitchController.evaluate_routing_matrix(current_tick_data, load_prediction_kw)
    
    for alert in active_routing_logs:
        full_log_string = f"[{current_tick_data['timestamp']}] {alert['message']}"
        if not any(full_log_string in standard_log for standard_log in st.session_state.event_logs):
            st.session_state.event_logs.insert(0, (full_log_string, alert['type']))
            
    if len(st.session_state.event_logs) > 12:
        st.session_state.event_logs.pop()

    # Dynamic KPI Panel Updates
    kpi_space[0].metric("Live Renewable Generation", f"{current_tick_data['generation_kw']} kW")
    kpi_space[1].metric("Live Grid Demand", f"{current_tick_data['demand_kw']} kW")
    kpi_space[2].metric("System Efficiency", f"{current_tick_data['efficiency_pct']} %")
    kpi_space[3].metric("Next-Hour Forecast", f"{load_prediction_kw} kW")
    kpi_space[4].metric("Data Source", current_tick_data['source'])

    # Time-Series Interactive Visualization Generation via Plotly
    if len(st.session_state.history_buffer) > 0:
        df = pd.DataFrame(st.session_state.history_buffer)
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df['timestamp'], y=df['generation_kw'], name='Clean Generation (kW)', line=dict(color='#2ecc71', width=3)))
        fig.add_trace(go.Scatter(x=df['timestamp'], y=df['demand_kw'], name='Grid Demand (kW)', line=dict(color='#e74c3c', width=3, dash='dash')))
        fig.add_trace(go.Scatter(x=df['timestamp'], y=df['thermal_waste_c'], name='Thermal Fluid Loss (°C)', yaxis='y2', line=dict(color='#f1c40f', width=2)))

        fig.update_layout(
            title="Live Public Grid Data Synchronization Pipeline",
            xaxis_title="Time",
            yaxis_title="Electrical Active Load Power (kW)",
            yaxis2=dict(title="Thermal Energy Scale (°C)", overlaying='y', side='right'),
            height=400,
            margin=dict(l=10, r=10, t=40, b=10),
            legend=dict(orientation="h", y=1.1)
        )
        chart_space.plotly_chart(fig, use_container_width=True)

    # Update Action Optimization Log Panels
    with log_space.container():
        st.write("### 🤖 Automated Micro-Grid Distribution & Routing Matrices")
        if len(st.session_state.event_logs) == 0:
            st.info("System operating nominally. No routing actions required.")
        for entry, log_type in st.session_state.event_logs:
            if log_type == "CRITICAL":
                st.error(entry)
            elif log_type == "WARNING":
                st.warning(entry)
            else:
                st.success(entry)

    # Poll API every 5 seconds
    time.sleep(5)
    st.rerun()
