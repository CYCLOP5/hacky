import os
import re
import json
from crewai import Agent, Task, Crew, Process, LLM
from crewai_tools import SerperDevTool
from dotenv import load_dotenv

# Import our custom tools
from data_tools import SpaceWeatherTools
from risk_tools import RiskAssessmentTools

# --- Step 1: Load Environment Variables & Initialize LLM ---
load_dotenv()

# We will use the known working model name from the successful test run.
llm = LLM(
    model="gemini/gemini-2.5-flash",
    api_key=os.getenv("GEMINI_API_KEY")
)

# --- Step 2: Instantiate Tools ---
search_tool = SerperDevTool()
noaa_data_tool = SpaceWeatherTools()
risk_assessment_tool = RiskAssessmentTools()

# --- Step 3: Define the Agents to Test ---
# We need both Agent 1 and Agent 2 for this test, as Agent 2 depends on Agent 1's output.
data_ingestion_agent = Agent(
  role='Space Weather Data Analyst',
  goal='Fetch the latest space weather forecasts and any real-time contextual alerts relevant to satellite operations.',
  backstory=(
      "You are a specialized data analyst working for a leading cosmic weather insurance firm..."
  ),
  verbose=True,
  allow_delegation=False,
  tools=[noaa_data_tool, search_tool],
  llm=llm 
)

risk_assessment_agent = Agent(
  role='GEO Satellite Actuarial Analyst',
  goal='Analyze space weather data and asset details to determine the precise probability of an anomaly.',
  backstory=(
      "You are a senior actuary with deep expertise in astrophysics and satellite engineering..."
  ),
  verbose=True,
  allow_delegation=False,
  tools=[risk_assessment_tool],
  llm=llm
)

# --- Step 4: Define the Tasks to Test ---

# UPDATED: The data_task now has a more structured expected output (JSON).
# This makes the handoff between agents much more reliable.
data_task = Task(
  description=(
      "1. Execute the 'NOAA Space Weather Forecast Tool' to get the baseline Kp index forecast. "
      "2. Independently, use the 'Search' tool to perform a web search for 'latest NOAA space weather alerts'. "
      "3. Synthesize the information from both tools into a final report. The report must clearly state the maximum predicted Kp for the next 24 hours "
      "and summarize any breaking news or active alerts. If no alerts are found, state 'RAG Alert: None'."
  ),
  expected_output="A JSON object containing two keys: 'worst_case_kp' (a number) and 'real_time_context' (a string).",
  agent=data_ingestion_agent
)

# UPDATED: The risk_task now expects to receive JSON and parse it.
risk_task = Task(
  description=(
      "Parse the JSON report from the data analyst. Then, execute the 'GEO Satellite Risk Assessment Tool'. "
      "You must extract the `worst_case_kp` and `real_time_context` from the JSON and pass them as arguments to the tool. "
      "You must also use the following user-provided asset details: "
      "asset_value_millions: {asset_value_millions}, "
      "shielding_level: '{shielding_level}', "
      "years_in_orbit: {years_in_orbit}."
  ),
  expected_output="A JSON string with 'risk_category', 'reasoning', 'incident_probability', and 'confidence'.",
  agent=risk_assessment_agent,
  context=[data_task]
)


# --- Step 5: Assemble a Test Crew for the First Two Steps ---
test_crew = Crew(
  agents=[data_ingestion_agent, risk_assessment_agent],
  tasks=[data_task, risk_task],
  verbose=True,
  process=Process.sequential
)

# --- Step 6: Run the Test ---
if __name__ == '__main__':
    print("--- Starting Test for Risk Assessment Agent (Agent 2) ---")
    
    user_inputs = {
        'asset_value_millions': 300.0,
        'shielding_level': 'Hardened',
        'years_in_orbit': 2
    }
    
    print(f"Executing with sample inputs: {user_inputs}")
    result = test_crew.kickoff(inputs=user_inputs)
    
    print("\n\n--- Test Complete ---")
    print("Final Output from Risk Assessment Agent:")
    print("-----------------------------------------")
    print(result)

    # UPDATED: Changed .raw_output to .raw to fix the AttributeError
    if data_task.output:
        print("\nOutput from Data Agent (passed to Risk Agent):")
        print("---------------------------------------------")
        print(data_task.output.raw)

