import requests
import numpy as np
import re
import json
import math
from typing import Optional
def map_kp_to_anomaly_prob(kp_index: float) -> float:
    return 1.0 / (1.0 + np.exp(-1.5 * (kp_index - 7)))
def get_noaa_forecast_from_txt(
    url: str = "https://services.swpc.noaa.gov/text/3-day-geomag-forecast.txt",
    timeout: int = 15,
    debug: bool = True
) -> Optional[np.ndarray]:
    headers = {'User-Agent': 'python-requests/1.0 (+https://your.domain)'}
    try:
        r = requests.get(url, headers=headers, timeout=timeout)
        r.raise_for_status()
        text = r.text
    except requests.exceptions.RequestException as e:
        if debug:
            print(f"[ERROR] Could not fetch NOAA file: {e}")
        return None
    lines = text.splitlines()
    joined = " ".join(lines)
    normalized = re.sub(r'[,\t/]', ' ', joined)
    normalized = re.sub(r'\s+', ' ', normalized)   
    timeslots = ["00-03UT", "03-06UT", "06-09UT", "09-12UT", "12-15UT", "15-18UT", "18-21UT", "21-00UT"]
    start_idx = normalized.find(timeslots[0])
    candidate_text = normalized[start_idx:] if start_idx != -1 else normalized
    tokens = re.findall(r'(?:\d{2}-\d{2}UT)|\d+\.\d+|\d+', candidate_text)
    idx = 0
    extracted = []
    for ts in timeslots:
        while idx < len(tokens) and tokens[idx] != ts:
            idx += 1
        if idx >= len(tokens):
            break
        idx += 1  
        nums = []
        while idx < len(tokens) and not re.match(r'\d{2}-\d{2}UT', tokens[idx]) and len(nums) < 20:
            tok = tokens[idx]
            if re.match(r'^\d+(\.\d+)?$', tok):
                try:
                    val = float(tok)
                    if 0.0 <= val <= 10.0:
                        nums.append(val)
                except Exception:
                    pass
            idx += 1
        extracted.append(nums)
    if len(extracted) < 8:
        if debug:
            print("[WARN] Could not parse 8 timeslot rows using timeslot-scan approach.")
            print(f"[DEBUG] Extracted rows count: {len(extracted)}; sample extracted: {extracted}")
        kp_lines = [ln for ln in lines if re.search(r'\bkp\b', ln, flags=re.IGNORECASE)]
        for ln in kp_lines:
            ln_norm = re.sub(r'[,\t/]', ' ', ln)
            ln_norm = re.sub(r'[-]+', ' ', ln_norm)
            toks = re.findall(r'\d+\.\d+|\d+', ln_norm)
            kps = [float(t) for t in toks if 0.0 <= float(t) <= 10.0]
            if len(kps) >= 8:
                kp_values = np.array(kps[:8], dtype=float)
                if debug:
                    print("[DEBUG] Fallback: parsed Kp from a 'kp' containing line:")
                    print("  " + ln.strip())
                    print("  Parsed:", kp_values)
                return kp_values
        all_nums = re.findall(r'\d+\.\d+|\d+', normalized)
        kps_all = [float(n) for n in all_nums if 0.0 <= float(n) <= 10.0]
        if len(kps_all) >= 8:
            kp_values = np.array(kps_all[:8], dtype=float)
            if debug:
                print("[DEBUG] Fallback across entire file; parsed first 8 plausible Kp tokens.")
                print("  Parsed:", kp_values)
            return kp_values
        if debug:
            print("[ERROR] Could not find 8 plausible Kp tokens in NOAA forecast text.")
        return None
    first_col = []
    for i, row in enumerate(extracted[:8]):
        if len(row) >= 1:
            first_col.append(row[0])
        else:
            if debug:
                print(f"[ERROR] Missing numeric token for timeslot {timeslots[i]}; extracted rows: {extracted}")
            return None
    kp_values = np.array(first_col, dtype=float)
    if debug:
        print("[DEBUG] parsed Kp values for first date:", kp_values)
    return kp_values
