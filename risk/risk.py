def get_satellite_risk(kp_forecast, dst_forecast):
    risk_score = 0
    risk_description = "No significant risk"
    potential_impacts = ["Normal satellite operations expected."]

    if kp_forecast >= 9:
        risk_score = 5
        risk_description = "G5 - Extreme Geomagnetic Storm"
        potential_impacts = [
            "Extensive surface charging on satellite components.",
            "Potential for communication uplink/downlink issues.",
            "Problems with satellite tracking and orientation."
        ]
    elif kp_forecast >= 8:
        risk_score = 4
        risk_description = "G4 - Severe Geomagnetic Storm"
        potential_impacts = [
            "Widespread surface charging on satellite components.",
            "Potential problems with satellite tracking and orientation."
        ]
    elif kp_forecast >= 7:
        risk_score = 3
        risk_description = "G3 - Strong Geomagnetic Storm"
        potential_impacts = [
            "Surface charging may occur on satellite components.",
            "Increased drag on low-Earth-orbit (LEO) satellites."
        ]
    elif kp_forecast >= 6:
        risk_score = 2
        risk_description = "G2 - Moderate Geomagnetic Storm"
        potential_impacts = [
            "Minor impact on satellite operations possible.",
            "Surface charging may begin to affect some satellite components."
        ]
    elif kp_forecast >= 5:
        risk_score = 1
        risk_description = "G1 - Minor Geomagnetic Storm"
        potential_impacts = ["Minor impact on satellite operations possible."]

    if dst_forecast < -100 and risk_score > 0:
        risk_score += 1 
        potential_impacts.append("Intense ring current (indicated by Dst) may increase anomaly risk.")

    return {
        "risk_score": min(risk_score, 5), 
        "risk_description": risk_description,
        "potential_impacts": potential_impacts
    }

if __name__ == '__main__':

    future_kp = 1.2
    future_dst = 121

    risk_assessment = get_satellite_risk(future_kp, future_dst)

    print("--- Satellite Risk Assessment ---")
    print(f"Forecasted Kp: {future_kp}")
    print(f"Forecasted Dst: {future_dst}")
    print("\nRisk Score (0-5):", risk_assessment["risk_score"])
    print("Risk Description:", risk_assessment["risk_description"])
    print("\nPotential Impacts:")
    for impact in risk_assessment["potential_impacts"]:
        print(f"- {impact}")