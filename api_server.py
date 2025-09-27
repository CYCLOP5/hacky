import os
import re
import json
import math
from typing import Any, Dict, Optional

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv

# CrewAI pieces (reuse the same constructs as main.py but defined locally to avoid import-time issues)
from crewai import Agent, Task, Crew, Process, LLM
from crewai_tools import SerperDevTool

from data_tools import SpaceWeatherTools
from risk_tools import RiskAssessmentTools
from cro_tools import PortfolioRiskTool
from pricing_tool import PricingTools


load_dotenv()


class NewPolicy(BaseModel):
    asset_value_millions: float
    shielding_level: str
    years_in_orbit: int
    adjustment_factor: float = 1.0


def load_portfolio_from_file(filepath: str = "portfolio_data.json") -> list:
    try:
        with open(filepath, "r") as f:
            return json.load(f)
    except Exception:
        return []


def safe_parse_json(value: Any) -> Optional[Dict[str, Any]]:
    if value is None:
        return None
    if isinstance(value, dict):
        return value
    try:
        return json.loads(value)
    except Exception:
        return None


def build_crew() -> Dict[str, Any]:
    """Create agents, tools, and tasks; return a dict with crew and task refs for introspection."""
    # Initialize one LLM shared by all agents
    llm = LLM(model="gemini/gemini-2.0-flash", api_key=os.getenv("GEMINI_API_KEY"))

    # Tools
    search_tool = SerperDevTool()
    noaa_data_tool = SpaceWeatherTools()
    risk_assessment_tool = RiskAssessmentTools()
    portfolio_risk_tool = PortfolioRiskTool()
    pricing_tool = PricingTools()

    # Agents
    data_ingestion_agent = Agent(
        role="Space Weather Data Analyst",
        goal="Fetch and synthesize the latest space weather forecasts and real-time alerts.",
        backstory="Expert in monitoring NOAA and other sources for critical space weather data.",
        verbose=False,
        tools=[noaa_data_tool, search_tool],
        llm=llm,
    )

    risk_assessment_agent = Agent(
        role="GEO Satellite Actuarial Analyst",
        goal=(
            "Determine the precise incident probability for a single satellite based on its characteristics "
            "and the space weather forecast."
        ),
        backstory="A senior actuary specializing in astrophysics and satellite engineering.",
        verbose=False,
        tools=[risk_assessment_tool],
        llm=llm,
    )

    cro_agent = Agent(
        role="Chief Risk Officer",
        goal=(
            "Analyze the entire insurance portfolio to assess total risk exposure and provide a strategic business recommendation."
        ),
        backstory=(
            "You are the Chief Risk Officer, focused on the overall financial health and solvency of the company."
        ),
        verbose=False,
        tools=[portfolio_risk_tool],
        llm=llm,
    )

    premium_pricing_agent = Agent(
        role="Pricing Specialist",
        goal=(
            "Synthesize individual risk and portfolio-level risk to calculate a final, commercially viable insurance premium."
        ),
        backstory=(
            "You must balance risk with market competitiveness, incorporating high-level strategic directives from the CRO."
        ),
        verbose=False,
        tools=[pricing_tool],
        llm=llm,
    )

    # Tasks
    data_task = Task(
        description=(
            "Fetch the latest NOAA Kp index forecast and search for any real-time space weather alerts. "
            "Consolidate this into a structured JSON report."
        ),
        expected_output="A JSON object with 'worst_case_kp' and 'real_time_context'.",
        agent=data_ingestion_agent,
    )

    risk_task = Task(
        description=(
            "Analyze the risk for a single GEO satellite. Use the data from the previous task and the following asset details: "
            "asset_value_millions: {asset_value_millions}, "
            "shielding_level: '{shielding_level}', "
            "years_in_orbit: {years_in_orbit}. "
            "Execute your 'GEO Satellite Risk Assessment Tool' with this information."
        ),
        expected_output="A JSON string containing the 'incident_probability' for the single new asset.",
        agent=risk_assessment_agent,
        context=[data_task],
    )

    portfolio_task = Task(
        description=(
            "Conduct a full portfolio analysis. Use the `worst_case_kp` from the data analyst's report and the list of all currently insured assets in the `{portfolio}`. "
            "Execute your 'Portfolio Risk Analysis Tool' to determine the Probable Maximum Loss (PML) and provide a strategic business recommendation."
        ),
        expected_output=(
            "A JSON object with 'total_exposure_millions', 'probable_maximum_loss_millions', and a 'strategic_recommendation'."
        ),
        agent=cro_agent,
        context=[data_task],
    )

    pricing_task = Task(
        description=(
            "Calculate the final 24-hour insurance premium for the new asset. You have two critical inputs: "
            "1. The individual incident probability for the new asset (from the actuarial analyst). "
            "2. The strategic recommendation for the entire portfolio (from the CRO). "
            "Synthesize these inputs. If the CRO's recommendation is anything other than 'Continue Writing New Policies', you MUST apply a surcharge to the final premium to account for the increased portfolio risk. "
            "Then, execute the 'Insurance Premium Calculation Tool' using the new asset's details: "
            "incident_probability: [from risk_task], "
            "asset_value_millions: {asset_value_millions}, "
            "adjustment_factor: {adjustment_factor}. "
            "Clearly state the final premium and whether a portfolio-risk surcharge was applied in your final answer."
        ),
        expected_output=(
            "A final report detailing the calculated premium, including the base premium, any applied surcharge, and the final quote."
        ),
        agent=premium_pricing_agent,
        context=[risk_task, portfolio_task],
    )

    crew = Crew(
        agents=[
            data_ingestion_agent,
            risk_assessment_agent,
            cro_agent,
            premium_pricing_agent,
        ],
        tasks=[data_task, risk_task, portfolio_task, pricing_task],
        verbose=False,
        process=Process.sequential,
    )

    return {
        "crew": crew,
        "data_task": data_task,
        "risk_task": risk_task,
        "portfolio_task": portfolio_task,
        "pricing_task": pricing_task,
    }


