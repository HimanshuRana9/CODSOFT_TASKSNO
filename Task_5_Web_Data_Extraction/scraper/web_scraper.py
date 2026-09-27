"""
Web Scraper — CodSoft Task 5: Web Data Extraction & Analysis
Target : https://books.toscrape.com  (public scraping sandbox, no login required)
Author : Himanshu Rana
Purpose: Scrape book listings (title, price, rating, availability, category)
         from every paginated catalogue page up to MAX_PAGES, then clean and
         export the structured dataset to CSV and Excel.

Ethical Scraping Notes:
  - books.toscrape.com is a publicly hosted demo site explicitly designed for
    web-scraping practice ("We love being scraped!").
  - No authentication, CAPTCHA bypass, or robots.txt violations are performed.
  - A descriptive User-Agent is supplied on every request.
  - A configurable delay (REQUEST_DELAY) is applied between consecutive page
    requests to avoid sending excessive traffic.
  - No private or personal information is collected.
"""

import time
import argparse
import logging
import re
from datetime import datetime
from pathlib import Path

import requests
from bs4 import BeautifulSoup
import pandas as pd

# ─── Logging ────────────────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger(__name__)

# ─── Configuration ───────────────────────────────────────────────────────────────
BASE_URL      = "https://books.toscrape.com/catalogue/"
START_URL     = "https://books.toscrape.com/catalogue/page-1.html"
MAX_PAGES     = 50           # 50 pages × 20 books = up to 1 000 books (full catalogue)
REQUEST_DELAY = 0.5          # seconds between consecutive page requests
REQUEST_TIMEOUT = 15         # HTTP timeout in seconds
USER_AGENT = (
    "Mozilla/5.0 (compatible; CodSoftTaskBot/1.0; "
    "+https://github.com/HimanshuRana9/CODSOFT_TASKSNO)"
)

# ─── Output paths ────────────────────────────────────────────────────────────────
PROJECT_ROOT  = Path(__file__).resolve().parent.parent
RAW_DIR       = PROJECT_ROOT / "data" / "raw"
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"
OUTPUTS_DIR   = PROJECT_ROOT / "outputs"

PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)

# ─── Rating word → numeric mapping ──────────────────────────────────────────────
RATING_MAP = {
    "One": 1,
    "Two": 2,
    "Three": 3,
    "Four": 4,
    "Five": 5,
}

# ─── Category page mapping (built from homepage sidebar) ─────────────────────────
CATEGORY_URL_MAP: dict[str, str] = {}   # populated lazily if needed


# ════════════════════════════════════════════════════════════════════════════════
# Helper: HTTP GET with error handling
# ════════════════════════════════════════════════════════════════════════════════
def _get(url: str) -> BeautifulSoup | None:
    """Fetch *url* and return a BeautifulSoup parse tree, or None on failure.

    Forces UTF-8 decoding regardless of the Content-Type charset header so
    that the £ sign (UTF-8: 0xC2 0xA3) is always decoded correctly.
    """
    try:
        response = requests.get(
            url,
            headers={"User-Agent": USER_AGENT},
            timeout=REQUEST_TIMEOUT,
        )
        response.raise_for_status()
        # Force UTF-8 — books.toscrape.com sends the £ sign as UTF-8 bytes
        # but the server may report charset as Latin-1 in its Content-Type.
        response.encoding = "utf-8"
        return BeautifulSoup(response.text, "html.parser")
    except requests.exceptions.Timeout:
        logger.warning("Request timed out: %s", url)
    except requests.exceptions.HTTPError as exc:
        logger.warning("HTTP error %s for %s", exc.response.status_code, url)
    except requests.exceptions.RequestException as exc:
        logger.warning("Request failed for %s — %s", url, exc)
    return None


# ════════════════════════════════════════════════════════════════════════════════
# Step 1: Build category map from homepage sidebar
# ════════════════════════════════════════════════════════════════════════════════
def build_category_map() -> dict[str, str]:
    """
    Scrape the homepage sidebar to build a mapping:
        category_slug → category_name
    e.g. "travel_2" → "Travel"
    This lets us annotate every book with its category during the main crawl.
    """
    logger.info("Building category map from homepage sidebar …")
    soup = _get("https://books.toscrape.com/")
    if soup is None:
        return {}

    cat_map: dict[str, str] = {}
    nav = soup.select("div.side_categories ul.nav.nav-list li > a")
    for anchor in nav:
        href = anchor.get("href", "")
        name = anchor.get_text(strip=True)
        # href pattern: catalogue/category/books/<slug>/index.html
        # or for "Books": catalogue/category/books_1/index.html  (skip root)
        if "category/books_" in href and "books/" not in href:
            continue  # skip the top-level "Books" entry
        slug_match = re.search(r"/books/(.+?)/index\.html", href)
        if slug_match and name and name != "Books":
            cat_map[slug_match.group(1)] = name

    logger.info("Found %d categories.", len(cat_map))
    return cat_map


