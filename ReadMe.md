# Cosmic Weather Insurance – Problem Summary

Space weather events like solar flares, CMEs, and high-energy particle storms can severely disrupt satellites and terrestrial power grids, causing multimillion-dollar losses. Current forecasts offer only limited lead time and don’t translate well into financial risk, leaving operators and insurers without actionable insights.

Our solution addresses this gap by building an agentic AI system that autonomously ingests space-weather data, forecasts storm intensity, assesses risk to assets, and prices insurance premiums with quantified uncertainty.

The system is structured into four specialized tools coordinated by a Master Agent:

Tool 1: Data Ingestion Tool – Fetches the latest solar wind, IMF Bz, Kp index, and related space-weather data.

Tool 2: Forecasting Tool – Uses a pre-trained LSTM model to generate probabilistic 24-hour Kp index forecasts.

Tool 3: Risk Assessment Tools (Conditional Logic) – Converts forecasts into impact probabilities:

Satellite Risk Tool → Estimates anomaly probability for satellites.

Power Grid Risk Tool → Estimates GIC-related outage probability based on asset latitude.

Tool 4: Pricing Tool – Calculates expected financial loss and derives the insurance premium for the given asset.

This pipeline enables data-driven insurance pricing for space-weather risks, delivering real-time alerts, portfolio-level aggregation, and intuitive “what-if” analysis for satellite operators and insurers.

NAME:-Hitesh Ghanchi,Varun Jhaveri,Swayam Kelkar,Sarthi Kanade.

---

## Getting Started (Backend + Frontend)

### Prerequisites

- Python 3.10+
- Node.js 18+
- A Gemini API key (env var: GEMINI_API_KEY)

### 1) Backend API (FastAPI)

- Create a Python virtual environment and install dependencies:
	- pip install -r requirements.txt
- Set environment variables in a .env file (at repo root):
	- GEMINI_API_KEY=your_key_here
	- SERPER_API_KEY=optional_if_search_tool_used
- Start the API server:
	- uvicorn api_server:app --reload --port 8000
- Health check: <https://127.0.0.1:8000/api/health>

### 2) Frontend (React + Vite)

- cd web
- npm install
- npm run dev
- Open <https://127.0.0.1:5173>

### Notes

- The frontend proxies /api to <https://127.0.0.1:8000> during dev (see web/vite.config.ts).
- The portfolio data is loaded from portfolio_data.json.
- The agentic workflow requires a valid GEMINI_API_KEY and internet access for NOAA requests.

### Troubleshooting

- If CrewAI or FastAPI imports are missing, ensure requirements.txt is installed in the active env.
- If requests to /api/run fail with 500, check the server logs for missing env vars or API rate limits.