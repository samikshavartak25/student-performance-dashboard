# ACADEMIC PERFORMANCE & AT-RISK STUDENT AUDIT REPORT
**Document Reference:** AR-2026-SEM4-6  
**Compiled By:** Samiksha Prashant Vartak (Data Analysis & Documentation)  
**Target Audience:** Department Heads, Academic Dean, & Faculty Mentors  
**Dataset Scope:** 250 Engineering Students across Semesters 4, 5, and 6  
**Tools Utilized:** Microsoft Excel (VLOOKUP, Pivot Tables), SQL, Power BI  
**Status:** Approved for Faculty Review and Remedial Action

---

## 1. Executive Summary
An exhaustive academic performance audit was conducted across 250 students enrolled in Computer Science & Business Systems (CSBS), Computer Engineering (CE), Information Technology (IT), and Artificial Intelligence & Data Science (AIDS).

### Primary Findings at a Glance:
| Metric | Value | Benchmark / Target | Variance Status |
| :--- | :--- | :--- | :--- |
| **Total Cohort Size** | 250 Students | - | Complete |
| **Cohort Average Score** | 63.68% | 65.0% | -1.32% (Close to Target) |
| **Cohort Average Attendance** | 81.87% | 80.0% | +1.87% (Satisfactory) |
| **Overall Pass Rate** | 73.6% (184 Passed) | 80.0% | **-6.4% (Requires Attention)** |
| **Overall Failure Rate** | 26.4% (66 Failed) | < 15.0% | **Critical Flag** |
| **Attendance Defaulters (<75%)** | 49 Students (19.6%) | < 10.0% | **High Risk Indicator** |
| **High-Risk Students** | 42 Students (16.8%) | - | Immediate Action Required |

---

## 2. Low-Performance Subject Analysis
By unpivoting subject-level assessment data and applying SQL aggregation queries, failure rates were computed for each individual course module.

### Subject Failure Matrix:
| Subject Name | Subject Code | Average Score | Failing Students | Failure Rate (%) | Performance Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Data Structures & Algorithms** | DSA | 58.32 / 100 | 30 | **12.0%** | **CRITICAL LOW-PERFORMANCE AREA** |
| **Operating Systems** | OS | 60.20 / 100 | 30 | **12.0%** | **CRITICAL LOW-PERFORMANCE AREA** |
| **Database Management Systems** | DBMS | 65.25 / 100 | 20 | 8.0% | Moderate Attention |
| **Computer Networks** | CN | 66.85 / 100 | 13 | 5.2% | Within Acceptable Threshold |
| **Business Intelligence** | BI | 67.80 / 100 | 12 | 4.8% | Strong Performance |

### Root Cause Analysis for Low-Performance Subjects:
1. **Data Structures & Algorithms (DSA - 12.0% Failure Rate)**:
   - Students displayed high difficulty in tree traversals, dynamic programming, and algorithm complexity analysis.
   - Internal lab scores demonstrated adequate syntax knowledge, but final written exams revealed weaknesses in analytical logic derivation.
2. **Operating Systems (OS - 12.0% Failure Rate)**:
   - Core failure points clustered around Process Synchronization (Semaphores, Deadlock prevention) and Virtual Memory Page Replacement calculations.

---

## 3. Attendance vs. Performance Correlation
Cross-tabulation and regression analysis clearly delineate that classroom attendance is the single strongest predictor of academic success.

```
+-----------------------------------------------------------------------------------------+
| ATTENDANCE GROUP          | HEADCOUNT | AVG SCORE | FAILED STUDENTS | FAILURE RATE      |
+-----------------------------------------------------------------------------------------+
| Defaulters (< 75.0%)      | 49        | 47.18%    | 42              | 85.71% [CRITICAL] |
| Regular Students (>= 75%) | 201       | 67.71%    | 24              | 11.94% [HEALTHY]  |
+-----------------------------------------------------------------------------------------+
```

### Key Statistical Takeaway:
- A student with **attendance under 75% is over 7.1 times more likely to fail** than a student with regular attendance (85.71% vs. 11.94%).
- Of the 66 students who failed at least one subject, **63.6% (42 students) were attendance defaulters**.

---

## 4. Department-Wise Academic Comparison
```
+--------------------------------------------+------------+---------------+-------------+-----------+
| Department                                 | Total Enr. | Avg Attnd (%) | Avg Score % | Pass Rate |
+--------------------------------------------+------------+---------------+-------------+-----------+
| Computer Science & Business Systems (CSBS) | 68         | 82.4%         | 64.9%       | 76.5%     |
| Computer Engineering (CE)                  | 64         | 82.1%         | 64.1%       | 75.0%     |
| Information Technology (IT)                | 58         | 81.3%         | 63.2%       | 72.4%     |
| Artificial Intelligence & Data Science     | 60         | 81.5%         | 62.3%       | 70.0%     |
+--------------------------------------------+------------+---------------+-------------+-----------+
```

---

## 5. Strategic Recommendations for Faculty Review

### A. Immediate Interventions (Within 7 Business Days):
1. **Attendance Defaulter Parent-Teacher Advisory**:
   - Issue official academic notices to the guardians of all 49 attendance defaulters.
   - Mandate bi-weekly biometric or signature check-ins with assigned faculty mentors.
2. **Targeted Remedial Clinics for DSA and OS**:
   - Schedule 2 hours of weekly bridge classes focusing on algorithm tracing and OS deadlock exercises.
   - Conduct peer-assisted study circles pairing high-performing students ('A+' and 'A' grade holders) with students at risk.

### B. Curriculum & Assessment Adjustments (Mid-Semester):
1. **Continuous Internal Assessment Rebalancing**:
   - Introduce formative micro-quizzes every fortnight to catch concept drift before mid-term evaluations.
2. **Lab Practice Reinforcement**:
   - Allocate 30 minutes in each 2-hour lab slot for live coding tests without IDE auto-complete.

---

## 6. Appendix: High-Risk Students Requiring Immediate Faculty Mentoring
*(Extracted via SQL view `view_at_risk_students`)*

| Student ID | Student Name | Department | Attendance | Overall Score | Failed Subjects | Recommended Action |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **STU1250** | Tanvi Mehta | Information Technology | 42.1% | 39.2% | DBMS, DSA, OS, BI | Guardian Conference + Mandatory Remedial Lab |
| **STU1026** | Yash Shah | AI & Data Science | 44.4% | 36.2% | DBMS, OS, CN | Formal Attendance Warning + Mentorship |
| **STU1202** | Priyanka Jadhav | Information Technology | 45.6% | 39.2% | DBMS, DSA, OS | Remedial DSA/OS Classes |
| **STU1197** | Sakshi Thakur | Computer Science & BS | 49.1% | 38.4% | DSA, CN, BI | Subject-specific Tutoring |
| **STU1142** | Akash Pawar | Computer Science & BS | 60.0% | 44.8% | DBMS, DSA, CN | Attendance Recovery Plan |
| **STU1015** | Tanmay Chavan | Computer Engineering | 51.2% | 41.6% | DSA, OS | Remedial Coding Sessions |
| **STU1088** | Rohan Kadam | AI & Data Science | 48.7% | 40.0% | DSA, OS, CN | Urgent Mentor Consultation |

---
*Report archived in College Academic Repository. Generated by Student Performance Analysis System.*