def calculate_premium_for_satellite(
    daily_kp_forecast: np.ndarray,
    satellite_value: float,
    profit_margin: float = 0.20,
    base_rate_fee: float = 1000.0,
    kp_bump: float = 1.0,
    kp_upper_cap: float = 9.0,
    use_ceil_for_bump: bool = True,
    debug: bool = True
) -> dict:
    if daily_kp_forecast is None or len(daily_kp_forecast) == 0:
        return {"error": "Could not retrieve a valid Kp forecast."}
    max_kp_pred = float(np.max(daily_kp_forecast))
    bumped = max_kp_pred + kp_bump
    if use_ceil_for_bump:
        bumped = float(math.ceil(bumped))
    kp_used_for_risk_calc = float(min(bumped, kp_upper_cap))
    prob_of_anomaly = float(map_kp_to_anomaly_prob(kp_used_for_risk_calc))
    expected_loss = prob_of_anomaly * satellite_value
    final_premium = (expected_loss * (1.0 + profit_margin)) + base_rate_fee
    result = {
        "data_source": "NOAA 3-Day Geomagnetic Forecast (text product)",
        "worst_case_forecast": {
            "predicted_kp_max_next_24h": float(max_kp_pred),
            "kp_used_for_risk_calc": float(kp_used_for_risk_calc),
            "kp_bump_details": {
                "kp_bump_added": float(kp_bump),
                "used_ceil_on_bump": bool(use_ceil_for_bump),
                "kp_upper_cap": float(kp_upper_cap)
            }
        },
        "risk_assessment": {
            "satellite_value": satellite_value,
            "probability_of_anomaly": prob_of_anomaly,
            "expected_loss": expected_loss
        },
        "insurance_premium": {
            "profit_margin": profit_margin,
            "base_rate_fee": base_rate_fee,
            "premium_quote": final_premium
        },
        "formatted": {
            "satellite_value": f"${satellite_value:,.2f}",
            "probability_of_anomaly_pct": f"{prob_of_anomaly:.4%}",
            "expected_loss": f"${expected_loss:,.2f}",
            "premium_quote": f"${final_premium:,.2f}"
        }
    }
    if debug:
        print("\n[INFO] Premium calculation details:")
        print(json.dumps(result["worst_case_forecast"], indent=2))
        print(json.dumps(result["risk_assessment"], indent=2))
        print("Formatted:", result["formatted"])
    return result
def test_parser_with_sample_text(sample_text: str):
    lines = sample_text.splitlines()
    joined = " ".join(lines)
    normalized = re.sub(r'[,\t/]', ' ', joined)
    normalized = re.sub(r'\s+', ' ', normalized)
    timeslots = ["00-03UT", "03-06UT", "06-09UT", "09-12UT", "12-15UT", "15-18UT", "18-21UT", "21-00UT"]
    start_idx = normalized.find(timeslots[0])
    candidate_text = normalized[start_idx:] if start_idx != -1 else normalized
    tokens = re.findall(r'(?:\d{2}-\d{2}UT)|\d+\.\d+|\d+', candidate_text)
    idx = 0
    extracted = []
    for ts in timeslots:
        while idx < len(tokens) and tokens[idx] != ts:
            idx += 1
        if idx >= len(tokens):
            break
        idx += 1
        nums = []
        while idx < len(tokens) and not re.match(r'\d{2}-\d{2}UT', tokens[idx]) and len(nums) < 20:
            tok = tokens[idx]
            if re.match(r'^\d+(\.\d+)?$', tok):
                val = float(tok)
                if 0.0 <= val <= 10.0:
                    nums.append(val)
            idx += 1
        extracted.append(nums)
    if len(extracted) >= 8:
        first_col = [row[0] for row in extracted[:8]]
        return np.array(first_col, dtype=float)
    kp_lines = [ln for ln in lines if re.search(r'\bkp\b', ln, flags=re.IGNORECASE)]
    for ln in kp_lines:
        ln_norm = re.sub(r'[,\t/]', ' ', ln)
        ln_norm = re.sub(r'[-]+', ' ', ln_norm)
        toks = re.findall(r'\d+\.\d+|\d+', ln_norm)
        kps = [float(t) for t in toks if 0.0 <= float(t) <= 10.0]
        if len(kps) >= 8:
            return np.array(kps[:8], dtype=float)
    all_nums = re.findall(r'\d+\.\d+|\d+', normalized)
    kps_all = [float(n) for n in all_nums if 0.0 <= float(n) <= 10.0]
    if len(kps_all) >= 8:
        return np.array(kps_all[:8], dtype=float)
    return None
if __name__ == "__main__":
    SATELLITE_VALUE = 150_000_000.0
    print("Fetching live Kp forecast from NOAA's text product...")
    kp_forecast = get_noaa_forecast_from_txt(debug=True)
    if kp_forecast is None:
        print("\n[ERROR] Parsing failed to extract Kp values from NOAA forecast.")
        print("You can (1) run test_parser_with_sample_text() with a saved copy of the file,")
        print("or (2) inspect the NOAA URL manually:", "https://services.swpc.noaa.gov/text/3-day-geomag-forecast.txt")
    else:
        print("\n[OK] Forecast acquired. Kp values (3-hourly for next 24h):")
        print(kp_forecast)
        print("Highest Kp in forecast:", float(np.max(kp_forecast)))
        premium = calculate_premium_for_satellite(
            daily_kp_forecast=kp_forecast,
            satellite_value=SATELLITE_VALUE,
            profit_margin=0.20,
            base_rate_fee=10000.0,
            kp_bump=0.7,
            kp_upper_cap=9.0,
            use_ceil_for_bump=True,
            debug=True
        )
        print("\n--- Insurance Premium Calculation (final) ---")
        print(json.dumps(premium, indent=2))