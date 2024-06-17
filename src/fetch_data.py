"""
This script scrapes the PGA Tour schedule and prints the top 5 winners of the season.
It also prints the number of regular wins, major wins, and money earned.
"""

import requests
from bs4 import BeautifulSoup


def fetch_data(url: str):
    """
    Fetches the content from the given URL.

    Parameters:
    - url (str): The URL to fetch the content from.

    Returns:
    - content: The content fetched from the URL, or None if an error occurs.
    """
    try:
        response_data = requests.get(url, timeout=10)
        response_data.raise_for_status()  # Raises HTTPError for bad responses

        soup = BeautifulSoup(response_data.content, "html.parser")

        data = soup.find("script", id="__NEXT_DATA__").string

        return data

    except requests.exceptions.Timeout:
        print("The request timed out")
    except requests.exceptions.HTTPError as e:
        print(f"HTTP error occurred: {e}")  # Specific HTTP error
    except requests.exceptions.RequestException as e:
        print(f"Error during request: {e}")  # Superclass for all requests exceptions
