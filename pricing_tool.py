import os
import json
import math
import numpy as np
from crewai import LLM
from crewai.tools import BaseTool

# This function is now part of the pricing tool's internal knowledge
def map_kp_to_anomaly_prob(kp_index: float) -> float:
    """A deterministic logistic function to map Kp index to anomaly probability."""
    return 1.0 / (1.0 + np.exp(-1.5 * (kp_index - 7)))

class PricingTools(BaseTool):
    name: str = "Strategic Insurance Premium Calculation Tool"
    description: str = (
        "Calculates a final, strategically-adjusted insurance premium. It synthesizes the "
        "individual asset risk with the high-level portfolio risk recommendation from the CRO."
    )

    def _run(self, individual_risk_assessment: str, portfolio_risk_assessment: str, asset_value_millions: float) -> str:
        """
        The main execution method for the pricing tool. It uses an LLM to synthesize inputs and calculate a final premium.
        """
        llm = LLM(model="gemini/gemini-2.0-flash", api_key=os.getenv("GEMINI_API_KEY"))

        prompt = f"""
        You are a senior pricing actuary. Your final task is to calculate a 24-hour insurance premium for a new satellite policy.
        You must synthesize two key reports: the detailed risk assessment for the individual satellite, and the high-level strategic recommendation from our Chief Risk Officer regarding the entire company portfolio.

        **Report 1: Individual Asset Risk Assessment:**
        ```json
        {individual_risk_assessment}
        ```

        **Report 2: CRO's Portfolio-Level Strategic Recommendation:**
        ```json
        {portfolio_risk_assessment}
        ```

        **Asset Details:**
        - Satellite Value: ${asset_value_millions:,.0f} Million USD

        **Your Calculation & Reasoning Instructions:**
        1.  **Extract Base Probability:** From the 'Individual Asset Risk Assessment', extract the `incident_probability`.
        2.  **Calculate Base Premium:** Use our firm's standard pricing formula to calculate a base premium. The formula is: `final_premium = (expected_loss * 1.20) + 10000.0`, where `expected_loss = probability * satellite_value`.
        3.  **Apply Strategic Surcharge (Crucial):** Analyze the `strategic_recommendation` from the CRO.
            - If the recommendation is 'Temporarily Halt New Policies', apply a **50% surcharge** to the base premium.
            - If the recommendation is 'Urgent Reinsurance Required', apply a **150% surcharge** to the base premium.
            - If the recommendation is 'Continue Writing New Policies', apply no surcharge.
        4.  **Provide Final Quote and Reasoning:** Your final output must be a JSON object with the keys "final_premium_usd" and "reasoning". The reasoning must clearly explain the base premium calculation and detail any strategic surcharge applied based on the CRO's recommendation.
        """
        try:
            response = llm.call(prompt)
            return response
        except Exception as e:
            return f'{{"error": "Error during final premium calculation: {e}"}}'