# ════════════════════════════════════════════════════════════════════════════════
# Step 2: Assign category from the individual book URL slug
# ════════════════════════════════════════════════════════════════════════════════
def _infer_category(book_url: str, cat_map: dict[str, str]) -> str:
    """
    books.toscrape.com listing pages do not embed the category directly on the
    listing card.  We resolve it by fetching each book's detail page once to
    read the breadcrumb, but that would be 1 000 extra requests.

    Instead we build a per-category page list and annotate as we go.
    This function is a fallback for the global listing; category annotation
    happens during the category-by-category sweep below.
    """
    return "Unknown"


# ════════════════════════════════════════════════════════════════════════════════
# Step 3: Parse a single catalogue page (listing page)
# ════════════════════════════════════════════════════════════════════════════════
def parse_listing_page(soup: BeautifulSoup, category: str = "All") -> list[dict]:
    """Extract every book from a paginated listing page soup."""
    books: list[dict] = []

    for article in soup.select("article.product_pod"):
        book: dict = {}

        # --- Title ---
        h3_a = article.select_one("h3 > a")
        book["Title"] = h3_a.get("title", "").strip() if h3_a else None

        # --- Price (extract numeric value robustly) ---
        # The site encodes the £ symbol as UTF-8 bytes; we force UTF-8 in
        # _get() but use a regex here as belt-and-suspenders.
        price_tag = article.select_one("p.price_color")
        if price_tag:
            raw_price = price_tag.get_text(strip=True)
            price_match = re.search(r"[\d]+\.[\d]+", raw_price)
            if price_match:
                try:
                    book["Price_GBP"] = float(price_match.group())
                except ValueError:
                    book["Price_GBP"] = None
            else:
                book["Price_GBP"] = None
        else:
            book["Price_GBP"] = None

        # --- Star Rating (word class → int) ---
        rating_tag = article.select_one("p.star-rating")
        if rating_tag:
            classes = rating_tag.get("class", [])
            rating_word = next((c for c in classes if c != "star-rating"), None)
            book["Rating"] = RATING_MAP.get(rating_word, None)
        else:
            book["Rating"] = None

        # --- Availability ---
        avail_tag = article.select_one("p.instock.availability")
        book["Availability"] = avail_tag.get_text(strip=True) if avail_tag else "Unknown"

        # --- Book URL ---
        if h3_a:
            href = h3_a.get("href", "")
            book["ProductURL"] = "https://books.toscrape.com/catalogue/" + href.lstrip("../")
        else:
            book["ProductURL"] = None

        # --- Category (passed in from outer loop) ---
        book["Category"] = category

        if book["Title"]:   # discard malformed records without a title
            books.append(book)

    return books


# ════════════════════════════════════════════════════════════════════════════════
# Step 4: Crawl category by category (preferred strategy)
#         → avoids a second per-book detail request for category information
# ════════════════════════════════════════════════════════════════════════════════
def scrape_by_category(
    cat_map: dict[str, str],
    max_pages_total: int,
) -> list[dict]:
    """
    Iterate over each category, paginate its catalogue, and extract books with
    the correct category label already attached.
    """
    all_books: list[dict] = []
    pages_scraped = 0

    for slug, category_name in cat_map.items():
        if pages_scraped >= max_pages_total:
            logger.info("Reached MAX_PAGES limit (%d). Stopping.", max_pages_total)
            break

        # Category first page URL
        next_url = (
            f"https://books.toscrape.com/catalogue/category/books/{slug}/index.html"
        )
        cat_page = 1

        while next_url and pages_scraped < max_pages_total:
            logger.info(
                "Fetching [%s] page %d  (total pages so far: %d)  %s",
                category_name, cat_page, pages_scraped, next_url,
            )
            soup = _get(next_url)
            if soup is None:
                logger.warning("Failed to load page; skipping %s.", next_url)
                break

            books = parse_listing_page(soup, category=category_name)
            all_books.extend(books)
            pages_scraped += 1
            cat_page += 1

            # Follow "next" pagination link within this category
            next_btn = soup.select_one("li.next > a")
            if next_btn:
                href = next_btn.get("href", "")
                # Build absolute URL relative to category base
                base = next_url.rsplit("/", 1)[0] + "/"
                next_url = base + href
            else:
                next_url = None  # end of this category

            if next_url:
                time.sleep(REQUEST_DELAY)

    logger.info("Crawling complete: %d pages, %d raw book records.", pages_scraped, len(all_books))
    return all_books


