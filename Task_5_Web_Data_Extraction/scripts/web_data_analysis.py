"""
Web Data Analysis Pipeline — CodSoft Task 5
Author : Himanshu Rana
Purpose: Loads the scraped book dataset, performs exploratory data analysis,
         generates visualisations, and prints a summary report.
"""

import sys
from pathlib import Path
from datetime import datetime
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Ensure UTF-8 output on Windows consoles if supported
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

# ─── Aesthetics ──────────────────────────────────────────────────────────────────
sns.set_theme(style="whitegrid", palette="muted")
plt.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["DejaVu Sans", "Arial", "Segoe UI"],
    "axes.titlesize": 14,
    "axes.labelsize": 12,
    "xtick.labelsize": 10,
    "ytick.labelsize": 10,
})

# ─── Paths ───────────────────────────────────────────────────────────────────────
BASE_DIR    = Path(__file__).resolve().parent.parent
DATA_PATH   = BASE_DIR / "data" / "processed" / "scraped_books.csv"
CHARTS_DIR  = BASE_DIR / "outputs" / "charts"
CHARTS_DIR.mkdir(parents=True, exist_ok=True)

RATING_LABELS = {1: "1 Star", 2: "2 Stars", 3: "3 Stars",
                 4: "4 Stars", 5: "5 Stars"}


# ════════════════════════════════════════════════════════════════════════════════
def load_and_validate(path: Path) -> pd.DataFrame:
    """Load scraped CSV and assert integrity."""
    if not path.exists():
        raise FileNotFoundError(
            f"Dataset not found at {path}. "
            "Please run 'python scraper/web_scraper.py' first."
        )
    df = pd.read_csv(path)
    assert df["Title"].notna().all(),    "Unexpected NaN titles after cleaning."
    assert df["Price_GBP"].notna().all(),"Unexpected NaN prices after cleaning."
    assert (df["Price_GBP"] > 0).all(),  "Non-positive prices found."
    return df


# ════════════════════════════════════════════════════════════════════════════════
def descriptive_stats(df: pd.DataFrame) -> None:
    """Print descriptive statistics."""
    print("\n--- Descriptive Statistics -----------------------------------------")
    print(df[["Price_GBP", "Rating"]].describe(percentiles=[0.25, 0.50, 0.75, 0.95]).round(2))

    print("\n--- Category Count --------------------------------------------------")
    cat_counts = df["Category"].value_counts()
    print(cat_counts.to_string())

    print("\n--- Rating Distribution ---------------------------------------------")
    print(df["Rating"].value_counts().sort_index().to_string())

    print("\n--- Availability ----------------------------------------------------")
    print(df["Availability"].value_counts().to_string())


# ════════════════════════════════════════════════════════════════════════════════
def chart_price_distribution(df: pd.DataFrame) -> None:
    fig, ax = plt.subplots(figsize=(11, 5))
    sns.histplot(df["Price_GBP"], bins=40, kde=True, color="#2980b9",
                 edgecolor="white", ax=ax)
    ax.axvline(df["Price_GBP"].median(), color="#e74c3c", ls="--", lw=2,
               label=f"Median £{df['Price_GBP'].median():.2f}")
    ax.axvline(df["Price_GBP"].mean(), color="#27ae60", ls=":", lw=2,
               label=f"Mean £{df['Price_GBP'].mean():.2f}")
    ax.set_title("Book Price Distribution (GBP)", fontweight="bold", pad=12)
    ax.set_xlabel("Price (GBP)")
    ax.set_ylabel("Number of Books")
    ax.legend(frameon=True)
    plt.tight_layout()
    path = CHARTS_DIR / "price_distribution.png"
    fig.savefig(path, dpi=300)
    plt.close(fig)
    print(f"  Saved: {path.name}")


# ════════════════════════════════════════════════════════════════════════════════
def chart_rating_distribution(df: pd.DataFrame) -> None:
    rating_counts = df["Rating"].value_counts().sort_index()
    labels = [RATING_LABELS.get(int(r), str(r)) for r in rating_counts.index]
    colours = ["#e74c3c", "#e67e22", "#f1c40f", "#2ecc71", "#3498db"]

    fig, ax = plt.subplots(figsize=(9, 5))
    bars = ax.bar(labels, rating_counts.values, color=colours, edgecolor="white",
                  linewidth=1.2)
    ax.set_title("Book Rating Distribution", fontweight="bold", pad=12)
    ax.set_xlabel("Star Rating")
    ax.set_ylabel("Number of Books")
    for bar in bars:
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 2,
                f"{int(bar.get_height()):,}", ha="center", fontweight="bold", fontsize=10)
    plt.tight_layout()
    path = CHARTS_DIR / "rating_distribution.png"
    fig.savefig(path, dpi=300)
    plt.close(fig)
    print(f"  Saved: {path.name}")


