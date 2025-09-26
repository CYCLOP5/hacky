import numpy as np

def map_kp_to_anomaly_prob(kp_index):

    prob = 1 / (1 + np.exp(-1.5 * (kp_index - 5.5)))
    return prob

def calculate_premium_for_satellite(daily_forecasts, satellite_value):


    PROFIT_MARGIN = 0.20
    BASE_RATE_FEE = 1000

    worst_case = daily_forecasts.loc[daily_forecasts['y_pred'].idxmax()]

    max_kp_pred = worst_case['y_pred']
    kp_upper_bound = worst_case['ub']

    prob_of_anomaly = map_kp_to_anomaly_prob(kp_upper_bound)

    expected_loss = prob_of_anomaly * satellite_value

    final_premium = (expected_loss * (1 + PROFIT_MARGIN)) + BASE_RATE_FEE

    return {
        "selected_date": str(worst_case['date'].date()),
        "worst_case_forecast": {
            "predicted_kp": round(max_kp_pred, 2),
            "kp_95_confidence_upper": round(kp_upper_bound, 2),
            "observed_kp_actual": round(worst_case['y_obs'], 2)
        },
        "risk_assessment": {
            "satellite_value": f"${satellite_value:,.2f}",
            "probability_of_anomaly": f"{prob_of_anomaly:.2%}",
            "expected_loss": f"${expected_loss:,.2f}"
        },
        "insurance_premium": {
            "premium_quote_usd": f"${final_premium:,.2f}"
        },
        "assumptions": {
            "profit_margin": f"{PROFIT_MARGIN:.0%}",
            "base_rate_fee": f"${BASE_RATE_FEE:,.2f}"
        }
    }