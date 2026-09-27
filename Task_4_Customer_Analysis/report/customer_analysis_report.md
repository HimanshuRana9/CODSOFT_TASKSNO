# Customer Data Analysis Report

**Project:** CodSoft Data Analytics Internship — Task 4  
**Author:** Himanshu Rana  
**Repository:** `CODSOFT_TASKSNO`  
**Dataset:** Online Retail II (Cleaned Analytical Base)  

---

## 1. Objective

The objective of Task 4 is to examine customer-level purchasing data to understand behavioral patterns, evaluate geographic dispersion, execute behavioral customer segmentation, identify the most commercially valuable customer groups, and formulate targeted, data-backed marketing strategies.

---

## 2. Dataset

The analysis is conducted on the validated, deduplicated, and business-filtered multi-year retail transactions dataset from Task 1:

- **Source File:** `Task_1_Data_Cleaning/data/processed/online_retail_ii_cleaned.csv`
- **Total Validated Transactions:** 779,425 sales line items
- **Time Horizon:** 2009-12-01 to 2011-12-09 (24 consecutive calendar months)
- **Customer Population:** 5,878 unique verified accounts (`CustomerID`)
- **Total Portfolio Revenue:** £17,374,804.25
- **Total Sales Orders:** 36,969 distinct invoices
- **Total Inventory Units Sold:** 10,513,952 items

---

## 3. Customer Purchasing Behavior

Aggregating transactional records into discrete customer accounts (1 row per `CustomerID`) reveals key behavioral metrics:

| Metric | Mean | Median (50%) | 25th Percentile | 75th Percentile | 95th Percentile | Maximum |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Total Revenue (£)** | £2,955.90 | £867.74 | £342.28 | £2,248.31 | £9,292.05 | £580,987.04 |
| **Total Orders** | 6.29 | 3.00 | 1.00 | 7.00 | 22.00 | 398.00 |
| **Average Order Value (£)** | £385.18 | £279.24 | £176.68 | £414.90 | £959.08 | £84,236.25 |
| **Average Units / Order** | 247.56 | 153.59 | 91.00 | 256.92 | 682.35 | 87,167.00 |
| **Recency (Days)** | 201.33 | 96.00 | 26.00 | 380.00 | 664.00 | 739.00 |
| **Customer Lifetime (Days)**| 273.02 | 220.50 | 0.00 | 511.00 | 708.00 | 738.00 |

### Behavioral Highlights:
1. **High Positive Skew:** Mean revenue (£2,955.90) is over 3.4× the median revenue (£867.74), reflecting a classic retail Pareto distribution where high-volume commercial accounts drive the monetary upper tail.
2. **Order Cadence:** 50% of customers placed 3 or fewer orders over the two-year period, while the top 5% placed 22 or more repeat orders.
3. **Transaction Recency:** Over 50% of the customer base ordered within the last 96 days of the recorded timeline; however, the long right tail (mean recency 201 days) underscores substantial customer churn or dormancy.

---

## 4. Geographic Analysis

Customers were analyzed by their registered geographic locations across **41 unique nations**:

| Country | Customer Count | Total Orders | Total Units | Total Revenue (£) | Avg Revenue / Customer | Avg Order Value (£) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **United Kingdom** | 5,350 | 33,542 | 8,532,412 | £14,389,436.46 | £2,689.61 | £429.00 |
| **EIRE** | 4 | 566 | 318,020 | £616,368.98 | £154,092.24 | £1,088.99 |
| **Netherlands** | 22 | 228 | 383,879 | £554,038.09 | £25,183.55 | £2,429.99 |
| **Germany** | 106 | 788 | 225,123 | £424,922.66 | £4,008.70 | £539.24 |
| **France** | 95 | 616 | 270,352 | £349,107.36 | £3,674.81 | £566.73 |
| **Australia** | 14 | 93 | 103,711 | £169,207.79 | £12,086.27 | £1,819.44 |
| **Spain** | 38 | 147 | 49,336 | £106,684.82 | £2,807.50 | £725.75 |
| **Switzerland** | 22 | 100 | 53,622 | £103,262.74 | £4,693.76 | £1,032.63 |
| **Sweden** | 19 | 104 | 88,495 | £91,515.82 | £4,816.62 | £879.96 |
| **Denmark** | 9 | 40 | 236,221 | £67,059.87 | £7,451.10 | £1,676.50 |

### Geographic Observations:
- **UK Market Dominance:** The United Kingdom hosts **91.02%** of all customers (5,350) and accounts for **82.82%** of global revenue (£14.39M).
- **International B2B Profile:** European and international accounts (Netherlands, EIRE, Australia, Denmark) exhibit substantially higher Average Order Values (£1,000–£2,400+) than the UK average (£429.00), signaling export wholesale distributors ordering in container or pallet volumes.

---

## 5. Customer Segmentation

Rather than relying on opaque clustering or arbitrary tiering, segmentation was performed using an empirical, transparent, and documented rule system based on **Customer Value (Revenue)**, **Purchase Frequency (Order Count)**, and **Recency**:

- **75th Percentile Revenue Threshold:** £2,248.31
- **Order Frequency Benchmark:** 6 orders (portfolio mean ~6.3 orders)
- **Recency Activity Horizon:** 180 days (~6 months)

### Empirical Segment Performance Matrix:

