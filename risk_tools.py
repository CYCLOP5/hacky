import os
import re
from crewai.tools import BaseTool
from crewai import LLM

class RiskAssessmentTools(BaseTool):
    name: str = "GEO Satellite Risk Assessment Tool"
    description: str = (
        "Analyzes space weather data and satellite characteristics to determine the precise "
        "probability of an anomaly for a specific geostationary satellite."
    )

    def _run(
        self, 
        worst_case_kp: str, 
        real_time_context: str, 
        asset_value_millions: float, 
        shielding_level: str, 
        years_in_orbit: int
    ) -> str:
        
        llm = LLM(
            model="gemini/gemini-2.0-flash",
            temperature=0.2,
            api_key=os.getenv("GEMINI_API_KEY")
        )

        # Extract Kp index
        kp_value_match = re.search(r"(\d+\.\d+)", worst_case_kp)
        if not kp_value_match:
            try:
                kp_value = float(worst_case_kp)
            except (ValueError, TypeError):
                return "Error: Could not parse Kp value from input."
        else:
            kp_value = float(kp_value_match.group(1))

        prompt = f"""
            Analyze the following insurance case for a 24-hour policy. You are an expert space weather actuary. Your task is to calculate a precise incident probability.

            **Geophysical Data:**
            - Maximum Predicted Kp Index (next 24h): {kp_value}
            - Current Real-Time Alerts from Web Search: {real_time_context}

            **Asset Details:**
            - Asset Type: Geostationary (GEO) Satellite
            - Asset Value: ${asset_value_millions:,.0f} Million USD
            - Shielding Level: '{shielding_level}'
            - Years in Orbit: {years_in_orbit}

            **Risk Modeling Instructions:**
            1.  **Baseline Risk Profile:** GEO satellites are primarily vulnerable to surface charging anomalies. The base probability of an anomaly follows a non-linear logistic curve based on the Kp index. A Kp index of 7 represents a 50% probability midpoint. The risk is negligible below Kp 4 but grows rapidly above Kp 5.
            2.  **Asset-Specific Adjustments:**
                - A 'Hardened' shielding level should significantly decrease the base probability (e.g., by 40-50%).
                - A 'Light/Legacy' shielding should increase it (e.g., by 30-40%).
                - For every year in orbit, slightly increase the risk to account for material degradation (e.g., 1-2% increase per year).
            3.  **Contextual Adjustment:** The presence of an active G-scale storm watch or other real-time alerts from the web search is a critical factor. If a significant alert is present, you MUST increase the final probability to reflect this heightened, immediate risk.
            4.  **Reasoning:** Provide a brief, clear rationale for how you combined these factors to reach your final probability.
            5.  **Final Output:** Based on all the above, calculate and provide a precise 'incident_probability'.

            Your final answer MUST be a JSON object with the following keys: "risk_category", "reasoning", "incident_probability", "confidence".
            Example: {{"risk_category": "Moderate", "reasoning": "Kp is elevated...", "incident_probability": 0.025, "confidence": 0.95}}
            """

        try:
            # CrewAI’s LLM is callable
            response = llm.call(prompt)
            return response  # already string content
        except Exception as e:
            return f"Error during LLM call for risk assessment: {e}"


