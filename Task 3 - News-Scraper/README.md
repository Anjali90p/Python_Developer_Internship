# News Headlines Scraper

A Python script to scrape the top headlines from a news website (BBC News) and save them into a text file.

## Features
- Fetches HTML content using the `requests` library.
- Parses the HTML and extracts `<h2>` headline tags using `BeautifulSoup`.
- Cleans and filters the text data.
- Automates data collection by saving the headlines into a `headlines.txt` file.

## Requirements
- Python 3
- `requests`
- `beautifulsoup4`

## How to Run
1. Install dependencies:
   ```bash
   pip install requests beautifulsoup4
   ```
2. Run the script:
   ```bash
   python scraper.py
   ```
3. Check the `headlines.txt` file for the output.