# ════════════════════════════════════════════════════════════════════════════════
# Step 5: Clean the raw records
# ════════════════════════════════════════════════════════════════════════════════
def clean_data(raw: list[dict]) -> pd.DataFrame:
    """Apply all cleaning rules and return a structured DataFrame."""
    df = pd.DataFrame(raw)

    logger.info("--- Cleaning ---")
    logger.info("Raw records: %d", len(df))

    # Strip whitespace
    for col in ["Title", "Availability", "Category"]:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip()

    # Standardise availability
    df["Availability"] = df["Availability"].str.strip().replace("", "Unknown")

    # Drop rows without title or price
    before = len(df)
    df = df.dropna(subset=["Title", "Price_GBP"])
    logger.info("Dropped %d rows missing title/price.", before - len(df))

    # Remove duplicate rows (same Title + Price + Category)
    before = len(df)
    df = df.drop_duplicates(subset=["Title", "Price_GBP", "Category"])
    logger.info("Dropped %d duplicate rows.", before - len(df))

    # Validate numeric ranges
    df = df[df["Price_GBP"] > 0]

    # Rating must be 1–5 (or NaN)
    df = df[df["Rating"].isna() | df["Rating"].between(1, 5)]

    # Scraping timestamp (use datetime.now(UTC) to avoid deprecation warning)
    df["ScrapeDate"] = datetime.now().strftime("%Y-%m-%d")

    # Reset index
    df = df.reset_index(drop=True)

    logger.info("Clean records: %d", len(df))
    return df


# ════════════════════════════════════════════════════════════════════════════════
# Step 6: Save outputs
# ════════════════════════════════════════════════════════════════════════════════
def save_outputs(df: pd.DataFrame) -> None:
    """Save the cleaned dataset to CSV and Excel with multiple sheets."""
    csv_path = PROCESSED_DIR / "scraped_books.csv"
    df.to_csv(csv_path, index=False)
    logger.info("CSV saved: %s (%d rows)", csv_path, len(df))

    # Excel with three sheets
    xlsx_path = OUTPUTS_DIR / "scraped_books.xlsx"
    category_summary = (
        df.groupby("Category")
        .agg(
            BookCount=("Title", "count"),
            AvgPrice=("Price_GBP", "mean"),
            MinPrice=("Price_GBP", "min"),
            MaxPrice=("Price_GBP", "max"),
            AvgRating=("Rating", "mean"),
        )
        .round(2)
        .reset_index()
        .sort_values("BookCount", ascending=False)
    )

    summary_stats = pd.DataFrame(
        {
            "Metric": [
                "Total Books",
                "Unique Categories",
                "Min Price (£)",
                "Max Price (£)",
                "Mean Price (£)",
                "Median Price (£)",
                "Min Rating",
                "Max Rating",
                "Mean Rating",
                "Scrape Date",
            ],
            "Value": [
                len(df),
                df["Category"].nunique(),
                df["Price_GBP"].min(),
                df["Price_GBP"].max(),
                round(df["Price_GBP"].mean(), 2),
                round(df["Price_GBP"].median(), 2),
                df["Rating"].min(),
                df["Rating"].max(),
                round(df["Rating"].mean(), 2),
                df["ScrapeDate"].iloc[0],
            ],
        }
    )

    with pd.ExcelWriter(xlsx_path, engine="openpyxl") as writer:
        df.to_excel(writer, sheet_name="Books", index=False)
        summary_stats.to_excel(writer, sheet_name="Summary", index=False)
        category_summary.to_excel(writer, sheet_name="Category Analysis", index=False)

    logger.info("Excel saved: %s", xlsx_path)


# ════════════════════════════════════════════════════════════════════════════════
# Main entry point
# ════════════════════════════════════════════════════════════════════════════════
def main(max_pages: int = MAX_PAGES) -> pd.DataFrame:
    logger.info("=" * 65)
    logger.info("CodSoft Task 5 — Web Scraper: Books to Scrape")
    logger.info("Target   : https://books.toscrape.com")
    logger.info("Max pages: %d", max_pages)
    logger.info("=" * 65)

    # 1. Build category map
    cat_map = build_category_map()
    if not cat_map:
        logger.error("Category map is empty — cannot continue.")
        raise RuntimeError("Failed to build category map from homepage.")

    # 2. Scrape
    raw_records = scrape_by_category(cat_map, max_pages_total=max_pages)
    if not raw_records:
        raise RuntimeError("No records scraped — check connectivity.")

    # 3. Clean
    df = clean_data(raw_records)

    # 4. Save
    save_outputs(df)

    # 5. Summary
    logger.info("=" * 65)
    logger.info("SCRAPING COMPLETE")
    logger.info("Books scraped (clean): %d", len(df))
    logger.info("Categories found     : %d", df["Category"].nunique())
    logger.info("Price range          : £%.2f – £%.2f", df["Price_GBP"].min(), df["Price_GBP"].max())
    logger.info("Rating range         : %d – %d", int(df["Rating"].min()), int(df["Rating"].max()))
    logger.info("=" * 65)

    return df


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Scrape books.toscrape.com and export structured dataset."
    )
    parser.add_argument(
        "--pages",
        type=int,
        default=MAX_PAGES,
        help=f"Maximum number of pages to scrape (default: {MAX_PAGES})",
    )
    args = parser.parse_args()
    main(max_pages=args.pages)
