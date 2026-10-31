# 🎓 Student Performance Analysis Dashboard
> **An End-to-End Academic Performance Audit, Power BI Analytics & Faculty Intervention System**  
> **Author:** Samiksha Prashant Vartak  
> **Tools & Tech:** SQL (MySQL/SQLite), Microsoft Power BI, MS Excel (VLOOKUP, Pivot Tables), Python, HTML5/CSS3/JavaScript (Chart.js)

---

## 📌 Executive Summary
This project evaluates the academic performance and risk vulnerability of **250+ undergraduate engineering students** across 4 semesters and disciplines (*Computer Science & Business Systems, Computer Engineering, Information Technology, Artificial Intelligence & Data Science*).

By ingesting raw academic records, resolving data quality anomalies via **SQL cleaning pipelines and Excel**, and visualizing KPIs through an **interactive Power BI Dashboard and Live Web Dashboard**, this system identifies critical subject bottlenecks and arms college faculty with an actionable remediation framework.

---

## 🚀 Key Project Highlights & Statistical Discoveries

```
+-----------------------------------------------------------------------------------------+
| METRIC                          | STATISTIC        | BENCHMARK / STATUS                 |
+-----------------------------------------------------------------------------------------+
| Total Audited Cohort            | 250 Students     | Complete Representative Sample     |
| Cohort Average Score            | 63.68%           | Passing cutoff: 40%                |
| Cohort Average Attendance       | 81.87%           | Mandatory threshold: 75%           |
| Overall Passing Rate            | 73.6% (184 Pass) | 26.4% (66 Fail)                    |
| Attendance Defaulters (< 75%)   | 49 Students      | 19.6% of entire student body       |
| High-Risk Students for Action   | 42 Students      | Mandatory Faculty Remedial List    |
+-----------------------------------------------------------------------------------------+
```

### 🔍 Core Findings:
1. **The 75% Attendance Cliff:**
   - Students with **attendance under 75% experienced an 85.71% failure rate** (42 out of 49 failed).
   - In contrast, students with regular attendance ($\ge 75\%$) had an **11.94% failure rate**.
   - Defaulters are **over 7.1x more likely to fail** end-semester examinations.
2. **Identified Low-Performance Subjects:**
   - **Data Structures & Algorithms (DSA):** Lowest average score (**58.32%**) and highest failure rate (**12.0%**, 30 failed students).
   - **Operating Systems (OS):** Second lowest average score (**60.20%**) and equal failure rate (**12.0%**, 30 failed students).
   - Root causes: Abstract data structure algorithms and process synchronization/memory management logic.

---

## 📁 Repository & Project Architecture

```
student-performance-dashboard/
│
├── data/
│   ├── raw_students_data.csv             # Raw data with casing & missing value anomalies (252 rows)
│   ├── cleaned_students_data.csv         # Cleaned, validated, normalized dataset (250 rows)
│   ├── student_performance.db           # SQLite production database with schema & indexes
│   └── student_performance_workbook.xls  # Multi-sheet Excel workbook (Cleaned, Raw, Pivot, Formulas)
│
├── sql/
│   ├── 01_schema.sql                     # DDL table creation, foreign keys, and indexes
│   ├── 02_data_cleaning.sql              # SQL deduplication, string trimming, null imputation
│   ├── 03_analysis_queries.sql           # Aggregations, subject rankings, correlation queries
│   └── 04_faculty_reports.sql            # Faculty risk views and intervention procedures
│
├── powerbi/
│   ├── DAX_Measures.dax                  # Complete DAX formulas (KPIs, Slicers, Alerts)
│   └── PowerBI_Setup_Guide.md            # Step-by-step recreation guide in Power BI Desktop
│
├── web/                                  # 1-Click Interactive Web Dashboard (Zero Install)
│   ├── index.html                        # Dashboard frontend with KPI cards, slicers & modal
│   ├── style.css                         # Modern dashboard styling + print-ready styles
│   ├── app.js                            # Filtering, search, pagination, Chart.js graphs, CSV export
│   ├── data.js                           # Pre-bundled JSON dataset for instant double-click execution
│   └── students_data.json                # Raw JSON dataset
│
├── reports/
│   └── Faculty_Review_Summary_Report.md  # Official documented audit report for college faculty
│
└── python/
    ├── generate_dataset.py               # Dataset generation & SQLite migration script
    ├── analyze_performance.py            # Automated SQL analytics execution script
    ├── build_excel_workbook.py           # Multi-sheet SpreadsheetML Excel workbook builder
    └── streamlit_app.py                  # Streamlit cloud application
```

---

## 🛠️ How to Run & Deploy the Project

### Option 1: Instant Local Browser View (Fastest - 0 Seconds Setup)
1. Navigate to the `web/` folder.
2. Double-click **`index.html`** in Windows File Explorer.
3. The interactive dashboard opens immediately in Google Chrome / Microsoft Edge with:
   - Live KPI cards
   - Subject-wise and Departmental charts
   - Attendance vs Score scatter plot
   - Searchable, paginated student roster
   - Filterable by Department, Semester, and Faculty Risk Category
   - **"Faculty Review Summary"** modal button (Print/Save to PDF)
   - **"Export Filtered CSV"** button

### Option 2: Deploy Free to GitHub Pages (Live Portfolio Link)
1. Initialize a git repository and push this folder to your GitHub account:
   ```bash
   git init
   git add .
   git commit -m "Add Student Performance Analysis Dashboard"
   git branch -M main
   git remote add origin https://github.com/<your-username>/student-performance-dashboard.git
   git push -u origin main
   ```
2. In GitHub, go to **Settings** > **Pages** > Select `Branch: main` and `/web` folder.
3. Your dashboard is now live online at `https://<your-username>.github.io/student-performance-dashboard/`!

### Option 3: Power BI Desktop Recreation
1. Open **Microsoft Power BI Desktop**.
2. Click **Get Data** > **Text/CSV** > Select `data/cleaned_students_data.csv`.
3. Follow the instructions in `powerbi/PowerBI_Setup_Guide.md` and copy the DAX measures from `powerbi/DAX_Measures.dax`.
4. Click **Publish** to deploy directly to Microsoft Power BI Service.

### Option 4: Execute SQL Analytics via Python
Run the analytical SQL query runner in your terminal:
```bash
python python/analyze_performance.py
```

---

## 💡 Interview Defense Guide (Questions for Samiksha)

### Q1: What was your objective with this project?
> *"The goal was to audit academic performance across 250+ students, identify exactly where students were failing, determine whether attendance directly correlates with end-semester failure rates, and provide department heads with an automated, actionable intervention report."*

### Q2: How did you clean the data using SQL and Excel?
> *"In Excel and SQL, I handled duplicate entries using SQL `ROW_NUMBER() OVER (PARTITION BY Student_ID)` CTEs. I standardized department names with `CASE WHEN` and string functions, imputed missing attendance with departmental medians using `COALESCE`, validated score boundaries ($0-100$), and generated calculated columns for pass/fail status and risk tiering."*

### Q3: What were your biggest analytical takeaways?
> *"Two major insights stood out: First, attendance below 75% resulted in an 85.7% failure rate compared to only 11.9% for regular attendees, proving attendance is the single biggest predictor of performance. Second, Data Structures (DSA) and Operating Systems (OS) had the highest failure rates (12.0% each), leading to targeted faculty remedial clinics."*

---
*Created and maintained by Samiksha Prashant Vartak • B.Tech Computer Science & Business Systems*
