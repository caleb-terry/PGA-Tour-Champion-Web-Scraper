"""_summary_
"""

# from src.fetch_data import fetch_data
# from src.parse_data import parse_tour_schedule
# from src.present_data import present_tour_schedule
import json
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


def parse_tour_champion_earnings(data: str):
    """
    Parses the data from the given string.

    Parameters:
    - data (str): The data to parse.

    Returns:
    - dict: The parsed data.
    """
    try:
        all_data = json.loads(data)
        important_data = {}
        for month in all_data["props"]["pageProps"]["schedule"]["completed"]:
            for tournament in month["tournaments"]:
                earnings_str = (
                    tournament.get("championEarnings", "$0")
                    .replace("$", "")
                    .replace(",", "")
                )
                earnings = float(earnings_str) if earnings_str.isdigit() else 0
                champions = tournament.get("champions", [])
                if champions:
                    earnings_per_champion = earnings / len(champions)
                    for champion in champions:
                        champion_name = champion["displayName"]
                        tournament_name = tournament["tournamentName"]
                        # Check if the champion already exists in the dictionary
                        if champion_name not in important_data:
                            important_data[champion_name] = [
                                [tournament_name, earnings_per_champion]
                            ]
                        else:
                            important_data[champion_name].append(
                                [tournament_name, earnings_per_champion]
                            )
        return json.dumps(important_data, indent=4)  # Pretty print the JSON
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON data: {e}")


def present_tour_schedule(data: str):
    """
    Present the data in a user-friendly format.
    """
    for champion in json.loads(data):
        print(champion)
        for tournament in json.loads(data)[champion]:
            print(f"{tournament[0]} - {tournament[1]}")


# from src.present_data import present_data
def main():
    """_summary_"""
    url = "https://www.pgatour.com/schedule"
    data = fetch_data(url)
    schedule = parse_tour_champion_earnings(data)
    present_tour_schedule(schedule)


if __name__ == "__main__":
    main()
