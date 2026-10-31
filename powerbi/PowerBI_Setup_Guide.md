# Power BI Dashboard Setup & Recreation Guide
**Project:** Student Performance Analysis Dashboard  
**Author:** Samiksha Prashant Vartak  
**Tools:** Microsoft Power BI Desktop, Power Query, DAX

---

## 1. Overview of the Dashboard Architecture
This Power BI dashboard transforms raw academic records of 250+ engineering students into actionable executive insights for college administration and faculty.

The dashboard consists of 3 primary view pages:
1. **Executive Overview Page**: Core KPIs (Total Students, Pass Rate, Avg Attendance, High-Risk Count), Departmental Performance Bar Chart, Pass/Fail Donut Chart, and Grade Distribution.
2. **Subject Deep Dive & Low-Performance Areas**: Subject score distributions, failure rates (highlighting Data Structures and Operating Systems as vulnerable subjects), and internal assessment impact.
3. **Faculty Intervention & Risk Matrix**: Scatter plot (Attendance vs Overall Percentage), Slicers for Department / Semester / Risk Category, and a filterable Student Roster table with conditional risk badges.

---

## 2. Step-by-Step Recreation in Power BI Desktop

### Step 1: Import Data via Power Query
1. Open **Power BI Desktop**.
2. Click **Get Data** > **Text/CSV**.
3. Select `data/cleaned_students_data.csv` from this project folder.
4. In Power Query Editor:
   - Ensure `attendance_pct`, `overall_pct`, `internal_assessment` are typed as `Decimal Number`.
   - Ensure `dbms_score`, `dsa_score`, `os_score`, `cn_score`, `bi_score`, `total_score` are typed as `Whole Number`.
   - Ensure `semester` is typed as `Whole Number`.
5. Click **Close & Apply**.

### Step 2: Add DAX Measures
1. Right-click on `cleaned_students_data` table > **New Measure**.
2. Paste each measure from `powerbi/DAX_Measures.dax`.
   - Recommended folder structure: Organize measures into a dedicated display folder named `_KeyMeasures`.

### Step 3: Page 1 - Executive Performance Dashboard
- **Top Card Visuals (KPI Row)**:
  - Card 1: `[Total Students]` (Formatted as whole number: 250)
  - Card 2: `[Pass Percentage]` (Formatted as percentage: 73.6%)
  - Card 3: `[Average Attendance Rate]` (Formatted as percentage: 81.9%)
  - Card 4: `[High Risk Student Count]` (Callout value color: `#EF4444` / Red: 42)
- **Visual 1 (Donut Chart)**:
  - Legend: `result_status`
  - Values: `[Total Students]`
  - Colors: Pass (`#10B981` / Emerald Green), Fail (`#EF4444` / Crimson)
- **Visual 2 (Clustered Bar Chart - Departmental Breakdown)**:
  - Y-Axis: `department`
  - X-Axis: `[Average Overall Percentage]` and `[Pass Percentage]`
- **Visual 3 (Column Chart - Grade Distribution)**:
  - X-Axis: `grade` (Sort by custom column order A+, A, B, C, D, F)
  - Y-Axis: `[Total Students]`

### Step 4: Page 2 - Subject Vulnerability Analysis
- **Visual 1 (Horizontal Bar Chart - Subject Failure Count)**:
  - Y-Axis: Subject Names
  - X-Axis: Failure Count (`DSA: 30`, `OS: 30`, `DBMS: 20`, `CN: 13`, `BI: 12`)
  - Tooltip: Average Subject Score
  - Data Color: Highlight DSA and OS with Alert Red (`#E11D48`).
- **Visual 2 (Scatter Plot - Attendance vs Percentage Correlation)**:
  - X-Axis: `attendance_pct` (Set constant line at 75% for Defaulter Threshold)
  - Y-Axis: `overall_pct` (Set constant line at 40% for Passing Threshold)
  - Details: `student_id`
  - Legend: `risk_category`
  - Insight: Instantly visualizes bottom-left quadrant (Attendance < 75% & Marks < 40%).

### Step 5: Page 3 - Faculty Action Roster
- **Interactive Slicers**:
  - Department Dropdown
  - Semester Dropdown
  - Risk Category Tile Slicer (High Risk / Medium Risk / Low Risk)
- **Table Visual (Student Action List)**:
  - Columns: `student_id`, `full_name`, `department`, `attendance_pct`, `overall_pct`, `failed_subjects`, `risk_category`
  - Conditional Formatting: Background color of `risk_category` mapped to High Risk (Red), Medium Risk (Orange), Low Risk (Green).

---

## 3. Power BI Service Publishing (Deployment)
1. Sign in to your Power BI account in Desktop.
2. Click **Publish** on the Home ribbon.
3. Select destination workspace (e.g. `My Workspace` or college team workspace).
4. Go to [app.powerbi.com](https://app.powerbi.com), open the report, click **File** > **Embed report** > **Publish to web (public)** to obtain a live embed link to include in resume/portfolio!
