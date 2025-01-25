"""
Returns PGA champions for a given year.

Parameters:
    --year: The year to fetch data for. Default is the current year.
    
Usage:
    python tour_champion_scraper.py --year 2021
"""

import logging
from typing import Dict, List, Optional, Union
from datetime import datetime
import json
import argparse
import requests
from bs4 import BeautifulSoup

# Constants
BASE_URL = "https://www.pgatour.com/schedule/{}"
TIMEOUT_SECONDS = 10
MIN_VALID_YEAR = 2012

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


class TourScraperError(Exception):
    """Custom exception for Tour Scraper errors"""


def fetch_tour_data(year: int) -> Optional[str]:
    """
    Fetches the content from the given URL.

    Parameters:
        year (int): The year to fetch data for

    Returns:
        Optional[str]: The JSON data as string if successful, None otherwise

    Raises:
        TourScraperError: If data cannot be fetched or parsed
    """
    url = BASE_URL.format(year)

    try:
        response_data = requests.get(url, timeout=TIMEOUT_SECONDS)
        response_data.raise_for_status()
        soup = BeautifulSoup(response_data.content, "html.parser")

        data = soup.find("script", id="__NEXT_DATA__")
        if not data or not data.string:
            raise TourScraperError("No tour data found for specified year")

        return data.string

    except requests.exceptions.Timeout:
        logging.error("The request timed out")
    except requests.exceptions.HTTPError as e:
        logging.error("HTTP error occurred: %s", e)
    except requests.exceptions.RequestException as e:
        logging.error("Error during request: %s", e)
    return None


def parse_tour_schedule(
    data: str,
) -> Optional[Dict[str, List[List[Union[str, float]]]]]:
    """
    Parses the tour schedule data.

    Parameters:
        data (str): The JSON data string to parse

    Returns:
        Optional[Dict[str, List[List[Union[str, float]]]]]: Dictionary with champion data
        or None if parsing fails
    """
    if not data:
        logging.error("No data provided to parse")
        return None

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
                earnings_per_champion = earnings / len(champions) if champions else 0
                for champion in champions:
                    champion_name = champion["displayName"]
                    tournament_name = tournament["tournamentName"]
                    important_data.setdefault(champion_name, []).append(
                        [month_name, tournament_name, earnings_per_champion]
                    )
        return important_data
    except json.JSONDecodeError as e:
        logging.error("Error parsing JSON data: %s", e)
        return None
    except KeyError as e:
        logging.error("Missing required key in data: %s", e)
        return None


def present_tour_schedule(schedule: Dict[str, List[List[Union[str, float]]]]) -> None:
    """
    Present the data in a user-friendly format.

    Parameters:
        schedule (Dict[str, List[List[Union[str, float]]]]): Dictionary containing tour schedule data
    """
    for champion, tournaments in schedule.items():
        print(f"\nChampion: {champion}")
        total_earnings = 0
        current_month = ""
        for tournament in tournaments:
            if current_month != tournament[0]:
                current_month = tournament[0]
                print(f"    Month: {current_month}")
            print(
                f"      Tournament: {tournament[1]} - Earnings: ${tournament[2]:,.2f}"
            )
            total_earnings += tournament[2]
        print(f"Total Earnings: ${total_earnings:,.2f}")


def valid_year(year: str) -> int:
    """
    Validate the input year.

    Parameters:
        year (str): The year to validate

    Returns:
        int: The validated year

    Raises:
        argparse.ArgumentTypeError: If year is invalid
    """
    current_year = datetime.now().year
    try:
        year_int = int(year)
        if len(year) != 4 or year_int <= MIN_VALID_YEAR or year_int > current_year:
            raise ValueError
        return year_int
    except ValueError as exc:
        raise argparse.ArgumentTypeError(
            f"Invalid year: {year}. Year must be between {MIN_VALID_YEAR} and {current_year}."
        ) from exc


def main():
    """Main entry point of the script."""
    current_year = datetime.now().year

    parser = argparse.ArgumentParser(description="Fetch PGA Tour Schedule Data.")
    parser.add_argument(
        "--year",
        type=valid_year,
        help=f"The year to fetch data for (between {MIN_VALID_YEAR} and current year). Default is current year.",
        default=current_year,
    )
    args = parser.parse_args()

    try:
        data = fetch_tour_data(args.year)
        if not data:
            raise TourScraperError("Failed to fetch tour data")

        schedule = parse_tour_schedule(data)
        if not schedule:
            raise TourScraperError("Failed to parse tour schedule")

        present_tour_schedule(schedule)

    except TourScraperError as e:
        logging.error(str(e))
        return 1

    return 0


if __name__ == "__main__":
    exit(main())
