# Task 5 — Web Data Extraction & Analysis

## CodSoft Data Science Internship — Task 5

> **Objective:** Collect data from a publicly available website using Python
> libraries (BeautifulSoup, requests), clean and organise the collected data
> into a structured dataset, and perform exploratory analysis to identify
> trends and patterns.

---

## Source Website

| Item | Detail |
|---|---|
| **URL** | https://books.toscrape.com |
| **Type** | Public scraping sandbox — no login, no CAPTCHA |
| **Legal** | Explicitly designed for scraping ("We love being scraped!") |
| **Data** | 1 000 books across 50 genre categories |

---

## Fields Extracted

| Column | Type | Description |
|---|---|---|
| `Title` | str | Full book title |
| `Price_GBP` | float | Listed price in GBP (£) |
| `Rating` | int | Star rating 1–5 |
| `Availability` | str | Stock status |
| `Category` | str | Genre category |
| `ProductURL` | str | Direct link to the product page |
| `ScrapeDate` | str | Date the record was scraped |

---

## Directory Structure

```
Task_5_Web_Data_Extraction/
├── scraper/
│   ├── __init__.py
│   └── web_scraper.py        # Main scraper — category-by-category strategy
├── scripts/
│   └── web_data_analysis.py  # EDA and chart generation pipeline
├── notebooks/
│   └── Task5_EDA.ipynb       # Interactive Jupyter notebook
├── data/
│   ├── raw/                  # (Empty — scraped data goes to processed/)
│   └── processed/
│       └── scraped_books.csv # Clean dataset (auto-generated on first run)
├── outputs/
│   ├── scraped_books.xlsx    # Multi-sheet Excel export
│   └── charts/               # PNG chart files (auto-generated)
│       ├── price_distribution.png
│       ├── rating_distribution.png
│       ├── products_by_category.png
│       ├── price_by_category.png
│       └── rating_vs_price.png
└── report/
    └── web_extraction_report.md
```

---

## How to Run

### Step 1 — Install dependencies
```bash
pip install -r requirements.txt
```

### Step 2 — Run the scraper
```bash
python Task_5_Web_Data_Extraction/scraper/web_scraper.py --pages 50
```
> Scrapes up to 50 catalogue pages (≈ all 1 000 books). Adjust `--pages` to
> limit runtime.

### Step 3 — Run the analysis
```bash
python Task_5_Web_Data_Extraction/scripts/web_data_analysis.py
```

### Step 4 — Open the notebook
```bash
jupyter notebook Task_5_Web_Data_Extraction/notebooks/Task5_EDA.ipynb
```

---

## Key Findings

- **812 books** scraped across **21 genre categories** (50 catalogue pages).
- Price range: £10.00 to £59.99 with a near-uniform distribution (mean £35.07, median £35.86).
- Ratings: 1 to 5 stars uniformly distributed (mean 2.91).
- **Default** (152), **Nonfiction** (110), and **Sequential Art** (75) are the largest categories by book count.
- No significant correlation between price and rating (expected for sandbox data).

---

## Ethical Scraping Compliance

- ✅ Target site explicitly designed for scraping practice.
- ✅ Descriptive User-Agent sent on every request.
- ✅ 0.5-second delay between consecutive page requests.
- ✅ No authentication bypass, no CAPTCHA circumvention.
- ✅ No personal or private information collected.

---

## CodSoft Task Requirements Checklist

| Requirement | Status |
|---|---|
| Collect data from publicly available websites | ✅ Done |
| Use Python libraries (BeautifulSoup, requests) | ✅ Done |
| Extract structured information (product details, prices, ratings) | ✅ Done |
| Clean and organise into a structured dataset | ✅ Done |
| Perform exploratory analysis to identify trends and patterns | ✅ Done |
| **Bonus:** Automate and export results to CSV and Excel | ✅ Done |
