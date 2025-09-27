import os
import json
from crewai import Agent, Task, Crew, Process, LLM
from dotenv import load_dotenv

# Import the new CRO tool
from cro_tools import PortfolioRiskTool

# --- Step 1: Load Environment Variables & Initialize LLM ---
load_dotenv()

llm = LLM(
    model="gemini/gemini-2.5-flash",
    api_key=os.getenv("GEMINI_API_KEY")
)

# --- Step 2: Instantiate Tools ---
portfolio_risk_tool = PortfolioRiskTool()

# --- Step 3: Define the Agent to Test ---
cro_agent = Agent(
  role='Chief Risk Officer',
  goal='Analyze the entire insurance portfolio to assess total risk exposure and determine capital adequacy.',
  backstory=(
      "You are the Chief Risk Officer of a leading cosmic weather insurance firm. "
      "You are not concerned with individual policies but with the overall health and "
      "solvency of the company's entire book of business. Your analysis guides the "
      "company's high-level strategy."
  ),
  verbose=True,
  allow_delegation=False,
  tools=[portfolio_risk_tool],
  llm=llm
)

# --- Step 4: Define the Task to Test ---
portfolio_task = Task(
  description=(
      "Execute the 'Portfolio Risk Analysis Tool'. You must use the provided "
      "`worst_case_kp` and the full `portfolio` list as arguments for the tool."
  ),
  expected_output="A JSON object with 'total_exposure_millions', 'probable_maximum_loss_millions', and 'strategic_recommendation'.",
  agent=cro_agent
)

# --- Step 5: Assemble and Run the Test Crew ---
test_crew = Crew(
  agents=[cro_agent],
  tasks=[portfolio_task],
  verbose=True,
  process=Process.sequential
)

def load_portfolio_from_file(filepath="portfolio_data.json"):
    """Helper function to load the portfolio from the JSON file."""
    try:
        with open(filepath, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: Portfolio file not found at {filepath}")
        return []
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from {filepath}")
        return []

if __name__ == '__main__':
    print("--- Starting Test for Chief Risk Officer (CRO) Agent ---")
    
    # Load the portfolio from the file you created on the Canvas
    portfolio_data = load_portfolio_from_file()
    
    if not portfolio_data:
        print("Could not run test because portfolio data is empty or missing.")
    else:
        # These inputs would normally come from the Data Agent and the app's state
        test_inputs = {
            'worst_case_kp': 8.7,  # Simulating a severe storm forecast
            'portfolio': portfolio_data
        }
        
        print(f"Executing with a severe Kp forecast of {test_inputs['worst_case_kp']}...")
        print("Portfolio under analysis:")
        print(json.dumps(test_inputs['portfolio'], indent=2))
        
        result = test_crew.kickoff(inputs=test_inputs)
        
        print("\n\n--- Test Complete ---")
        print("Final Output from CRO Agent:")
        print("-----------------------------------------")
        try:
            # CORRECTED: We access the .raw attribute of the result object
            # before passing it to json.loads()
            result_json = json.loads(result.raw)
            print(json.dumps(result_json, indent=2))
        except (json.JSONDecodeError, AttributeError):
            print("Could not parse the final result as JSON. Raw output:")
            print(result)

