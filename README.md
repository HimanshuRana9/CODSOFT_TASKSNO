# CodSoft Data Analytics Internship Portfolio

[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Pandas](https://img.shields.io/badge/Pandas-2.2%2B-150458.svg)](https://pandas.pydata.org/)
[![NumPy](https://img.shields.io/badge/NumPy-1.26%2B-013243.svg)](https://numpy.org/)
[![Matplotlib](https://img.shields.io/badge/Matplotlib-3.8%2B-orange.svg)](https://matplotlib.org/)
[![Seaborn](https://img.shields.io/badge/Seaborn-0.13%2B-blueviolet.svg)](https://seaborn.pydata.org/)
[![Plotly](https://img.shields.io/badge/Plotly-5.18%2B-3F4F75.svg)](https://plotly.com/)
[![Scikit-Learn](https://img.shields.io/badge/scikit--learn-1.4%2B-F7931E.svg)](https://scikit-learn.org/)
[![Status](https://img.shields.io/badge/Status-In%20Progress-success.svg)]()

> A data analytics portfolio demonstrating practical, reproducible end-to-end data analytics: data cleaning & quality auditing, exploratory data analysis (EDA), data visualization dashboards, customer behavior & RFM segmentation, and automated web data extraction.

---

## 📌 Internship Information

- **Organization:** [CodSoft](https://www.codsoft.in/)
- **Domain:** Data Analytics
- **Repository:** `CODSOFT_TASKSNO`
- **Primary Language:** Python 3.x
- **Development Environment:** Jupyter Notebook / VS Code
- **Dataset (Tasks 1–4):** [UCI Machine Learning Repository — Online Retail II](https://archive.ics.uci.edu/dataset/502/online%2Bretail) (1,067,371 records)

---

## 🚀 Tasks Roadmap & Implementation Status

| Task | Title | Description | Primary Tools | Status |
| :---: | :--- | :--- | :--- | :---: |
| **01** | [**Data Cleaning & Preprocessing**](Task_1_Data_Cleaning/) | End-to-end audit, deduplication, schema standardization, and business validation on 1.06M retail records. | Python, Pandas, NumPy, Matplotlib |  **Completed** |
| **02** | [**Exploratory Data Analysis**](Task_2_EDA/) | Statistical summaries, distributions, seasonality, sales velocity, and anomaly detection. | Pandas, Seaborn, Matplotlib |  **Completed** |
| **03** | [**Data Visualization Dashboard**](Task_3_Data_Visualization/) | Interactive KPIs, revenue trends, category performance, and geographic distribution. | Power BI Desktop, DAX, Power Query | ✅ **Completed** |
| **04** | [**Customer Data Analysis**](Task_4_Customer_Analysis/) | Customer purchasing behavior, behavioral segmentation, and high-value cohort analysis. | Python, Pandas, Matplotlib, Seaborn | ✅ **Completed** |
| **05** | [**Web Data Extraction & Analysis**](Task_5_Web_Data_Extraction/) | Public structured web scraping, data sanitation, exploratory analysis, and insights. | Requests, BeautifulSoup, Pandas | 📋 Planned |

---

## 🏗️ Repository Architecture

```text
CODSOFT_TASKSNO/
│
├── README.md                          # Master project portfolio overview
├── requirements.txt                   # Locked project dependencies
├── .gitignore                         # Git exclusion rules for large datasets
│
├── Task_1_Data_Cleaning/             # TASK 1: Data Cleaning & Preprocessing
│   ├── README.md                      # Task 1 detailed documentation
│   ├── data/
│   │   ├── raw/                       # Raw immutable sources (Excel/CSV)
│   │   └── processed/                 # Cleaned analytical dataset
│   ├── notebooks/
│   │   └── 01_data_cleaning.ipynb     # Interactive cleaning & audit notebook
│   ├── scripts/
│   │   ├── download_dataset.py        # UCI dataset fetcher script
│   │   └── clean_dataset.py           # Production data cleaning pipeline
│   ├── outputs/
│   │   ├── data_quality_before.csv    # Pre-cleaning audit scorecard
│   │   ├── data_quality_after.csv     # Post-cleaning validation scorecard
│   │   └── data_cleaning_summary.png  # Audit comparison visual
│   └── report/
│       └── task_1_report.md           # Formal task summary report
│
├── Task_2_EDA/                        # TASK 2: Exploratory Data Analysis
│   ├── README.md
│   ├── data/
│   ├── notebooks/
│   ├── scripts/
│   ├── outputs/
│   └── report/
│
├── Task_3_Data_Visualization/         # TASK 3: Data Visualization Dashboard
│   ├── README.md                      # Task 3 overview & dashboard documentation
│   ├── powerbi/
│   │   ├── Online_Retail_Sales_Dashboard.pbix # Completed Power BI Desktop dashboard
│   │   ├── README.md                  # Power BI guide & how-to-open instructions
│   │   └── screenshots/               # Dashboard screenshots
│   ├── outputs/
│   │   └── visualization_report.md    # Formal visual analytics report
│   └── screenshots/                   # Dashboard previews
│
├── Task_4_Customer_Analysis/          # TASK 4: Customer Data Analysis
│   ├── README.md                      # Comprehensive Task 4 guide
│   ├── notebooks/
│   │   └── 04_customer_analysis.ipynb # Interactive customer analytics notebook
│   ├── scripts/
│   │   └── customer_analysis.py       # Automated customer segmentation pipeline
│   ├── outputs/
│   │   ├── customer_summary.csv       # Customer profile metrics (5,878 rows)
│   │   ├── customer_segments.csv      # Customer segment assignments (5,878 rows)
│   │   ├── country_customer_analysis.csv # Geographic distribution (41 countries)
│   │   ├── segment_summary.csv        # Segment performance matrix (6 segments)
│   │   └── charts/                    # High-resolution visual charts
│   └── report/
│       └── customer_analysis_report.md# Formal customer analysis report
│
├── Task_5_Web_Data_Extraction/        # TASK 5: Web Data Extraction & Analysis
│   ├── README.md
│   ├── data/
│   ├── notebooks/
│   ├── scripts/
│   ├── outputs/
│   └── report/
│
└── docs/                              # Global documentation & standards
    ├── data_dictionary.md             # Complete schema and feature descriptions
    ├── methodology.md                 # 10-stage analytics lifecycle framework
    ├── testing.md                     # QA testing and assertion matrix
    └── project_report.md              # Executive portfolio report
```

---

## 🔍 Task 1 Highlight: Data Cleaning & Quality Audit

The **UCI Online Retail II** raw dataset contained **1,067,371 rows** spanning two operational years. The cleaning pipeline uncovered and resolved key data quality issues:

```text
┌────────────────────────────────────────────────────────────────────────┐
│                        DATA CLEANING FUNNEL                            │
├────────────────────────────────────────────────────────────────────────┤
│ Initial Raw Records:            1,067,371                              │
│ ├── Duplicate Rows Purged:        -34,335  (3.22% of total rows)       │
│ ├── Missing CustomerID Quarantined: -243,007 (22.77% uncredited guests)│
│ ├── Cancellations (Invoice 'C'):  -19,494  (tagged & removed)          │
│ └── Non-positive Volume/Price:    -22,950  (adjustments & write-offs)  │
│                                                                        │
│ Final Clean Analytical Records:   779,425 (100% verified sales)        │
│ Final Null Values:                      0                              │
│ Final Duplicate Rows:                   0                              │
└────────────────────────────────────────────────────────────────────────┘
```

![Task 1 Quality Summary](Task_1_Data_Cleaning/outputs/data_cleaning_summary.png)

---

## Task 3 — Data Visualization Dashboard

Task 3 focuses on transforming the validated, multi-year Online Retail dataset into an executive business dashboard built in **Microsoft Power BI Desktop**. Building upon the data cleaning in Task 1 and exploratory data analysis in Task 2, Task 3 visualizes sales performance, seasonal trajectories, customer engagement, and product revenue contributors.

### Key Visualizations & Features
- **Executive KPI Cards:** Total Revenue, Total Orders Display, Total Customers Display, Total Products Display, Total Units Sold, and Average Order Value.
- **Monthly Revenue Trend (Line Chart):** Continuous time-series tracking monthly revenue and seasonality peaks across the 24-month horizon.
- **Revenue by Country (Horizontal Bar Chart):** Geographic market breakdown comparing UK domestic sales with international export destinations.
- **Top 10 Products by Revenue (Horizontal Bar Chart):** Highlighting the highest-earning product catalog SKUs.
- **Revenue by Year (Column / Bar Chart):** Annual revenue comparison across operating fiscal periods.
- **Interactive Slicers:** Country filter and Date Range slider for real-time dynamic filtering and visual cross-filtering across the entire dashboard.

### Dashboard File & Documentation
- **Power BI File:** [`Task_3_Data_Visualization/powerbi/Online_Retail_Sales_Dashboard.pbix`](Task_3_Data_Visualization/powerbi/Online_Retail_Sales_Dashboard.pbix)
- **Detailed Documentation:** [Task 3 README](Task_3_Data_Visualization/README.md)
- **Visual Analytics Report:** [Task 3 Visualization Report](Task_3_Data_Visualization/outputs/visualization_report.md)

---

## 👥 Task 4 Highlight: Customer Data Analysis

Task 4 performs customer purchasing behavior analysis and customer segmentation using **Python, Pandas, Matplotlib, and Seaborn**. Built on the validated Online Retail transactions dataset, this analysis profiles 5,878 distinct customer accounts across 41 countries.

### Key Analytical Findings & Features
- **Customer Profiling:** Reconciled 779,425 transactions into 5,878 customer profiles tracking revenue, order count, average order value (AOV), inventory units, and recency.
- **Geographic Analysis:** Evaluated domestic vs. export market dynamics, establishing the UK as the volume core (91% of customers) and international markets (EIRE, Netherlands, Australia) as high-AOV wholesale drivers.
- **Transparent Behavioral Segmentation:** Implemented an empirical rule-based framework categorizing customers into 6 distinct behavioral tiers (*High-Value Frequent*, *High-Value Occasional*, *High-Value Lapsed*, *Steady Repeat*, *Occasional Active*, *Dormant / Inactive*).
- **Most Valuable Customer Cohorts:** Identified that the top 20.02% of customers (*High-Value Frequent*) generate 71.42% (£12.41M) of total portfolio turnover.
- **Actionable Marketing Strategies (Bonus):** Formulated targeted marketing campaigns for VIP loyalty, wholesale cadence acceleration, lapsed win-back, and dormant reactivation.
- **Age Limitation Documented:** Transparently noted that age-based segmentation was not performed as the source dataset contains no demographic age attributes.

- **Interactive Notebook:** [`Task_4_Customer_Analysis/notebooks/04_customer_analysis.ipynb`](Task_4_Customer_Analysis/notebooks/04_customer_analysis.ipynb)
- **Detailed Documentation:** [Task 4 README](Task_4_Customer_Analysis/README.md)
- **Customer Analysis Report:** [Task 4 Report](Task_4_Customer_Analysis/report/customer_analysis_report.md)

---

## 🌐 Task 5 Highlight: Web Data Extraction & Analysis

Task 5 implements an end-to-end web scraping, structured data cleaning, and exploratory data analysis pipeline using **Python, BeautifulSoup4, Requests, Pandas, Matplotlib, and Seaborn**. Data was harvested ethically from the public sandbox [Books to Scrape](https://books.toscrape.com) across 50 catalogue pages.

### Key Highlights & Deliverables
- **Automated Web Scraper:** Built a modular crawler in [`Task_5_Web_Data_Extraction/scraper/web_scraper.py`](Task_5_Web_Data_Extraction/scraper/web_scraper.py) with category taxonomy mapping, rate limiting, and defensive UTF-8 encoding handling.
- **Clean Structured Dataset:** Extracted 812 book records across 21 genres with zero missing values or duplicate records, saved to [`Task_5_Web_Data_Extraction/data/processed/scraped_books.csv`](Task_5_Web_Data_Extraction/data/processed/scraped_books.csv).
- **Multi-Sheet Excel Workbook:** Automated export to [`Task_5_Web_Data_Extraction/outputs/scraped_books.xlsx`](Task_5_Web_Data_Extraction/outputs/scraped_books.xlsx) featuring *Books*, *Summary*, and *Category Analysis* sheets.
- **Exploratory Data Analysis:** Analyzed price distributions, star rating proportions, category inventory depth, and price-rating correlations in [`Task_5_Web_Data_Extraction/scripts/web_data_analysis.py`](Task_5_Web_Data_Extraction/scripts/web_data_analysis.py).
- **Interactive Notebook:** [`Task_5_Web_Data_Extraction/notebooks/Task5_EDA.ipynb`](Task_5_Web_Data_Extraction/notebooks/Task5_EDA.ipynb)
- **Comprehensive Report:** [Task 5 Web Extraction Report](Task_5_Web_Data_Extraction/report/web_extraction_report.md)

---

## 💻 Installation & Reproduction Guide

### 1. Clone the Repository
```bash
git clone https://github.com/HimanshuRana9/CODSOFT_TASKSNO.git
cd CODSOFT_TASKSNO
```

### 2. Configure Virtual Environment
```bash
python -m venv .venv
# On Windows:
.venv\Scripts\activate
# On Linux/macOS:
source .venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Execute Task 1 Data Cleaning
```bash
python Task_1_Data_Cleaning/scripts/clean_dataset.py
```

### 5. Launch Jupyter Notebook
```bash
jupyter notebook Task_1_Data_Cleaning/notebooks/01_data_cleaning.ipynb
```

---

## 📚 Technical Standards & Documentation

For detailed methodology, schema specifications, and testing verification:
- [Data Dictionary](docs/data_dictionary.md)
- [Methodology & Architecture](docs/methodology.md)
- [Testing & Quality Assurance](docs/testing.md)
- [Master Project Report](docs/project_report.md)

---

## 👤 Author

- **Himanshu Rana**
- **GitHub:** [@HimanshuRana9](https://github.com/HimanshuRana9)
- **Internship:** CodSoft Data Analytics Internship
