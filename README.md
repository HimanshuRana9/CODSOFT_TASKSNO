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
| **03** | [**Data Visualization Dashboard**](Task_3_Data_Visualization/) | Interactive KPIs, revenue trends, category performance, and geographic distribution. | Matplotlib, Seaborn, Plotly | 🔄 Next Up |
| **04** | [**Customer Data Analysis**](Task_4_Customer_Analysis/) | Customer purchasing behavior, RFM segmentation, and high-value customer identification. | Pandas, Scikit-learn, Seaborn | 📋 Planned |
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
│   ├── README.md
│   ├── data/
│   ├── notebooks/
│   ├── dashboard/
│   ├── outputs/
│   └── report/
│
├── Task_4_Customer_Analysis/          # TASK 4: Customer Data Analysis & RFM
│   ├── README.md
│   ├── data/
│   ├── notebooks/
│   ├── scripts/
│   ├── outputs/
│   └── report/
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