app = FastAPI(title="Borealis Insurance API")

# CORS for local dev
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        os.getenv("FRONTEND_ORIGIN", "*")
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/health")
def health():
    return {"status": "ok"}


@app.get("/api/portfolio")
def get_portfolio():
    data = load_portfolio_from_file()
    return {"items": data}


@app.get("/api/kp-forecast")
def kp_forecast(hours: int = 72):
    """Return Kp forecast time series for the next N hours (default 72)."""
    import requests
    import pandas as pd
    from datetime import datetime, timedelta

    url = "https://services.swpc.noaa.gov/products/noaa-planetary-k-index-forecast.json"
    try:
        resp = requests.get(url, timeout=15)
        resp.raise_for_status()
        data = resp.json()
        if not data or len(data) < 2:
            raise ValueError("Empty or invalid NOAA forecast data")

        columns, records = data[0], data[1:]
        df = pd.DataFrame(records, columns=columns)
        df['time_tag'] = pd.to_datetime(df['time_tag'])
        df['kp'] = pd.to_numeric(df['kp'], errors='coerce')
        df = df.dropna(subset=['kp'])

        now_utc = datetime.utcnow()
        horizon = now_utc + timedelta(hours=max(1, min(hours, 168)))  # cap at 7 days
        window = df[(df['time_tag'] >= now_utc) & (df['time_tag'] <= horizon)].copy()
        if window.empty:
            # fallback: take next 72 rows as-is
            window = df.head(72).copy()

        window.sort_values('time_tag', inplace=True)
        series = [
            {"t": t.isoformat(), "kp": float(k)}
            for t, k in zip(window['time_tag'], window['kp'])
        ]

        # Aggregates
        max_kp = float(window['kp'].max()) if not window.empty else None
        min_kp = float(window['kp'].min()) if not window.empty else None
        avg_kp = float(window['kp'].mean()) if not window.empty else None

        # Daily aggregates
        window['date'] = window['time_tag'].dt.date
        by_day = window.groupby('date')['kp']
        daily = [
            {
                "date": str(idx),
                "max": float(vals.max()),
                "min": float(vals.min()),
                "avg": float(vals.mean()),
            }
            for idx, vals in by_day
        ]

        return {
            "series": series,
            "summary": {"max": max_kp, "min": min_kp, "avg": avg_kp},
            "daily": daily,
        }
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"NOAA forecast fetch failed: {e}")


