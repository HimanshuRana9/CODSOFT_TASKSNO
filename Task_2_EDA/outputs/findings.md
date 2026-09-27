# Task 2 — Exploratory Data Analysis (EDA) Findings

**Project:** CodSoft Data Analytics Internship Portfolio  
**Task:** Task 2 — Exploratory Data Analysis  
**Author:** Himanshu Rana  
**Status:** Completed & Validated  
**Dataset Source:** `Task_1_Data_Cleaning/data/processed/online_retail_ii_cleaned.csv`  

---

## 1. Dataset Overview
- **Total Valid Records:** 779,425 rows across 9 features.
- **Completeness:** 0 missing values, 0 duplicate records.
- **Temporal Span:** 2009-12-01 to 2011-12-09 (24 full months).
- **Total Portfolio Revenue:** £17,374,804.25
- **Total Units Sold:** 10,513,952 units.
- **Unique Invoices / Transactions:** 36,969
- **Unique Active Customers:** 5,878
- **Unique Products (SKUs):** 4,631
- **Unique Countries:** 41

---

## 2. Descriptive Statistics Summary

| Feature | Mean | Median | Std Dev | Min | 25% | 75% | Max |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Quantity** | 13.49 | 6.00 | 145.86 | 1 | 2 | 12 | 80995 |
| **Price (£)** | £3.22 | £1.95 | £29.68 | £0.00 | £1.25 | £3.75 | £10953.50 |
| **TotalPrice (£)** | £22.29 | £12.48 | £227.43 | £0.00 | £4.95 | £19.80 | £168469.60 |

**Analytical Note:**  
All three continuous variables exhibit positive skewness (Mean > Median). The median line revenue is £12.48 while the mean is £22.29, indicating that high-volume wholesale orders pull the average upward.

---

## 3. Revenue Trends Over Time
- **Highest Revenue Month:** **2010-11** with **£1,166,460.02** (2,587 transactions).
- **Lowest Revenue Month:** **2011-02** with **£446,084.92** (997 transactions).
- **Seasonality Pattern:** Pronounced revenue spikes occur every September to November leading into the holiday season (Q4 surge), followed by normal contraction in early Q1.

---

## 4. Geographic Analysis
- **Dominant Market:** The **United Kingdom** accounts for **£14,389,234.90** (**82.82%** of total global revenue).
- **Top International Markets:**
  1. **EIRE:** £616,570.54 (567 transactions)
  2. **Netherlands:** £554,038.09 (228 transactions)
  3. **Germany:** £425,019.71 (789 transactions)
  4. **France:** £348,768.96 (614 transactions)

---

## 5. Top Products by Revenue
- **Top Product:** `22423` — **REGENCY CAKESTAND 3 TIER**
  - Generated **£277,656.25** across **24,124 units** and **3,317 orders**.
- Top 5 Products Account for substantial cumulative turnover, reflecting high demand for recurring decorative gift items.

---

## 6. Variable Relationships & Correlations
- **Correlation Matrix:**
  - `Quantity` vs `TotalPrice`: **0.8272** (Moderate positive correlation, volume strongly drives revenue)
  - `Price` vs `TotalPrice`: **0.1360** (Slight positive correlation)
  - `Quantity` vs `Price`: **-0.0049** (Slight negative correlation, higher unit prices correspond with smaller order batch quantities)

---

## 7. Outlier Detection (IQR Method)
- **Quantity Outliers:** 51,119 records (6.56% of dataset above 27 units).
- **Price Outliers:** 65,463 records (8.4% of dataset above £7.50).
- **TotalPrice Outliers:** 63,562 records (8.15% of dataset above £42.08).

**Important Insight:** These observations are statistical outliers under the IQR method. They should be investigated as potentially unusual but valid transactions rather than automatically removed.

---

## 8. Answers to Core Business Questions

| # | Business Question | Computed Answer |
| :-: | :--- | :--- |
| **Q1** | How many transactions are in the dataset? | **36,969 unique orders** |
| **Q2** | How many unique customers are represented? | **5,878 verified accounts** |
| **Q3** | How many products are represented? | **4,631 unique product SKUs** |
| **Q4** | Which country generates the highest revenue? | **United Kingdom (£14,389,234.90, 82.82% share)** |
| **Q5** | Which product/stock code generates the highest revenue? | **22423 — REGENCY CAKESTAND 3 TIER (£277,656.25)** |
| **Q6** | Which month has the highest revenue? | **2010-11 (£1,166,460.02)** |
| **Q7** | Which month has the lowest revenue? | **2011-02 (£446,084.92)** |
| **Q8** | What is the average transaction line revenue? | **£22.29 (Median: £12.48)** |
| **Q9** | What are the major outliers? | **Bulk orders exceeding 27 units and line values over £42.08 (B2B wholesale transactions)** |
| **Q10** | What relationships exist between Quantity, Price and TotalPrice? | **Quantity is the strongest driver of TotalPrice (r = 0.8272); unit price has low correlation with quantity (r = -0.0049)** |

---

## 9. Key Findings & Strategic Takeaways
1. **Strong UK Concentration:** The business is heavily UK-centric (>80% turnover). International expansion offers considerable upside in high-AOV European markets (EIRE, Netherlands, Germany).
2. **Q4 Seasonality Domination:** Q4 generates massive sales surges; inventory planning and logistics must scale up between August and October.
3. **Wholesale Core:** While average retail ticket is modest (~£12.48), a small tier of bulk B2B clients drives outsized revenue. This directly motivates Task 4 Customer Segmentation (RFM analysis).
