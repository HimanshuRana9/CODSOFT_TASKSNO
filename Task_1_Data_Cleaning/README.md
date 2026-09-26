# Task 1 — Data Cleaning & Preprocessing

## Objective
Import a dataset using Python and inspect its structure. Identify missing values, duplicate records, inconsistent data entries and data-type issues. Clean the dataset with Pandas and save the result as a new CSV.

## Dataset
**UCI Online Retail II** — a two-year transactional dataset for a UK-based non-store online retailer. The UCI repository reports 1,067,371 instances and states that the dataset contains missing values.

Source:
https://archive.ics.uci.edu/dataset/502/online%2Bretail

## Pipeline
Raw dataset → inspection → quality report → cleaning → validation → cleaned CSV.

## Cleaning decisions
- Remove exact duplicate rows.
- Standardize column names.
- Convert `InvoiceDate` to datetime.
- Convert numeric fields to numeric types.
- Treat blank/whitespace-only descriptions as missing.
- Remove records without a usable `CustomerID` because customer identification is important for downstream customer analysis.
- Remove records with non-positive `Quantity` or `Price` from the sales-analysis dataset; cancellations/returns should be handled explicitly rather than treated as normal positive sales.
- Standardize text fields by trimming whitespace.
- Save the cleaned dataset separately from the raw data.

## Outputs
- `data/processed/online_retail_ii_cleaned.csv`
- `outputs/data_quality_before.csv`
- `outputs/data_quality_after.csv`
