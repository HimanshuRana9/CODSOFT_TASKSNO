# Task 3 — Data Visualization Dashboard

## Overview

This task focuses on transforming the cleaned multi-year Online Retail dataset into clear, decision-oriented business visualizations and an interactive Power BI dashboard. 

While **Task 1** performed comprehensive data cleaning and schema validation, and **Task 2** conducted in-depth exploratory data analysis (EDA), **Task 3** bridges analysis and business decision-making by communicating critical commercial insights visually. The dashboard enables stakeholders to explore revenue dynamics, customer activity, top-performing product lines, and geographic performance interactively.

---

## Objective

The core objectives of the Data Visualization Dashboard are to:

- **Visualize sales performance** across key executive metrics (revenue, orders, units sold, and average order value).
- **Identify revenue trends** across months and operational years to spot cyclicality and seasonal surges.
- **Compare countries by revenue** to understand geographic concentration and international market contributions.
- **Identify top-performing products** driving the business's top-line revenue.
- **Provide interactive filtering** through multi-dimensional slicers (country and date range) allowing ad-hoc exploration.
- **Deliver a professional business dashboard** built using industry-standard BI tooling (Microsoft Power BI Desktop).

---

## Dataset

The dashboard is powered by the cleaned dataset produced in **Task 1**:

- **Dataset Path:** [`Task_1_Data_Cleaning/data/processed/online_retail_ii_cleaned.csv`](../Task_1_Data_Cleaning/data/processed/online_retail_ii_cleaned.csv)
- **Verified Records:** 779,425 validated transactions
- **Time Horizon:** 2009-12-01 to 2011-12-09 (24 months)
- **Data Quality:** Zero missing values, zero uncredited guest transactions, deduplicated, and business-validated.

> [!NOTE]
> The dashboard links directly to the cleaned dataset generated in Task 1 to avoid duplicate storage and maintain a single source of truth across the project.

---

## Tools Used

Only tools and technologies utilized in building this dashboard are included:

- **Microsoft Power BI Desktop** — Dashboard authoring, layout design, visual configuration, and interactivity.
- **Power Query** — Data ingestion and schema type verification.
- **DAX (Data Analysis Expressions)** — Calculated measures for business KPIs and aggregations.
- **Cleaned Online Retail II Dataset** — Processed analytical data source from Task 1.

---

## Dashboard Components

The completed Power BI dashboard (`ONLINE RETAIL SALES DASHBOARD`) consists of the following components:

| Component | Visualization | Purpose |
| :--- | :--- | :--- |
| **Total Revenue** | KPI Card | Displays the overall gross revenue generated across the selected scope |
| **Total Orders Display** | KPI Card | Displays the total count of distinct purchase orders |
| **Total Customers Display** | KPI Card | Shows the count of unique registered customers |
| **Total Products Display** | KPI Card | Shows the number of distinct catalog products sold |
| **Total Units Sold** | KPI Card | Displays total quantity of inventory units sold |
| **Average Order Value** | KPI Card | Displays the average monetary value per completed order |
| **Monthly Revenue Trend** | Line Chart | Illustrates revenue trajectories over time, highlighting monthly fluctuations |
| **Revenue by Country** | Horizontal Bar Chart | Compares sales revenue across active international geographic markets |
| **Top 10 Products by Revenue** | Horizontal Bar Chart | Highlights the 10 highest revenue-generating product catalog items |
| **Country** | Slicer | Provides interactive dropdown/list filtering to isolate specific countries |
| **Date Range** | Date Slicer | Enables dynamic date interval filtering across the transaction timeline |
| **Revenue by Year** | Column / Bar Chart | Compares annual revenue totals across operating fiscal periods |

---

## Dashboard Preview

The dashboard layout and visuals are saved in the project's Power BI workbook:

- **Power BI File:** [`powerbi/Online_Retail_Sales_Dashboard.pbix`](powerbi/Online_Retail_Sales_Dashboard.pbix)
- **Screenshots Directory:** [`powerbi/screenshots/`](powerbi/screenshots/) and [`screenshots/`](screenshots/)

*(To display a screenshot here, save a high-resolution export of the Power BI canvas as `powerbi/screenshots/dashboard_overview.png` and it will automatically render below).*

```text
[Dashboard Overview Screenshot: powerbi/screenshots/dashboard_overview.png]
```

---

## Interactivity

The dashboard provides dynamic bidirectional filtering and slicing:

1. **Country Slicer:** Users can select one or multiple countries to instantly adjust all KPI cards, revenue trends, top products, and yearly performance for that specific market.
2. **Date Range Slicer:** Users can adjust starting and ending dates to zoom into specific quarters, promotional periods, or seasonal intervals.
3. **Cross-Filtering:** Selecting specific visual elements (such as a country or year) updates connected visuals dynamically, enabling granular exploration without requiring manual query execution.

---

## Key Insights

The dashboard illustrates key commercial findings substantiated by the underlying cleaned retail data:

- **Pronounced Seasonality:** Revenue varies considerably by month, displaying marked growth toward Q4 (holiday peak sales period) before normalizing in the early months of the calendar year.
- **Geographic Concentration:** The United Kingdom represents the dominant revenue contribution among all recorded countries, followed by key European markets including EIRE, the Netherlands, Germany, and France.
- **Product Revenue Leadership:** A focused set of top-performing SKUs (such as Regency Cakestand and decorative giftware items) drives a disproportionate share of product revenue.
- **Multi-Year Growth:** Revenue can be evaluated across operating years, showing consistent commercial throughput across the 2009–2011 trading period.
- **Ad-Hoc Market Exploration:** Interactive country and date slicers allow stakeholders to isolate international performance and monitor domestic vs. export dynamics.

---

## Task Requirements

The completed Power BI dashboard satisfies the core data visualization requirements:
- Development of an executive-ready business dashboard in a dedicated BI environment.
- Implementation of multi-metric KPI summary cards.
- Line chart visualization for continuous time-series revenue trends.
- Comparative horizontal bar charts for country and product performance rankings.
- Discrete column/bar chart for annual revenue comparisons.
- Interactive slicers for dynamic geographic and temporal filtering.

> [!NOTE]
> Additional visualization types can be added in a future iteration if required by the task specification.

---

## Files

```text
Task_3_Data_Visualization/
├── README.md                                   # Task 3 comprehensive documentation
├── powerbi/
│   ├── Online_Retail_Sales_Dashboard.pbix     # Completed Power BI Desktop project file
│   ├── README.md                               # Power BI workbook guide & open instructions
│   └── screenshots/                            # Screenshot repository for dashboard captures
│       └── (dashboard_overview.png)
├── outputs/
│   └── visualization_report.md                 # Formal data visualization & findings report
└── screenshots/                                # Root visual captures directory
    └── (dashboard_overview.png)
```

---

## How to Open

1. **Prerequisite:** Download and install [Microsoft Power BI Desktop](https://powerbi.microsoft.com/desktop/) (free on Windows).
2. **Open the File:** Double-click [`powerbi/Online_Retail_Sales_Dashboard.pbix`](powerbi/Online_Retail_Sales_Dashboard.pbix) or open it from Power BI Desktop (`File > Open Report`).
3. **Navigate:** The primary interactive canvas is located on Page 1 (`ONLINE RETAIL SALES DASHBOARD`).
4. **Interact:** Use the **Country** and **Date Range** slicers to filter and explore the visuals dynamically.
