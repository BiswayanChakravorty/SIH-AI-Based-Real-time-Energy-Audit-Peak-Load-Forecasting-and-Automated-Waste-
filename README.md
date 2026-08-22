# SIH 2026: AI-Based Real-time Energy Audit & Optimization Platform (Live API Version)

This application has been completely rebuilt to use **Live Public Web Data APIs** instead of random simulation or IoT hardware. It ingests real-time grid generation mixes (via the UK Carbon Intensity API), scales them to micro-grid proportions, and uses a Random Forest ML model to forecast next-hour demand and trigger automated waste mitigation protocols.

## 🚀 Key Features
- **No IoT Required:** Pulls live energy data directly from public web APIs.
- **Real-Time Telemetry:** Streams live generation and demand metrics into an interactive Streamlit dashboard.
- **ML Load Forecasting:** Uses `scikit-learn` Random Forest to predict upcoming demand spikes.
- **Automated Routing:** Evaluates live metrics against thresholds to trigger virtual battery dispatch and thermal rerouting.

## 💻 Local Setup Instructions
1. Clone the repository and navigate to the root directory.
2. Initialize a Python virtual environment: `python -m venv venv`
3. Activate the environment: `source venv/bin/activate` (or `venv\Scripts\activate` on Windows)
4. Install dependencies: `pip install -r requirements.txt`
5. Run the application: `streamlit run src/app.py`
https://liveaudit-udeb4gvu.manus.space/  FUNCTIONAL WEBSITE
