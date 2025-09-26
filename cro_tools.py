import os
import json
import math
import numpy as np
from crewai import LLM
from crewai.tools import BaseTool

# --- Actuarial Calculation Functions ---
# These functions are based on the logic you provided.
def map_kp_to_anomaly_prob(kp_index: float) -> float:
    """A deterministic logistic function to map Kp index to anomaly probability."""
    return 1.0 / (1.0 + np.exp(-1.5 * (kp_index - 7)))

# --- The CRO's Primary Tool ---
class PortfolioRiskTool(BaseTool):
    name: str = "Portfolio Risk Analysis Tool"
    description: str = (
        "Analyzes an entire portfolio of insured assets against a Kp forecast to determine "
        "the Probable Maximum Loss (PML) and provide a strategic recommendation. "
        "This is a high-level tool for the Chief Risk Officer."
    )

    def _run(self, worst_case_kp: float, portfolio: list) -> str:
        """
        The main execution method. It uses an LLM to reason through a complex,
        multi-step financial modeling task.
        """
        llm = LLM(model="gemini/gemini-2.0-flash", api_key=os.getenv("GEMINI_API_KEY"))
        
        portfolio_str = json.dumps(portfolio, indent=2)

        prompt = f"""
        You are a Chief Risk Officer (CRO) for a major space insurance firm. Your task is to conduct a portfolio-level risk analysis based on an incoming space weather forecast.

        **Forecast Data:**
        - Maximum Predicted Kp Index (next 24h): **{worst_case_kp}**

        **Current Active Insurance Portfolio:**
        ```json
        {portfolio_str}
        ```

        **Your Analytical Task & Reasoning Instructions:**
        1.  **Calculate Total Exposure:** First, sum the 'value_millions' for all assets to determine the total value at risk.
        2.  **Analyze Risk Correlation:** State that a single geomagnetic storm is a 100% correlated risk event for all GEO satellites in the portfolio.
        3.  **Model Probable Maximum Loss (PML):** You must calculate the total expected loss across the *entire portfolio*. For each satellite, perform the following calculation based on our firm's standard actuarial model:
            - **Start with the forecast:** `kp_forecast = {worst_case_kp}`
            - **Apply a risk bump:** `bumped_kp = ceil({worst_case_kp} + 1.0)`. This is a safety margin.
            - **Cap the risk:** `risk_kp = min(bumped_kp, 9.0)`.
            - **Calculate probability:** `probability = 1.0 / (1.0 + exp(-1.5 * (risk_kp - 7)))`.
            - **Calculate individual expected loss:** `expected_loss = probability * satellite_value_millions`.
            - **Sum the losses:** The PML is the sum of all individual expected losses.
        4.  **Provide Strategic Recommendation:** Based on the calculated PML relative to the total exposure, provide a clear, actionable recommendation.
            - If PML < 5% of total exposure: 'Continue Writing New Policies'.
            - If 5% <= PML <= 15% of total exposure: 'Temporarily Halt New Policies'.
            - If PML > 15% of total exposure: 'Urgent Reinsurance Required'.

        Your final answer MUST be ONLY a JSON object with keys: "total_exposure_millions", "probable_maximum_loss_millions", "strategic_recommendation", and "reasoning". In the 'reasoning' section, show your step-by-step calculations for the PML.
        """
        try:
            response = llm.call(prompt)
            return response
        except Exception as e:
            return f'{{"error": "Error during portfolio risk analysis: {e}"}}'