def _parse_kp_token(tok: str) -> Optional[float]:
    """Parse Kp token that may include '-', 'o', '+' thirds into a float."""
    tok = tok.strip()
    if not tok:
        return None
    # Normalize unicode minus/plus
    tok = tok.replace('−', '-').replace('＋', '+')
    # Accept forms like '3', '3o', '3+', '3-'
    m = re.fullmatch(r"(\d)([+\-o])?", tok)
    if m:
        base = float(m.group(1))
        suf = m.group(2) or ''
        if suf == '+':
            return base + 1.0/3.0
        if suf == '-':
            return base - 1.0/3.0
        return base
    # Fallback pure float
    try:
        v = float(tok)
        if 0.0 <= v <= 9.0:
            return v
    except Exception:
        return None
    return None


@app.get("/api/daily-geomag")
def daily_geomag(limit: int = 30):
    """Return last N days of daily geomagnetic indices parsed from NOAA text feed.

    Output shape:
    {
      days: [
        { date: 'YYYY-MM-DD', ap: number|null, kp_values: [.. up to 8 ..], kp_max: number|null, kp_avg: number|null }
      ]
    }
    """
    import requests
    url = "https://services.swpc.noaa.gov/text/daily-geomagnetic-indices.txt"
    try:
        resp = requests.get(url, timeout=15)
        resp.raise_for_status()
        text = resp.text
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"NOAA daily indices fetch failed: {e}")

    lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
    rows = []
    for ln in lines:
        # Find lines starting with date-like tokens
        parts = ln.split()
        if len(parts) < 4:
            continue
        # Look for YYYY MM DD
        try:
            y, m, d = int(parts[0]), int(parts[1]), int(parts[2])
            if y < 1900 or not (1 <= m <= 12) or not (1 <= d <= 31):
                continue
            date_str = f"{y:04d}-{m:02d}-{d:02d}"
        except Exception:
            continue

        # NOAA format: YYYY MM DD [Ap] [8 K-indices] [Ap] [8 K-indices] [Ap] [8 Kp values]
        # The actual Kp values (decimals) are at the very end, after all the integer K-indices
        ap_val: Optional[float] = None
        kp_vals: list[float] = []
        
        # Strategy: Look for decimal values (containing '.') at the end of the line
        # These are the actual Kp values we want
        decimal_values = []
        for i in range(len(parts) - 1, 2, -1):  # Work backwards from end, skip date
            part = parts[i]
            if '.' in part:  # This is a decimal value (Kp)
                try:
                    val = float(part)
                    if 0.0 <= val <= 9.0:
                        decimal_values.insert(0, val)  # Insert at beginning to maintain order
                    if len(decimal_values) == 8:  # We found all 8 Kp values
                        break
                except:
                    continue
        
        kp_vals = decimal_values
        
        # Find the planetary Ap value (usually the third integer after the date)
        integer_candidates = []
        for i, part in enumerate(parts[3:], 3):  # Skip date parts
            try:
                val = float(part)
                if val == int(val) and 0 <= val <= 400:  # Integer Ap values
                    integer_candidates.append(val)
                if len(integer_candidates) == 3:  # Found third Ap (planetary)
                    ap_val = integer_candidates[2]
                    break
            except:
                continue

        kp_max = max(kp_vals) if kp_vals else None
        kp_avg = sum(kp_vals) / len(kp_vals) if kp_vals else None
        rows.append({
            "date": date_str,
            "ap": ap_val,
            "kp_values": kp_vals,
            "kp_max": kp_max,
            "kp_avg": kp_avg,
        })

    # Keep only last N entries by date
    try:
        rows.sort(key=lambda r: r["date"])  # ascending
        if limit and limit > 0:
            rows = rows[-limit:]
    except Exception:
        pass

    return {"days": rows}


