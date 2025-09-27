import os
import json
from crewai import Agent, Task, Crew, Process, LLM
from dotenv import load_dotenv

from pricing_tool import PricingTools

# --- Step 1: Load Environment Variables & Initialize LLM ---
load_dotenv()

llm = LLM(
    model="gemini/gemini-2.5-flash",
    api_key=os.getenv("GEMINI_API_KEY")
)

# --- Step 2: Instantiate the Tool to be Tested ---
pricing_tool = PricingTools()

# --- Step 3: Define the Agent to Test ---
premium_pricing_agent = Agent(
  role='Strategic Pricing Actuary',
  goal='Synthesize individual risk and portfolio-level risk to calculate a final, commercially viable insurance premium.',
  backstory='You are a pricing specialist who must balance risk with market competitiveness, incorporating high-level strategic directives from the CRO.',
  verbose=True,
  allow_delegation=False,
  tools=[pricing_tool],
  llm=llm
)

# --- Step 4: Define the Task to Test ---
# The description instructs the agent on how to use its inputs and tool.
pricing_task = Task(
  description=(
      "Calculate the final 24-hour insurance premium for a new asset. You have two critical reports as input: "
      "1. The 'individual_risk_assessment' for the new asset. "
      "2. The 'portfolio_risk_assessment' from the CRO. "
      "You must synthesize these inputs by passing them to your 'Strategic Insurance Premium Calculation Tool'. "
      "Use the asset_value_millions of {asset_value_millions}."
  ),
  expected_output="A final JSON report detailing the calculated premium and the reasoning, including any applied surcharges.",
  agent=premium_pricing_agent
)

# --- Step 5: Assemble the Test Crew ---
test_crew = Crew(
  agents=[premium_pricing_agent],
  tasks=[pricing_task],
  verbose=True,
  process=Process.sequential
)

# --- Step 6: Run the Test ---
if __name__ == '__main__':
    print("--- Starting Test for Strategic Pricing Agent (Agent 4) ---")

    # --- MOCK DATA: Simulate the output from the previous two agents ---
    # This is what the Risk Agent would have produced for the new policy
    mock_individual_risk_report = json.dumps({
      "risk_category": "Severe",
      "reasoning": "The Kp index of 8.7 is extremely high, indicating a severe geomagnetic storm. Even with hardened shielding, the probability of an anomaly is significant.",
      "incident_probability": 0.85, # A very high probability for this test case
      "confidence": 0.96
    })

    # This is what the CRO Agent would have produced for the entire portfolio
    mock_portfolio_risk_report = json.dumps({
      "total_exposure_millions": 825.0,
      "probable_maximum_loss_millions": 289.21,
      "strategic_recommendation": "Apply High Risk Surcharge",
      "reasoning": "The PML of $289.21M represents over 35% of our total portfolio exposure. This is a critical risk level."
    })
    
    # These are the user inputs for the new policy being priced
    test_inputs = {
        'individual_risk_assessment': mock_individual_risk_report,
        'portfolio_risk_assessment': mock_portfolio_risk_report,
        'asset_value_millions': 400.0,
    }
    
    print("\nExecuting with the following simulated inputs:")
    print(f"Individual Risk Report: {mock_individual_risk_report}")
    print(f"Portfolio Risk Report: {mock_portfolio_risk_report}")
        
    result = test_crew.kickoff(inputs=test_inputs)
    
    print("\n\n--- Test Complete ---")
    print("Final Output from Pricing Agent:")
    print("---------------------------------")
    try:
        result_json = json.loads(result.raw)
        print(json.dumps(result_json, indent=2))
    except (json.JSONDecodeError, AttributeError):
        print("Could not parse the final result as JSON. Raw output:")
        print(result)