| Customer Segment | Customer Count | Customer Share (%) | Total Revenue (£) | Revenue Share (%) | Total Orders | Avg Revenue / Customer | Avg Orders / Customer | Avg Order Value (£) | Avg Recency (Days) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **High-Value Frequent** | 1,177 | 20.02% | £12,409,720.48 | **71.42%** | 22,375 | £10,543.52 | 19.01 | £494.81 | 32.8 |
| **Steady Repeat** | 1,272 | 21.64% | £1,523,518.83 | 8.77% | 6,526 | £1,197.73 | 5.13 | £250.60 | 53.2 |
| **Dormant / Inactive** | 2,241 | **38.13%** | £1,242,995.69 | 7.15% | 4,751 | £554.66 | 2.12 | £279.15 | 426.6 |
| **High-Value Lapsed** | 159 | 2.71% | £1,093,495.32 | 6.29% | 1,456 | £6,877.33 | 9.16 | £1,336.33 | 361.9 |
| **High-Value Occasional**| 134 | 2.28% | £673,556.95 | 3.88% | 537 | £5,026.54 | 4.01 | **£1,710.38** | 61.7 |
| **Occasional Active** | 895 | 15.23% | £431,516.98 | 2.48% | 1,324 | £482.14 | 1.48 | £330.38 | 61.8 |

---

## 6. Most Valuable Customer Groups

Based on empirical, calculated performance metrics:

1. **Highest Gross Revenue Generation:**
   - **High-Value Frequent** is the single most valuable group by gross turnover, contributing **£12,409,720.48 (71.42% of all company sales)** with an average customer revenue of **£10,543.52** and 19.01 orders.
2. **Highest Single-Order Monetary Value:**
   - **High-Value Occasional** generated the highest average spend per completed invoice at **£1,710.38 per order**, followed by **High-Value Lapsed** at **£1,336.33 per order**, pointing to bulk commercial buying cycles.
3. **High-Value Win-Back Opportunity:**
   - **High-Value Lapsed** accounts for only 159 customers (2.71% of user base) but generated **£1.09M (6.29% of revenue)** before lapsing (average 361.9 days since last order). Regaining these accounts represents substantial revenue potential for retention campaigns.

---

## 7. Key Findings

1. **Massive Commercial Concentration:** 20.02% of customers produce 71.42% of revenue. Business revenue stability depends heavily on retaining the ~1,177 core champions.
2. **High Customer Attrition Risk:** 38.13% of all accounts (2,241 customers) have not ordered in over 6 months (average recency of 426 days).
3. **Mid-Market Stability:** The **Steady Repeat** segment forms the commercial operational backbone with 1,272 accounts averaging 5.13 orders, generating £1.52M.
4. **Domestic vs. Export Dichotomy:** Domestic UK buyers buy frequently with moderate basket sizes, while international buyers order in large, infrequent bulk volumes.

---

## 8. Marketing Strategy Suggestions (Bonus Requirement)

*The following strategies are evidence-based recommendations derived from the observed behavioral segments:*

| Segment | Strategic Objective | Concrete Marketing & Commercial Action |
| :--- | :--- | :--- |
| **High-Value Frequent** | Retention & Lifetime Value Maximization | Establish a VIP tier offering dedicated account liaisons, quarterly exclusive product previews, volume shipping discounts, and priority dispatch. |
| **High-Value Occasional** | Purchasing Cadence Acceleration | Implement scheduled reorder reminders aligned with their 60–90 day purchasing interval; introduce progressive tiered volume pricing to capture additional line items. |
| **High-Value Lapsed** | High-Yield Win-Back | Deploy targeted, personalized outreach from senior sales reps or tailored email sequences offering a significant return incentive (e.g., free bulk shipping or a 15% reactivation credit). |
| **Steady Repeat** | Upselling & Cross-Selling | Recommend complementary product categories (e.g., giftware accessories) and introduce annual spend-tier thresholds to incentivize upgrading into the High-Value bracket. |
| **Occasional Active** | Second-Purchase Conversion | Deploy automated triggered email sequences 14–30 days post-order containing curated bestseller recommendations and first-repeat discounts. |
| **Dormant / Inactive** | Re-Engagement & List Sanitation | Execute a multi-touch sunset campaign featuring an aggressive reactivation discount; archive permanently unresponsive accounts after 60 days to reduce CRM overhead. |

---

## 9. Limitations

1. **Absence of Customer Age Data:** The official CodSoft brief mentions age-based segmentation; however, the UCI Online Retail II dataset contains no customer age or demographic attributes. To maintain analytical integrity, **no customer ages were invented or estimated**. Segmentation relied strictly on verifiable location and purchasing behavior data.
2. **Lack of Cost & Margin Data:** Transaction line items reflect gross sales revenue (`Quantity * Price`) rather than net commercial profit. High-revenue bulk orders may carry thinner margins than individual high-price retail items.
3. **No Direct Cancellation Linkage:** Returns (Invoices beginning with 'C') were quarantined in Task 1. Net returns at the customer level were not tracked against subsequent purchases.

---

## 10. Conclusion

Task 4 successfully bridges transactional records and strategic commercial intelligence. By constructing customer profiles and applying transparent behavioral rules, the analysis isolates high-yield customer cohorts, uncovers high-impact win-back opportunities, and provides an actionable blueprint for targeted retention and growth campaigns.