@app.get("/api/forecast-3day")
def forecast_3day():
    """Parse NOAA 3-day forecast text into structured JSON.

    Returns:
    {
      issued: ISO8601 string or null,
      observed_max_kp: float | null,
      expected_max_kp: float | null,
      days: ["YYYY-MM-DD", "YYYY-MM-DD", "YYYY-MM-DD"],
      breakdown: [ { period: "00-03UT", values: [d1, d2, d3] }, ... ],
      rationale: string
    }
    """
    import requests
    from datetime import datetime

    url = "https://services.swpc.noaa.gov/text/3-day-forecast.txt"
    try:
        resp = requests.get(url, timeout=15)
        resp.raise_for_status()
        text = resp.text
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"NOAA 3-day forecast fetch failed: {e}")

    lines = text.splitlines()
    # Parse issued timestamp
    issued_iso = None
    for ln in lines:
        if ln.startswith(":Issued:"):
            # Example: ":Issued: 2025 Sep 26 1230 UTC"
            try:
                parts = ln.split(":", 1)[1].strip()
                # Convert '2025 Sep 26 1230 UTC' to ISO
                dt = datetime.strptime(parts.replace(" UTC", ""), "%Y %b %d %H%M")
                issued_iso = dt.strftime("%Y-%m-%dT%H:%M:00Z")
            except Exception:
                pass
            break

    # Parse observed and expected max kp
    observed_max = None
    expected_max = None
    for ln in lines:
        if "greatest observed 3 hr Kp" in ln:
            m = re.search(r"(\d+\.\d+|\d+)", ln)
            if m:
                try:
                    observed_max = float(m.group(1))
                except Exception:
                    pass
        if "greatest expected 3 hr Kp" in ln:
            m = re.search(r"(\d+\.\d+|\d+)", ln)
            if m:
                try:
                    expected_max = float(m.group(1))
                except Exception:
                    pass

    # Find breakdown header and parse grid
    breakdown_rows = []
    day_labels = []
    rationale = ""
    try:
        start_idx = None
        for i, ln in enumerate(lines):
            if ln.strip().startswith("NOAA Kp index breakdown"):
                start_idx = i
                break
        if start_idx is not None:
            # Next lines: blank, then header with three day labels
            i = start_idx + 1
            # Skip blank lines
            while i < len(lines) and not lines[i].strip():
                i += 1
            # Header line with dates
            if i < len(lines):
                header = lines[i]
                # tokens like 'Sep 26       Sep 27       Sep 28'
                day_tokens = [t for t in header.split() if t.isalpha() or t.isdigit() or (len(t) == 3 and t.isalpha())]
                # A simpler approach: just split and grab the last 6 tokens and join pairs
                raw = header.strip().split()
                # Attempt to reconstruct labels as pairs month day
                tmp = []
                j = 0
                while j < len(raw):
                    if raw[j].isalpha() and j + 1 < len(raw) and raw[j+1].isdigit():
                        tmp.append(f"{raw[j]} {raw[j+1]}")
                        j += 2
                    else:
                        j += 1
                day_labels = tmp[:3]
                i += 1

            # Parse 8 time rows until blank line
            count = 0
            while i < len(lines) and count < 8:
                row = lines[i]
                if not row.strip():
                    break
                # Example: '00-03UT       2.33         2.33         2.33'
                m = re.match(r"\s*([0-9]{2}-[0-9]{2}UT)\s+(.+)$", row)
                if m:
                    period = m.group(1)
                    rest = m.group(2)
                    nums = re.findall(r"\d+\.\d+|\d+", rest)
                    values = [float(x) for x in nums[:3]] if nums else []
                    breakdown_rows.append({"period": period, "values": values})
                    count += 1
                i += 1

        # Capture rationale paragraph following the breakdown
        # Find line starting with 'Rationale:' near the breakdown region
        for k in range((start_idx or 0), min((start_idx or 0) + 100, len(lines))):
            if lines[k].strip().startswith("Rationale:"):
                rationale = lines[k].split(":", 1)[1].strip()
                # Include subsequent lines until blank
                t = k + 1
                extra = []
                while t < len(lines) and lines[t].strip():
                    extra.append(lines[t].strip())
                    t += 1
                if extra:
                    rationale += " " + " ".join(extra)
                break
    except Exception:
        pass

    # Try to attach year to day labels using the line that contains the 3-day range
    year = None
    for ln in lines:
        if "Sep" in ln and "202" in ln and "NOAA Kp index breakdown" in lines[start_idx] if 'start_idx' in locals() and start_idx is not None else True:
            m = re.search(r"(20\d{2})", ln)
            if m:
                year = int(m.group(1))
                break
    # Fallback: look earlier line with 'Sep 26-Sep 28 2025'
    if year is None:
        for ln in lines:
            m = re.search(r"(20\d{2})", ln)
            if m:
                year = int(m.group(1))
                break

    # Build ISO dates if possible
    from calendar import month_abbr
    month_map = {m: i for i, m in enumerate(month_abbr) if m}
    iso_days = []
    if year and len(day_labels) == 3:
        for label in day_labels:
            try:
                mon_str, day_str = label.split()
                mon = month_map.get(mon_str[:3], None)
                day = int(day_str)
                if mon:
                    iso_days.append(f"{year:04d}-{mon:02d}-{day:02d}")
            except Exception:
                iso_days.append(label)
    else:
        iso_days = day_labels

    return {
        "issued": issued_iso,
        "observed_max_kp": observed_max,
        "expected_max_kp": expected_max,
        "days": iso_days,
        "breakdown": breakdown_rows,
        "rationale": rationale,
    }


