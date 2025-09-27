import os
import json
from crewai import Agent, Task, Crew, Process, LLM
from crewai_tools import SerperDevTool
from dotenv import load_dotenv

# Import all custom tools
from data_tools import SpaceWeatherTools
from risk_tools import RiskAssessmentTools
from cro_tools import PortfolioRiskTool
from pricing_tool import PricingTools

# --- Step 1: Load Environment Variables & Initialize LLM ---
load_dotenv()

# Initialize the LLM once and share it among all agents for efficiency
llm = LLM(
    model="gemini/gemini-2.5-flash",
    api_key=os.getenv("GEMINI_API_KEY")
)

# --- Step 2: Instantiate All Tools ---
search_tool = SerperDevTool()
noaa_data_tool = SpaceWeatherTools()
risk_assessment_tool = RiskAssessmentTools()
portfolio_risk_tool = PortfolioRiskTool()
pricing_tool = PricingTools()

# --- Step 3: Define the Full Team of Agents ---
data_ingestion_agent = Agent(
  role='Space Weather Data Analyst',
  goal='Fetch and synthesize the latest space weather forecasts and real-time alerts.',
  backstory='Expert in monitoring NOAA and other sources for critical space weather data.',
  verbose=True,
  tools=[noaa_data_tool, search_tool],
  llm=llm
)

risk_assessment_agent = Agent(
  role='GEO Satellite Actuarial Analyst',
  goal='Determine the precise incident probability for a single satellite based on its characteristics and the space weather forecast.',
  backstory='A senior actuary specializing in astrophysics and satellite engineering.',
  verbose=True,
  tools=[risk_assessment_tool],
  llm=llm
)

# --- NEW: The Chief Risk Officer Agent ---
cro_agent = Agent(
  role='Chief Risk Officer',
  goal='Analyze the entire insurance portfolio to assess total risk exposure and provide a strategic business recommendation.',
  backstory='You are the Chief Risk Officer, focused on the overall financial health and solvency of the company. Your word determines underwriting strategy.',
  verbose=True,
  tools=[portfolio_risk_tool],
  llm=llm
)

premium_pricing_agent = Agent(
  role='Pricing Specialist',
  goal='Synthesize individual risk and portfolio-level risk to calculate a final, commercially viable insurance premium.',
  backstory='You are a pricing specialist who must balance risk with market competitiveness, incorporating high-level strategic directives from the CRO.',
  verbose=True,
  tools=[pricing_tool],
  llm=llm
)

# --- Step 4: Define the Full, Multi-Step Workflow (Tasks) ---
# Each task builds upon the previous ones.
data_task = Task(
  description="Fetch the latest NOAA Kp index forecast and search for any real-time space weather alerts. Consolidate this into a structured JSON report.",
  expected_output="A JSON object with 'worst_case_kp' and 'real_time_context'.",
  agent=data_ingestion_agent
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
  context=[data_task]
)

# --- NEW: The CRO's Task ---
portfolio_task = Task(
  description=(
      "Conduct a full portfolio analysis. Use the `worst_case_kp` from the data analyst's report and the list of all currently insured assets in the `{portfolio}`. "
      "Execute your 'Portfolio Risk Analysis Tool' to determine the Probable Maximum Loss (PML) and provide a strategic business recommendation."
  ),
  expected_output="A JSON object with 'total_exposure_millions', 'probable_maximum_loss_millions', and a 'strategic_recommendation'.",
  agent=cro_agent,
  context=[data_task] # This task also depends on the initial data forecast
)

# --- UPDATED: The Final Pricing Task ---
# This task now uses context from BOTH the individual risk task and the CRO's portfolio task.
pricing_task = Task(
  description=(
      "Calculate the final 24-hour insurance premium for the new asset. You have two critical inputs: "
      "1. The individual incident probability for the new asset (from the actuarial analyst). "
      "2. The strategic recommendation for the entire portfolio (from the CRO). "
      "Synthesize these inputs. Apply surcharges based on the CRO's strategic recommendation: 'Apply Moderate Risk Surcharge' (75% surcharge), 'Apply High Risk Surcharge' (150% surcharge), 'Urgent Reinsurance Required' (200% surcharge), or 'Temporarily Halt New Policies' (400% surcharge). No surcharge for 'Continue Writing New Policies'. "
      "Then, execute the 'Insurance Premium Calculation Tool' using the new asset's details: "
      "incident_probability: [from risk_task], "
      "asset_value_millions: {asset_value_millions}, "
      "adjustment_factor: {adjustment_factor}. "
      "Clearly state the final premium and whether a portfolio-risk surcharge was applied in your final answer."
  ),
  expected_output="A final report detailing the calculated premium, including the base premium, any applied surcharge, and the final quote.",
  agent=premium_pricing_agent,
  context=[risk_task, portfolio_task] # This is the key change - it now depends on two previous tasks.
)

# --- Step 5: Assemble and Run the Full Crew ---
borealis_crew = Crew(
  agents=[data_ingestion_agent, risk_assessment_agent, cro_agent, premium_pricing_agent],
  tasks=[data_task, risk_task, portfolio_task, pricing_task],
  verbose=True,
  process=Process.sequential
)

def load_portfolio_from_file(filepath="portfolio_data.json"):
    try:
        with open(filepath, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"Could not load portfolio: {e}")
        return []

if __name__ == '__main__':
    print("--- Starting Full Borealis Insurance Workflow ---")
    
    portfolio_data = load_portfolio_from_file()
    
    if not portfolio_data:
        print("Stopping: Portfolio data is missing or empty.")
    else:
        # These are the inputs for the NEW policy we want to add
        new_policy_inputs = {
            'asset_value_millions': 400.0,
            'shielding_level': 'Standard',
            'years_in_orbit': 1,
            'adjustment_factor': 1.0,
            'portfolio': portfolio_data # The current portfolio is passed as context
        }
        
        print(f"Executing with new policy inputs: {new_policy_inputs}")
        
        result = borealis_crew.kickoff(inputs=new_policy_inputs)
        
        print("\n\n--- Full Workflow Complete ---")
        print("Final Output from Pricing Agent:")
        print("---------------------------------")
        print(result.raw)

