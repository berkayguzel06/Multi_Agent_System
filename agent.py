from smolagents import CodeAgent, LiteLLMModel, DuckDuckGoSearchTool
import agent_tools as at
import os
import dotenv

dotenv.load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
PROMPT_JSON_FILE = os.getenv("PROMPT_JSON_FILE")

if GEMINI_API_KEY is not None:
    os.environ["GEMINI_API_KEY"] = GEMINI_API_KEY
else:
    raise EnvironmentError("GEMINI_API_KEY environment variable is not set.")

visit_webpage = at.visit_webpage
create_file_if_not_exists = at.create_file_if_not_exists
create_folder_if_not_exists = at.create_folder_if_not_exists
is_prime = at.is_prime
sql_engine = at.sql_engine
get_database_column_info = at.get_database_column_info
write_findings_to_text_file = at.write_findings_to_text_file


model = LiteLLMModel(model_id="gemini/gemini-2.0-flash")

web_agent = CodeAgent(
    tools=[DuckDuckGoSearchTool(), visit_webpage],
    model=model,
    name="Web Agent",
    description="This agent can search the web and provide the results.",
)

code_agent = CodeAgent(
    tools=[write_findings_to_text_file,
           create_file_if_not_exists, create_folder_if_not_exists, is_prime],
    additional_authorized_imports=['pandas','statsmodels','sklearn','numpy','json',
                                   'matplotlib', 'os',"selenium", "requests", "markdownify",
                                    "selenium.webdriver.common.by", "selenium.webdriver.common.keys", "yfinance", "subprocess",
                                    "bs4"],
    name="Code Agent",
    description="This agent can run code snippets and provide the output.",
    model=model,
)

database_agent = CodeAgent(
    tools=[sql_engine, get_database_column_info],
    model=model,
    name="Database Agent",
    description="This agent can query a database and provide the results.",
)

code_prompt = """
    Check if the number 17 is a prime number and provide the result in cheerful way.
"""

search_prompt = """
    Search for the latest news on artificial intelligence.
"""

database_prompt = """
    Get the column information of the table 'users' from db 'WhatsappDB'.
"""

code_agent.run(code_prompt)
web_agent.run(search_prompt)
database_agent.run(database_prompt)