def _next_24h_max_kp_from_noaa_json() -> Optional[float]:
    """Fetch official NOAA JSON and compute the next-24h maximum Kp.
    Returns a float in [0, 9] or None if unavailable.
    """
    try:
        import requests
        import pandas as pd
        from datetime import datetime, timedelta
        url = "https://services.swpc.noaa.gov/products/noaa-planetary-k-index-forecast.json"
        resp = requests.get(url, timeout=15)
        resp.raise_for_status()
        data = resp.json()
        if not data or len(data) < 2:
            return None
        columns, records = data[0], data[1:]
        df = pd.DataFrame(records, columns=columns)
        df['time_tag'] = pd.to_datetime(df['time_tag'])
        df['kp'] = pd.to_numeric(df['kp'], errors='coerce')
        df = df.dropna(subset=['kp'])
        now_utc = datetime.utcnow()
        horizon = now_utc + timedelta(hours=24)
        win = df[(df['time_tag'] >= now_utc) & (df['time_tag'] <= horizon)]
        if win.empty:
            return None
        val = float(win['kp'].max())
        # Clamp to physical range
        return max(0.0, min(9.0, val))
    except Exception:
        return None


def _next_24h_max_kp_from_3day() -> Optional[float]:
    """Compute the next-24h max Kp using the 3-day forecast breakdown (first day)."""
    try:
        data = forecast_3day()
        breakdown = data.get("breakdown") or []
        if not breakdown:
            return None
        vals = []
        for row in breakdown:
            arr = row.get("values") or []
            if len(arr) >= 1 and isinstance(arr[0], (int, float)):
                vals.append(float(arr[0]))
        if not vals:
            return None
        val = max(vals)
        return max(0.0, min(9.0, float(val)))
    except Exception:
        return None


