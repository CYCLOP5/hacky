import os
from crewai import Agent, Task, Crew, Process, LLM
from crewai_tools import SerperDevTool
from dotenv import load_dotenv

# Import our custom tools
from data_tools import SpaceWeatherTools

# --- Step 1: Load Environment Variables & Initialize LLM ---
load_dotenv()

# UPDATED: Using CrewAI's native LLM class for initialization.
# This approach is cleaner and more integrated with the framework.
# The model name should still include the 'gemini/' prefix.
llm = LLM(
    model="gemini/gemini-2.0-flash" ,
    api_key=os.getenv("GEMINI_API_KEY")
)

# --- Step 2: Instantiate Tools ---
search_tool = SerperDevTool()
noaa_data_tool = SpaceWeatherTools()

# --- Step 3: Define the Agent to Test ---
data_ingestion_agent = Agent(
  role='Space Weather Data Analyst',
  goal='Fetch the latest space weather forecasts and any real-time contextual alerts relevant to satellite operations.',
  backstory=(
      "You are a specialized data analyst working for a leading cosmic weather insurance firm. "
      "Your primary responsibility is to monitor NOAA's Space Weather Prediction Center and other "
      "relevant sources to provide the most current and accurate data for risk assessment. "
      "You understand the urgency and precision required in this field."
  ),
  verbose=True,
  allow_delegation=False,
  tools=[noaa_data_tool, search_tool],
  llm=llm 
)

# --- Step 4: Define the Task to Test ---
data_task = Task(
  description=(
      "1. Execute the 'NOAA Space Weather Forecast Tool' to get the baseline Kp index forecast. "
      "2. Independently, use the 'Search' tool to perform a web search for 'latest NOAA space weather alerts'. "
      "3. Synthesize the information from both tools into a final report. The report must clearly state the maximum predicted Kp for the next 24 hours "
      "and summarize any breaking news or active alerts found in the web search. If no alerts are found, state 'RAG Alert: None'."
  ),
  expected_output="A comprehensive report including the worst-case 24-hour Kp index as a number, and a text summary of real-time alerts from your web search.",
  agent=data_ingestion_agent
)

# --- Step 5: Assemble a Test Crew ---
test_crew = Crew(
  agents=[data_ingestion_agent],
  tasks=[data_task],
  verbose=True,
  process=Process.sequential
)

# --- Step 6: Run the Test ---
if __name__ == '__main__':
    print("--- Starting Test for Data Ingestion Agent ---")
    
    result = test_crew.kickoff(inputs={})
    
    print("\n\n--- Test Complete ---")
    print("Final Output from Data Ingestion Agent:")
    print("-----------------------------------------")
    print(result)

