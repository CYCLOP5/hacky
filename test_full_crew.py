import os
import json
from crewai import Agent, Task, Crew, Process, LLM
from crewai_tools import SerperDevTool
from dotenv import load_dotenv

# Import all custom tools from their respective files
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

cro_agent = Agent(
  role='Chief Risk Officer',
  goal='Analyze the entire insurance portfolio to assess total risk exposure and provide a strategic business recommendation.',
  backstory='You are the Chief Risk Officer, focused on the overall financial health and solvency of the company. Your word determines underwriting strategy.',
  verbose=True,
  tools=[portfolio_risk_tool],
  llm=llm
)

premium_pricing_agent = Agent(
  role='Strategic Pricing Actuary',
  goal='Synthesize individual and portfolio risk to calculate a final, commercially viable insurance premium.',
  backstory='You are a pricing specialist who must balance risk with market conditions and strategic directives from the CRO.',
  verbose=True,
  tools=[pricing_tool],
  llm=llm
)

# --- Step 4: Define the Full, Multi-Step Workflow (Tasks) ---
data_task = Task(
  description="Fetch the Kp forecast and search for alerts. Consolidate into a JSON report.",
  expected_output="A JSON object with 'worst_case_kp' and 'real_time_context'.",
  agent=data_ingestion_agent
)

risk_task = Task(
  description=(
      "Analyze the risk for a single GEO satellite. Use the data from the previous task and the following asset details: "
      "asset_value_millions: {asset_value_millions}, "
      "shielding_level: '{shielding_level}', "
      "years_in_orbit: {years_in_orbit}. "
  ),
  expected_output="A JSON string with the 'incident_probability' for the new asset.",
  agent=risk_assessment_agent,
  context=[data_task]
)

portfolio_task = Task(
  description=(
      "Conduct a full portfolio analysis. Use the `worst_case_kp` from the data analyst's report and the list of all currently insured assets in the `{portfolio}`. "
      "Execute your 'Portfolio Risk Analysis Tool'."
  ),
  expected_output="A JSON object with 'total_exposure_millions', 'probable_maximum_loss_millions', and a 'strategic_recommendation'.",
  agent=cro_agent,
  context=[data_task] # This task also depends on the initial data forecast
)

pricing_task = Task(
  description=(
      "Calculate the final 24-hour insurance premium for the new asset. You have two critical reports as input: "
      "1. The individual risk assessment for the new asset (the output of the risk_task). "
      "2. The portfolio-level risk assessment from the CRO (the output of the portfolio_task). "
      "You must synthesize these inputs by passing them to your 'Strategic Insurance Premium Calculation Tool'. "
      "Use the asset_value_millions of {asset_value_millions}."
  ),
  expected_output="A final JSON report detailing the calculated premium and the reasoning, including any applied surcharges.",
  agent=premium_pricing_agent,
  context=[risk_task, portfolio_task] # Depends on both previous tasks
)

# --- Step 5: Assemble the Full Crew ---
borealis_crew = Crew(
  agents=[data_ingestion_agent, risk_assessment_agent, cro_agent, premium_pricing_agent],
  tasks=[data_task, risk_task, portfolio_task, pricing_task],
  verbose=True,
  process=Process.sequential
)

# --- Helper function to load portfolio data ---
def load_portfolio_from_file(filepath="portfolio_data.json"):
    try:
        with open(filepath, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"Could not load portfolio: {e}")
        return []

# --- Main execution block ---
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
            'portfolio': portfolio_data # The current portfolio is passed as context
        }
        
        print(f"\nExecuting with new policy inputs: {new_policy_inputs}")
        
        # Kickoff the full workflow
        result = borealis_crew.kickoff(inputs=new_policy_inputs)
        
        print("\n\n--- Full Workflow Complete ---")
        print("Final Output from Pricing Agent:")
        print("---------------------------------")
        try:
            # The final result is the raw output of the last task
            result_json = json.loads(result.raw)
            print(json.dumps(result_json, indent=2))
        except (json.JSONDecodeError, AttributeError):
            print("Could not parse the final result as JSON. Raw output:")
            print(result)