def _next_24h_kp_detail_from_3day() -> Optional[Dict[str, Any]]:
    """Return details for the first-day max from the 3-day forecast: value, period, and day."""
    try:
        data = forecast_3day()
        breakdown = data.get("breakdown") or []
        days = data.get("days") or []
        if not breakdown or not days:
            return None
        day0 = days[0]
        best = {"value": None, "period": None}
        for row in breakdown:
            vals = row.get("values") or []
            if not vals:
                continue
            v = vals[0]
            if isinstance(v, (int, float)):
                if best["value"] is None or v > best["value"]:
                    best = {"value": float(v), "period": row.get("period")}
        if best["value"] is None:
            return None
        return {"value": max(0.0, min(9.0, best["value"])), "period": best["period"], "day": day0}
    except Exception:
        return None


def _parse_incident_probability_from_text(text: str) -> Optional[float]:
    """Extract 'Incident Probability: X' from a text block."""
    try:
        m = re.search(r"Incident\s+Probability\s*:\s*([0-9]*\.?[0-9]+)", text, flags=re.IGNORECASE)
        if not m:
            return None
        val = float(m.group(1))
        # If value looks like a percent (>1), assume it's already a fraction? Keep as-is if <=1
        if val > 1.0 and val <= 100.0:
            return round(val / 100.0, 6)
        return max(0.0, min(1.0, val))
    except Exception:
        return None


def _compute_incident_probability(kp: float, shielding: str, years_in_orbit: int) -> float:
    """Deterministic fallback based on logistic curve and simple adjustments.

    - Base: p = 1/(1+exp(-1.5*(kp-7)))
    - Shielding: Hardened -45%, Standard 0%, Light/Legacy +35%
    - Aging: +1.5% per year
    """
    try:
        kp = max(0.0, min(9.0, float(kp)))
        base = 1.0 / (1.0 + math.exp(-1.5 * (kp - 7.0)))
        s = (shielding or "").lower()
        if "hardened" in s:
            base *= 0.55
        elif "light" in s or "legacy" in s:
            base *= 1.35
        # standard -> no change
        years = max(0, int(years_in_orbit))
        base *= (1.0 + 0.015 * years)
        return max(0.0, min(1.0, base))
    except Exception:
        return 0.0


