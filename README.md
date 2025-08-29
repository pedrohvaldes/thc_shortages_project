# 📊 Case Study: Shortages Analysis for Amazon Supplier

## 📌 Business Context
Our client is an Amazon supplier who frequently faces **shortages disputes** — situations where Amazon records fewer items received than what was shipped. As a result, Amazon reduces the invoice payment.  
Our client, however, strongly believes that all units were shipped correctly. Resolving these disputes is crucial to ensure **full payment recovery** and reduce financial leakage.

---

## 🎯 Objectives of the Analysis
1. **Quantify the financial impact of shortages** by calculating the **Total Shortage Amount (USD)**.  
2. **Identify trends over time** by producing an **Annual Breakdown of shortages** (sum, count, average).  
3. **Classify and measure aged shortages** — shortages that remain unresolved **over 90 days past the due date**.  

---

## 🛠️ Approach & Methodology
- **Data Source:** Amazon invoice dataset (CSV export).  
- **Tools Used:** Python (pandas, numpy, matplotlib), Click CLI for reproducibility, Excel & CSV for outputs.  
- **Process Steps:**  
  1. Load and validate dataset (currency, dates, schema).  
  2. Extract shortages using `Quantity Variance Amount`.  
  3. Compute **aging** based on `Payment Due Date` vs reference date.  
  4. Aggregate shortages by **year** and classify into **current vs aged**.  
  5. Export results into Excel, CSVs, and PNG charts for reporting.  

---

## 📊 Results & Insights

### 🔹 Total Shortages
- **$877,997.87** in shortages across **3,336 invoice lines**.  

### 🔹 Annual Breakdown
| Year | Total Shortage (USD) | Lines | Avg Shortage (USD) | Share % |
|------|-----------------------|-------|--------------------|---------|
| 2021 | $8,771.47            | 196   | $44.75             | 1.0%    |
| 2022 | $25,480.03           | 576   | $44.24             | 2.9%    |
| 2023 | $51,669.80           | 957   | $53.99             | 5.9%    |
| 2024 | **$486,215.20**      | 1,380 | $352.33            | 55.4%   |
| 2025 | **$305,861.37**      | 227   | $1,347.41          | 34.8%   |

➡️ **Insight:** ~90% of shortage dollars occurred in **2024–2025**, suggesting systemic issues or process breakdowns in recent years.  

### 🔹 Aged Shortages
- **100% of shortages are aged (>90 days past due)** as of Aug 29, 2025.  
- Recovery focus should target **high-value invoices in 2024–2025**.  

---

## 📂 Deliverables
The analysis produces the following outputs (in `outputs/` folder):  
- **shortage_analysis_report.xlsx** → consolidated report with all tables  
- **annual_breakdown.csv** → shortages by year  
- **aged_by_year.csv** → aged shortages by year  
- **current_vs_aged.csv** → comparison table  
- **fig_total_by_year.png** → bar chart of total shortages per year  
- **fig_aged_by_year.png** → bar chart of aged shortages per year  
- **run_summary.json** → run metadata (analysis date, totals, etc.)  

---

## 🚀 How to Run the Project

1. **Setup Environment**
```powershell
python -m venv .venv; .\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
$env:PYTHONPATH = "$PWD\src"
```

2. **Run Analysis**
```powershell
python -m thc_shortages.cli analyze --input "data\input\Headers.2025-03-18.na-us_R (2).csv" --outdir outputs --report-date 2025-08-29 --dayfirst
```

---

## ✅ Key Takeaways
- Shortages represent **nearly $878k in potential lost revenue**.  
- The **vast majority is concentrated in 2024–2025** and is already aged.  
- Immediate recovery efforts should prioritize these high-value shortages.  
- Future improvements could include **root cause analysis by PO, SKU, or DC** and building a **dashboard** for continuous monitoring.  

---

## 👤 Author
**Pedro Henrique Valdes**  
*Jr. Data Scientist – Assessment Submission*  
