import os
import pandas as pd
import matplotlib.pyplot as plt
import requests
from requests.exceptions import RequestException
from markdownify import markdownify
import re
from sqlalchemy import create_engine, text
from smolagents import tool

engine = create_engine("postgresql://postgres:1234@localhost:5432/WhatsappDB")

@tool
def visit_webpage(url: str) -> str:
    """Visits a webpage at the given URL and returns its content as a markdown string.

    Args:
        url: The URL of the webpage to visit.

    Returns:
        The content of the webpage converted to Markdown, or an error message if the request fails.
    """
    try:
        # Send a GET request to the URL
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for bad status codes

        # Convert the HTML content to Markdown
        markdown_content = markdownify(response.text).strip()

        # Remove multiple line breaks
        markdown_content = re.sub(r"\n{3,}", "\n\n", markdown_content)

        return markdown_content

    except RequestException as e:
        return f"Error fetching the webpage: {str(e)}"
    except Exception as e:
        return f"An unexpected error occurred: {str(e)}"

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

@tool
def get_database_column_info(dbName: str) -> str:
    """
    Get the column information of the database
    Args:
        dbName: Name of the database
    """
    with engine.connect() as con:
        query = f"SELECT column_name, data_type FROM information_schema.columns WHERE table_name = '{dbName}'"
        rows = con.execute(query)
        output = ""
        for row in rows:
            output += f"\n{row[0]}: {row[1]}"
    return output

@tool
def sql_engine(query: str) -> str:
    """
    Allows you to perform SQL queries on the table. Returns a string representation of the result.
    The table is named 'users'. Its description is as follows:
        Columns:
        - name: String
        - phone: Integer

    Args:
        query: The query to perform. This should be correct SQL.
    """
    output = ""
    with engine.connect() as con:
        rows = con.execute(text(query))
        for row in rows:
            output += "\n" + str(row)
    return output


@tool
def is_prime(n: int) -> bool:
    """
    Check if a number is a prime number.

    Args:
        n: The number to check.

    Returns:
        True if n is a prime number, False otherwise.
    """
    if n < 2:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True