@app.post("/api/run")
def run_full_workflow(body: NewPolicy):
    if not os.getenv("GEMINI_API_KEY"):
        raise HTTPException(status_code=500, detail="GEMINI_API_KEY not configured")

    portfolio = load_portfolio_from_file()
    if not portfolio:
        raise HTTPException(status_code=400, detail="Portfolio data is missing or empty.")

    setup = build_crew()
    crew = setup["crew"]
    data_task = setup["data_task"]
    risk_task = setup["risk_task"]
    portfolio_task = setup["portfolio_task"]
    pricing_task = setup["pricing_task"]

    inputs = {
        "asset_value_millions": body.asset_value_millions,
        "shielding_level": body.shielding_level,
        "years_in_orbit": body.years_in_orbit,
        "adjustment_factor": body.adjustment_factor,
        "portfolio": portfolio,
    }

    try:
        result = crew.kickoff(inputs=inputs)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Workflow error: {e}")

    # Parse intermediate outputs where possible
    worst_case_kp = None
    individual_risk = None
    portfolio_assessment = None
    pricing_result = None

    kp_detail = None
    try:
        # Preferred: use official 3-day forecast (first day) for next-24h Kp
        d = _next_24h_kp_detail_from_3day()
        if d is not None:
            worst_case_kp = d.get("value")
            kp_detail = {"source": "3-day-forecast", "period": d.get("period"), "day": d.get("day")}

        # Fallback: official JSON forecast API
        if worst_case_kp is None:
            fallback = _next_24h_max_kp_from_noaa_json()
            if fallback is not None:
                worst_case_kp = fallback
                kp_detail = {"source": "noaa-json-forecast"}

        # Last resort: parse Data Agent output
        if worst_case_kp is None and data_task.output and getattr(data_task.output, "raw", None):
            raw_str = data_task.output.raw
            data_json = safe_parse_json(raw_str)
            if data_json:
                val = data_json.get("worst_case_kp")
                if isinstance(val, (int, float)):
                    worst_case_kp = max(0.0, min(9.0, float(val)))
                    kp_detail = {"source": "agent-parsed"}
            if worst_case_kp is None and isinstance(raw_str, str):
                m = re.findall(r"Kp[^\d]*(\d+\.\d+|\d+)", raw_str, flags=re.IGNORECASE)
                if m:
                    try:
                        worst_case_kp = max(0.0, min(9.0, float(m[-1])))
                        kp_detail = {"source": "agent-parsed"}
                    except Exception:
                        pass
    except Exception:
        pass

    try:
        if risk_task.output and getattr(risk_task.output, "raw", None):
            individual_risk = safe_parse_json(risk_task.output.raw)
    except Exception:
        pass

    try:
        if portfolio_task.output and getattr(portfolio_task.output, "raw", None):
            portfolio_assessment = safe_parse_json(portfolio_task.output.raw)
    except Exception:
        pass

    try:
        raw = getattr(result, "raw", None)
        pricing_result = safe_parse_json(raw) or {"raw": raw}
        # Extract final premium if present in raw text
        if isinstance(raw, str):
            m = re.search(r"Final\s+Premium:\s*\$([\d,]+(?:\.\d{2})?)", raw, re.IGNORECASE)
            if m:
                amt = m.group(1).replace(",", "")
                try:
                    pricing_result["final_premium_usd"] = float(amt)
                except Exception:
                    pass
    except Exception:
        pricing_result = None

    # Deterministic fallback for portfolio assessment if JSON missing
    if portfolio_assessment is None and worst_case_kp is not None and portfolio:
        try:
            bumped_kp = math.ceil(float(worst_case_kp) + 1.0)
            risk_kp = min(bumped_kp, 9.0)
            probability = 1.0 / (1.0 + math.exp(-1.5 * (risk_kp - 7)))
            total_exposure = sum(float(item.get("value_millions", 0.0)) for item in portfolio)
            pml = sum(float(item.get("value_millions", 0.0)) * probability for item in portfolio)
            pct = (pml / total_exposure) * 100.0 if total_exposure > 0 else 0.0
            if pct < 5.0:
                rec = "Continue Writing New Policies"
            elif pct <= 15.0:
                rec = "Temporarily Halt New Policies"
            else:
                rec = "Urgent Reinsurance Required"
            portfolio_assessment = {
                "total_exposure_millions": round(total_exposure, 3),
                "probable_maximum_loss_millions": round(pml, 3),
                "strategic_recommendation": rec,
                "reasoning": f"Fallback computation with risk_kp={risk_kp}, probability={probability:.4f}"
            }
        except Exception:
            pass

    # Incident probability fallback if risk agent didn't produce JSON
    if individual_risk is None:
        # Try parse from pricing_result raw
        parsed_prob = None
        try:
            if pricing_result and isinstance(pricing_result.get("raw"), str):
                parsed_prob = _parse_incident_probability_from_text(pricing_result["raw"])            
        except Exception:
            parsed_prob = None

        if parsed_prob is None and worst_case_kp is not None:
            parsed_prob = _compute_incident_probability(
                kp=worst_case_kp,
                shielding=body.shielding_level,
                years_in_orbit=body.years_in_orbit,
            )

        if parsed_prob is not None:
            individual_risk = {
                "risk_category": (
                    "Low" if parsed_prob < 0.02 else "Moderate" if parsed_prob < 0.08 else "High"
                ),
                "reasoning": "Deterministic fallback based on NOAA Kp, shielding, and age.",
                "incident_probability": round(parsed_prob, 6),
                "confidence": 0.7,
            }

    return {
        "inputs": inputs,
        "worst_case_kp": worst_case_kp,
        "kp_source": kp_detail.get("source") if isinstance(kp_detail, dict) else None,
        "kp_detail": kp_detail,
        "individual_risk": individual_risk,
        "portfolio_assessment": portfolio_assessment,
        "pricing_result": pricing_result,
    }


# Run with: uvicorn api_server:app --reload