# ════════════════════════════════════════════════════════════════════════════════
def chart_products_by_category(df: pd.DataFrame) -> None:
    cat_counts = df["Category"].value_counts().head(20)
    fig, ax = plt.subplots(figsize=(12, 7))
    sns.barplot(x=cat_counts.values, y=cat_counts.index,
                palette="viridis", hue=cat_counts.index, legend=False, ax=ax)
    ax.set_title("Top 20 Book Categories by Number of Books", fontweight="bold", pad=12)
    ax.set_xlabel("Number of Books")
    ax.set_ylabel("Category")
    for p in ax.patches:
        w = p.get_width()
        ax.text(w + 0.3, p.get_y() + p.get_height() / 2, f"{int(w):,}",
                va="center", fontsize=9, fontweight="bold")
    ax.set_xlim(0, cat_counts.max() * 1.15)
    plt.tight_layout()
    path = CHARTS_DIR / "products_by_category.png"
    fig.savefig(path, dpi=300)
    plt.close(fig)
    print(f"  Saved: {path.name}")


# ════════════════════════════════════════════════════════════════════════════════
def chart_price_by_category(df: pd.DataFrame) -> None:
    top_cats = df["Category"].value_counts().head(15).index
    df_top = df[df["Category"].isin(top_cats)]

    avg_price = (df_top.groupby("Category")["Price_GBP"]
                 .mean()
                 .sort_values(ascending=False)
                 .reset_index())

    fig, ax = plt.subplots(figsize=(12, 6))
    sns.barplot(data=avg_price, x="Price_GBP", y="Category",
                palette="rocket", hue="Category", legend=False, ax=ax)
    ax.set_title("Average Book Price by Category (Top 15 Categories)", fontweight="bold", pad=12)
    ax.set_xlabel("Average Price (GBP)")
    ax.set_ylabel("Category")
    for p in ax.patches:
        w = p.get_width()
        ax.text(w + 0.2, p.get_y() + p.get_height() / 2, f"£{w:.2f}",
                va="center", fontsize=9, fontweight="bold")
    plt.tight_layout()
    path = CHARTS_DIR / "price_by_category.png"
    fig.savefig(path, dpi=300)
    plt.close(fig)
    print(f"  Saved: {path.name}")


# ════════════════════════════════════════════════════════════════════════════════
def chart_rating_vs_price(df: pd.DataFrame) -> None:
    df_plot = df.dropna(subset=["Rating"])
    palette = {1: "#e74c3c", 2: "#e67e22", 3: "#f1c40f", 4: "#2ecc71", 5: "#3498db"}

    fig, ax = plt.subplots(figsize=(11, 6))
    for rating, grp in df_plot.groupby("Rating"):
        ax.scatter(grp["Price_GBP"], grp["Rating"] + np.random.uniform(-0.15, 0.15, len(grp)),
                   label=RATING_LABELS.get(int(rating), str(rating)),
                   color=palette.get(int(rating), "#7f8c8d"),
                   alpha=0.55, s=30, edgecolors="none")

    ax.set_title("Rating vs. Price (Jitter Added for Visibility)", fontweight="bold", pad=12)
    ax.set_xlabel("Price (GBP)")
    ax.set_ylabel("Star Rating")
    ax.set_yticks([1, 2, 3, 4, 5])
    ax.set_yticklabels(["1 Star", "2 Stars", "3 Stars", "4 Stars", "5 Stars"])
    ax.legend(title="Rating", bbox_to_anchor=(1.02, 1), loc="upper left", frameon=True)
    plt.tight_layout()
    path = CHARTS_DIR / "rating_vs_price.png"
    fig.savefig(path, dpi=300)
    plt.close(fig)
    print(f"  Saved: {path.name}")


# ════════════════════════════════════════════════════════════════════════════════
def main() -> None:
    print("=" * 65)
    print("TASK 5 - WEB DATA ANALYSIS PIPELINE")
    print("=" * 65)

    df = load_and_validate(DATA_PATH)
    print(f"\nLoaded {len(df):,} cleaned book records from {DATA_PATH.name}")

    descriptive_stats(df)

    print("\n--- Generating Charts ----------------------------------------------")
    chart_price_distribution(df)
    chart_rating_distribution(df)
    chart_products_by_category(df)
    chart_price_by_category(df)
    chart_rating_vs_price(df)

    print("\n=== DATA QUALITY SUMMARY ===========================================")
    print(f"  Records loaded       : {len(df):,}")
    print(f"  Unique categories    : {df['Category'].nunique()}")
    print(f"  Missing Price_GBP    : {df['Price_GBP'].isna().sum()}")
    print(f"  Missing Rating       : {df['Rating'].isna().sum()}")
    print(f"  Duplicate rows       : {df.duplicated().sum()}")
    print(f"  Price range          : GBP {df['Price_GBP'].min():.2f} - GBP {df['Price_GBP'].max():.2f}")
    print(f"  Mean price           : GBP {df['Price_GBP'].mean():.2f}")
    print(f"  Median price         : GBP {df['Price_GBP'].median():.2f}")
    print(f"  Rating range         : {int(df['Rating'].min())} - {int(df['Rating'].max())}")
    print(f"  Mean rating          : {df['Rating'].mean():.2f}")
    print(f"  Scrape date          : {df['ScrapeDate'].iloc[0]}")
    print("=" * 65)
    print("Analysis complete. Charts saved to outputs/charts/")


if __name__ == "__main__":
    main()
