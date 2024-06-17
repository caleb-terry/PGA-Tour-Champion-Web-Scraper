# Python Web Scraper - PGA Tour Champions and Earnings

This project is a Python web scraper that retrieves data from the PGA Tour Champions website and extracts information about players and their earnings.

## Installation

To use this web scraper, follow these steps:

1. Clone the repository to your local machine.
2. Install the required dependencies by running `pip install -r requirements.txt`.
3. Run the `tour_champion_scraper.py` script to start scraping the PGA Tour Champions website.

## Usage

The `tour_champion_scraper.py` script provides the following options:

- `--year`: Specify the year for which you want to retrieve earnings data.

Example usage:

```
python tour_champion_scraper.py --year 2024
```

**Note:** The script will retrieve data for the current year if no year is specified.

## Output

```
.\tour_champion_scraper.py --year 2022

Champion: Max Homa
    Month: September
      Tournament: Fortinet Championship - Earnings: $1,260,000.00
    Month: May
      Tournament: Wells Fargo Championship - Earnings: $1,620,000.00
Total Earnings: $2,880,000.00
```

## Contributing

Contributions are welcome! If you have any suggestions or improvements, please open an issue or submit a pull request.

## License
