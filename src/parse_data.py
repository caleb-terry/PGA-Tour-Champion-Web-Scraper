"""_summary_
"""

import json

# load ./data/pga_tour_schedule.json


def parse_tour_schedule(data: str):
    """
    Parses the data from the given string.

    Parameters:
    - data (str): The data to parse.

    Returns:
    - dict: The parsed data.
    """
    try:
        return json.loads(data)
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON data: {e}")


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
        for champion in all_data["props"]["pageProps"]["champions"]:
            important_data[champion["champion"]] = champion["championEarnings"]
        return json.dumps(important_data)
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON data: {e}")
