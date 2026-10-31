"""
Analytical Script executing queries on student_performance.db
Author: Samiksha Prashant Vartak
Prints key metrics, findings, and faculty report data.
"""

import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "student_performance.db")

def run_analytics():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    print("=" * 70)
    print("STUDENT PERFORMANCE ANALYSIS - EXECUTING KEY ANALYTICAL QUERIES")
    print("=" * 70)

    # 1. Executive KPI Summary
    cursor.execute("""
    SELECT 
        COUNT(*) AS total_students,
        ROUND(AVG(overall_pct), 2) AS average_score_pct,
        ROUND(AVG(attendance_pct), 2) AS average_attendance_pct,
        SUM(CASE WHEN result_status = 'Pass' THEN 1 ELSE 0 END) AS total_passed,
        SUM(CASE WHEN result_status = 'Fail' THEN 1 ELSE 0 END) AS total_failed,
        ROUND(100.0 * SUM(CASE WHEN result_status = 'Pass' THEN 1 ELSE 0 END) / COUNT(*), 2) AS passing_rate_pct
    FROM students;
    """)
    kpi = cursor.fetchone()
    print("\n[1] Overall Academic KPI Summary:")
    print(f"  • Total Enrolled Students : {kpi[0]}")
    print(f"  • Average Overall Score   : {kpi[1]}%")
    print(f"  • Average Attendance      : {kpi[2]}%")
    print(f"  • Students Passed         : {kpi[3]} ({kpi[5]}%)")
    print(f"  • Students Failed         : {kpi[4]} ({round(100 - kpi[5], 2)}%)")

    # 2. Attendance Impact Analysis
    cursor.execute("""
    SELECT 
        CASE WHEN attendance_pct < 75.0 THEN 'Defaulters (<75%)' ELSE 'Regular (>=75%)' END AS att_group,
        COUNT(*) AS count,
        ROUND(AVG(overall_pct), 2) AS avg_score,
        SUM(CASE WHEN result_status = 'Fail' THEN 1 ELSE 0 END) AS fails,
        ROUND(100.0 * SUM(CASE WHEN result_status = 'Fail' THEN 1 ELSE 0 END) / COUNT(*), 2) AS failure_rate
    FROM students
    GROUP BY CASE WHEN attendance_pct < 75.0 THEN 'Defaulters (<75%)' ELSE 'Regular (>=75%)' END;
    """)
    att_results = cursor.fetchall()
    print("\n[2] Attendance Correlation with Failure Rates:")
    for row in att_results:
        print(f"  • {row[0]:<18} | Count: {row[1]:<3} | Avg Marks: {row[2]}% | Failed: {row[3]:<2} | Failure Rate: {row[4]}%")

    # 3. Subject-wise Failure Analysis (Identifying low-performance areas)
    cursor.execute("""
    SELECT 
        subject,
        ROUND(AVG(score), 2) AS avg_score,
        SUM(CASE WHEN score < 40 THEN 1 ELSE 0 END) AS failed_count,
        ROUND(100.0 * SUM(CASE WHEN score < 40 THEN 1 ELSE 0 END) / COUNT(*), 2) AS failure_pct
    FROM (
        SELECT 'DBMS' AS subject, dbms_score AS score FROM students
        UNION ALL SELECT 'DSA', dsa_score FROM students
        UNION ALL SELECT 'OS', os_score FROM students
        UNION ALL SELECT 'CN', cn_score FROM students
        UNION ALL SELECT 'BI', bi_score FROM students
    )
    GROUP BY subject
    ORDER BY failure_pct DESC;
    """)
    subject_results = cursor.fetchall()
    print("\n[3] Subject Vulnerability Breakdown (Identified Low-Performance Areas):")
    for row in subject_results:
        flag = " [LOW PERFORMANCE AREA!]" if row[3] > 10.0 else ""
        print(f"  • {row[0]:<6} | Avg Score: {row[1]} | Failed: {row[2]:<2} | Failure Rate: {row[3]}%{flag}")

    # 4. Risk Categorization Summary
    cursor.execute("""
    SELECT risk_category, COUNT(*), ROUND(100.0 * COUNT(*) / (SELECT COUNT(*) FROM students), 1)
    FROM students
    GROUP BY risk_category
    ORDER BY COUNT(*) DESC;
    """)
    risk_results = cursor.fetchall()
    print("\n[4] Student Risk Category Breakdown:")
    for row in risk_results:
        print(f"  • {row[0]:<12}: {row[1]} students ({row[2]}%)")

    # 5. Top 5 High-Risk Students needing immediate Faculty Attention
    cursor.execute("""
    SELECT student_id, full_name, department, attendance_pct, overall_pct, failed_subjects
    FROM students
    WHERE risk_category = 'High Risk'
    ORDER BY failed_subject_count DESC, attendance_pct ASC
    LIMIT 5;
    """)
    high_risk = cursor.fetchall()
    print("\n[5] Immediate Faculty Review Sample (Top High-Risk Students):")
    for s in high_risk:
        print(f"  • ID: {s[0]} | {s[1]:<18} | Dept: {s[2][:10]}... | Att: {s[3]}% | Score: {s[4]}% | Failed in: {s[5]}")

    conn.close()

if __name__ == "__main__":
    run_analytics()
