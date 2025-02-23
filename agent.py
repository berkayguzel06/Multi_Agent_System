from smolagents import CodeAgent, tool, LiteLLMModel, DuckDuckGoSearchTool
import pandas as pd
import matplotlib.pyplot as plt
import os
import json
import dotenv

dotenv.load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
PROMPT_JSON_FILE = os.getenv("PROMPT_JSON_FILE")

if GEMINI_API_KEY is not None:
    os.environ["GEMINI_API_KEY"] = GEMINI_API_KEY
else:
    raise EnvironmentError("GEMINI_API_KEY environment variable is not set.")

# Get Promt json file "prompt.json"
prompts = json.load(open(PROMPT_JSON_FILE))

model = LiteLLMModel(model_id="gemini/gemini-2.0-flash")

@tool
def create_file_if_not_exists(path: str) -> None:
    """
    Create file if not exists
    Args:
        path: Path to file
    """
    if not os.path.exists(path):
        open(path, 'w').close()

@tool
def create_folder_if_not_exists(path: str) -> None:
    """
    Create folder if not exists
    Args:
        path: Path to folder
    """
    if not os.path.exists(path):
        os.makedirs(path)

@tool
def load_csv_from_path(path: str) -> pd.DataFrame:
    """
    Look at the path and load csv data from path
    Args:
        path: Path to csv file
    """
    return pd.read_csv(path)

@tool
def add_matplotlib_plot_to_file(plot: plt.Figure, path: str) -> None:
    """
    Add matplotlib plot to file
    Args:
        plot: Matplotlib plot
        path: Path to save plot
    """
    plot.savefig(path)

@tool
def write_findings_to_text_file(findings: str, path: str) -> None:
    """
    Write findings to text file
    Args:
        findings: Findings
        path: Path to save findings
    """
    with open(path, 'w') as file:
        file.write(findings)

web_agent = CodeAgent(
    tools=[DuckDuckGoSearchTool()],
    model=model,
    name=prompts['prompts'][2]['type'],
    description=prompts['prompts'][2]['description'],
    prompt_templates={
        "system_prompt": prompts['prompts'][2]['prompt'],
    }
)

code_agent = CodeAgent(
    tools=[write_findings_to_text_file,
           create_file_if_not_exists, create_folder_if_not_exists],
    additional_authorized_imports=['pandas','statsmodels','sklearn','numpy','json',
                                   'matplotlib', 'os',"selenium", "requests", "markdownify",
                                    "selenium.webdriver.common.by", "selenium.webdriver.common.keys", "yfinance", "subprocess",
                                    "bs4"],
    name=prompts['prompts'][1]['type'],
    description=prompts['prompts'][1]['description'],
    model=model,
    prompt_templates={
        "system_prompt": prompts['prompts'][1]['prompt'],
    }
)

management_agent = CodeAgent(
    tools=[],
    model=model,
    managed_agents=[web_agent, code_agent],
    name=prompts['prompts'][3]["type"],
    description=prompts['prompts'][3]["description"],
    prompt_templates={
        "system_prompt": prompts['prompts'][3]['prompt'],
    }
)

prompt = """
    Can you write a pyhton script that can help me to find the best stock to invest in?
    Then save the python file in the current directory.
"""

code_agent.run(prompt)