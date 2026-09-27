# Power BI Dashboard

The Power BI dashboard for Task 3 was created using **Microsoft Power BI Desktop** and the cleaned Online Retail dataset from Task 1.

The dashboard was built manually in Power BI Desktop to provide executive stakeholders with an intuitive, interactive analytical view of business performance.

---

## File Details

- **File Name:** `Online_Retail_Sales_Dashboard.pbix`
- **Location:** [`Task_3_Data_Visualization/powerbi/Online_Retail_Sales_Dashboard.pbix`](Online_Retail_Sales_Dashboard.pbix)
- **Format:** Microsoft Power BI Desktop binary file (`.pbix`)
- **Dashboard Title:** `ONLINE RETAIL SALES DASHBOARD`

---

## Source Dataset

The dashboard connects directly to the cleaned dataset generated in Task 1:
- **Source File:** [`../../Task_1_Data_Cleaning/data/processed/online_retail_ii_cleaned.csv`](../../Task_1_Data_Cleaning/data/processed/online_retail_ii_cleaned.csv)
- **Volume:** 779,425 verified sales transactions
- **Timeframe:** December 2009 – December 2011

---

## Dashboard Components

The completed Power BI dashboard page contains:

1. **Dashboard Title Banner:**
   - `ONLINE RETAIL SALES DASHBOARD`

2. **Executive KPI Cards:**
   - **Total Revenue:** High-level monetary gross turnover
   - **Total Orders Display:** Distinct count of completed transactions
   - **Total Customers Display:** Distinct count of verified customer accounts
   - **Total Products Display:** Distinct count of individual catalog items
   - **Total Units Sold:** Aggregate inventory volume purchased
   - **Average Order Value:** Mean sales revenue generated per purchase order

3. **Monthly Revenue Trend:**
   - Continuous line chart illustrating monthly revenue trends and seasonal peaks

4. **Revenue by Country:**
   - Horizontal bar chart ranking countries by their overall gross revenue contribution

5. **Top 10 Products by Revenue:**
   - Horizontal bar chart highlighting the top 10 best-selling catalog items

6. **Interactive Slicers:**
   - **Country Slicer:** Filter all visual cards and charts by individual or multiple countries
   - **Date Range Slicer:** Temporal slider enabling time-window adjustments across the 24-month horizon

7. **Revenue by Year:**
   - Discrete column / bar chart comparing yearly sales totals across operational periods

---

## How to Open and Use the File

1. **System Requirement:** Ensure [Power BI Desktop](https://powerbi.microsoft.com/desktop/) is installed on your Windows system.
2. **Open Workbook:**
   - Double-click `Online_Retail_Sales_Dashboard.pbix`, or
   - Launch Power BI Desktop and navigate to `File > Open Report > Browse reports`.
3. **Explore Dashboard:**
   - The primary canvas is displayed on Page 1.
   - Use the **Country** slicer dropdown/list to isolate individual markets (e.g., United Kingdom, Germany, France).
   - Adjust the **Date Range** slicer handles to filter by specific date spans.
   - Click directly on bar or column chart elements for bidirectional cross-filtering.
4. **Data Source Path Configuration (if moved across machines):**
   - If opening on a new workstation where the local file path has changed, click `Transform data > Data source settings > Change Source` and point to `Task_1_Data_Cleaning/data/processed/online_retail_ii_cleaned.csv`.
