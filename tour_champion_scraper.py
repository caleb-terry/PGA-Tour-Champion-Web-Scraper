import json
import argparse
import requests
from bs4 import BeautifulSoup
from datetime import datetime


def fetch_tour_data(year: int):
    """
    Fetches the content from the given URL.

    Parameters:
    - url (str): The URL to fetch the content from.

    Returns:
    - content: The content fetched from the URL, or None if an error occurs.
    """
    
    url = f"https://www.pgatour.com/schedule/{year}"
    
    try: # to get data
        response_data = requests.get(url, timeout=10)
        response_data.raise_for_status()
        soup = BeautifulSoup(response_data.content, "html.parser")

        data = soup.find("script", id="__NEXT_DATA__").string

        return data

    except requests.exceptions.Timeout:
        print("The request timed out")
    except requests.exceptions.HTTPError as e:
        print(f"HTTP error occurred: {e}")
    except requests.exceptions.RequestException as e:
        print(f"Error during request: {e}")


def parse_tour_schedule(data: str):
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
            month_name = month["month"]
            for tournament in month["tournaments"]:
                earnings_str = (
                    tournament.get("championEarnings", "$0")
                    .replace("$", "")
                    .replace(",", "")
                )
                earnings = float(earnings_str) if earnings_str.isdigit() else 0
                champions = tournament.get("champions", [])
                if champions: # are multiple, split the champion's earnings and add each champion as a new object in the array.
                    earnings_per_champion = earnings / len(champions)
                    for champion in champions:
                        champion_name = champion["displayName"]
                        tournament_name = tournament["tournamentName"]
                        if champion_name not in important_data:
                            important_data[champion_name] = [
                                [month_name, tournament_name, earnings_per_champion]
                            ]
                        else:
                            important_data[champion_name].append(
                                [month_name, tournament_name, earnings_per_champion]
                            )
        return json.dumps(important_data, indent=4)
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON data: {e}")


def present_tour_schedule(data: str):
    """
    Present the data in a user-friendly format.
    """
    data_dict = json.loads(data)
    for champion, tournaments in data_dict.items():
        print(f"\nChampion: {champion}")
        total_earnings = 0
        current_month = ""
        for tournament in tournaments:
            if current_month != tournament[0]:
                current_month = tournament[0]
                print(f"    Month: {current_month}")
            print(f"      Tournament: {tournament[1]} - Earnings: ${tournament[2]:,.2f}")
            total_earnings += tournament[2]
        print(f"Total Earnings: ${total_earnings:,.2f}")


def main():
   """
   Returns PGA champions for a given year.

   Parameters:
     --year = 
   """
    
    current_year = datetime.now().year
    
    parser = argparse.ArgumentParser(description='Fetch PGA Tour Schedule Data.')
    parser.add_argument('--year', type=int, help='Year to fetch data for', default=current_year)
    args = parser.parse_args()
    
    data = fetch_tour_data(args.year)
    schedule = parse_tour_schedule(data)
    present_tour_schedule(schedule)


if __name__ == "__main__":
    main()
