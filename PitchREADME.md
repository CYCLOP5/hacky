# Project Borealis – Hackathon Pitch Script

> **Time box:** 3 minutes

## 1. Opening Hook (0:00 – 0:25)

Good morning judges! Imagine you’re underwriting a $300 million satellite mission when NOAA flashes a severe geomagnetic storm warning. Within hours, solar wind can fry electronics, scramble GPS, and trigger cascading failures across your entire portfolio. Today, insurers make life-or-death pricing calls using stale dashboards and gut instinct. Project **Borealis** changes that story.

## 2. Problem & Stakes (0:25 – 0:55)

- Space-weather incidents have produced multi-billion dollar losses—think the 2003 Halloween storms and the 2015 Quebec blackout.
- Forecast data is raw and noisy; translating it into exposure-adjusted premiums requires a war-room of analysts.
- Insurers need a way to **see**, **price**, and **act** on cosmic volatility in real time—without grounding fleets or walking away from profitable policies.

## 3. Our Breakthrough (0:55 – 1:35)

Project Borealis orchestrates a crew of specialized AI agents to deliver a fully underwritten quote in minutes:

1. **Data Analyst Agent** pulls live NOAA telemetry and historical analogs.
2. **Forecasting Agent** runs a pre-trained **LSTM time-series model** to generate a probabilistic 24-hour Kp index, rather than trusting a single deterministic value.
3. **Risk Analyst Agent** converts that forecast into anomaly probabilities for the specific satellite, factoring shielding, mission age, and orbit.
4. **Chief Risk Officer Agent** evaluates portfolio-level exposure, deciding whether to keep writing policies.
5. **Pricing Actuary Agent** synthesizes everything into a premium, automatically capping at 15% of asset value, or recommending partial coverage instead of rejecting a customer outright.

Every step is auditable, surfaced in plain English, and replayable through our UI so underwriters can trust the pipeline.

## 4. Live Demo Flow (1:35 – 2:35)

Here’s how I walk the judges through the product:

1. **Configure a policy**: Enter satellite value, shielding class, and mission duration.
2. **Run the AI workflow**: Hit “Run Analysis” and watch the step indicator light up as agents collaborate.
3. **Reveal the dashboard**: Show the real-time KP forecast, risk categorization, and CRO recommendation.
4. **Drill into the premium**: Highlight how the AI explains its math—expected loss, LSTM-derived surcharge, coverage adjustments.
5. **Historical playback**: Jump to the Historical Events page, select the newly-added *St. Patrick’s Day Storm 2015* scenario, and show how the system recommends a partial coverage plan instead of a blanket rejection.

## 5. Competitive Edge (2:35 – 2:50)

- **LSTM-powered forecasting** beats rule-based triggers by learning storm cadence from decades of NASA and NOAA data.
- **Agentic architecture** (CrewAI + FastAPI) keeps human-understandable guardrails while scaling to multiple asset classes.
- **Dual-screen experience** (React/Vite front-end + FastAPI backend) means underwriting teams and ops centers get the same transparent story.
- **Business empathy baked in**: the system negotiates modified coverage, deductibles, and mitigation tips—so we close deals instead of issuing “sorry, rejected” emails.
