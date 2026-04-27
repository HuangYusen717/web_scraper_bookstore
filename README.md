# Book Website Scraper (Books to Scrape)

A lightweight Python scraping project that collects book data from [Books to Scrape](https://books.toscrape.com/) and saves it to `data.csv`.

This project is a good practice example for:
- Getting started with web scraping (`requests` + `BeautifulSoup`)
- Learning multi-page crawling
- Exporting structured data to CSV

## Features

- Page-by-page scraping (default: pages 1 to 50)
- Automatically extracts: page number, title, price, and availability
- Handles request errors and non-200 status codes
- Exports CSV in UTF-8 BOM encoding (Excel-friendly)

## Tech Stack

- Python 3.8+
- requests
- beautifulsoup4

## Project Structure

```text
pachong1/
├─ scraper.py      # Main scraper script
├─ data.csv        # Scraped output (generated/overwritten after running)
└─ README.md
```

## Quick Start

### 1. Clone the repository

```bash
git clone <your-repo-url>
cd pachong1
```

### 2. Install dependencies

```bash
pip install requests beautifulsoup4
```

### 3. Run the script

```bash
python scraper.py
```

After execution, `data.csv` will be generated (or overwritten) in the project root.

## Output Fields

`data.csv` contains the following columns:

- `Page`: source page number
- `Title`: book title
- `Price`: book price
- `Availability`: stock status

Sample (excerpt):

```csv
Page,Title,Price,Availability
1,A Light in the Attic,£51.77,In stock
1,Tipping the Velvet,£53.74,In stock
```

## Configurable Options

You can adjust these values in `scraper.py`:

- `START_PAGE`: starting page (default `1`)
- `END_PAGE`: ending page (default `50`)
- `BASE_PAGE_URL`: pagination URL template

If you only want to scrape the first 5 pages, change `END_PAGE = 50` to `END_PAGE = 5`.

## Notes

- This project is for learning purposes only. Please follow the target website's robots policy and terms of use.
- Running the script will overwrite the existing `data.csv`. Back it up first if needed.

## Possible Improvements

- Add more fields such as rating, category, and detail page URL
- Add randomized delay and retry logic
- Support CLI arguments (for custom page range and output filename)
- Save data to a database (SQLite / MySQL)

---

If this project helps you, feel free to give it a Star.

