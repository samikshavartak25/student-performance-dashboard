-- ==============================================================================
-- Project: Student Performance Analysis Dashboard
-- Developer: Samiksha Prashant Vartak
-- Component: 03_analysis_queries.sql - Key Analytical Queries & Insights
-- ==============================================================================

-- -----------------------------------------------------------------------------
-- Query 1: Executive KPI Summary
-- Calculates Total Students, Overall Average Percentage, Overall Passing Rate %,
-- and Average Attendance across all departments.
-- -----------------------------------------------------------------------------
SELECT 
    COUNT(*) AS total_students,
    ROUND(AVG(overall_pct), 2) AS average_score_pct,
    ROUND(AVG(attendance_pct), 2) AS average_attendance_pct,
    SUM(CASE WHEN result_status = 'Pass' THEN 1 ELSE 0 END) AS total_passed,
    SUM(CASE WHEN result_status = 'Fail' THEN 1 ELSE 0 END) AS total_failed,
    ROUND(100.0 * SUM(CASE WHEN result_status = 'Pass' THEN 1 ELSE 0 END) / COUNT(*), 2) AS passing_rate_pct
FROM student_performance;

-- -----------------------------------------------------------------------------
-- Query 2: Attendance vs Academic Performance Correlation
-- Compares students with low attendance (<75%) vs regular attendance (>=75%)
-- -----------------------------------------------------------------------------
SELECT 
    CASE 
        WHEN attendance_pct < 75.0 THEN 'Low Attendance (< 75%)'
        ELSE 'Regular Attendance (>= 75%)'
    END AS attendance_group,
    COUNT(*) AS student_count,
    ROUND(AVG(overall_pct), 2) AS avg_academic_score,
    ROUND(AVG(internal_assessment), 2) AS avg_internal_score,
    SUM(CASE WHEN result_status = 'Pass' THEN 1 ELSE 0 END) AS passed_students,
    SUM(CASE WHEN result_status = 'Fail' THEN 1 ELSE 0 END) AS failed_students,
    ROUND(100.0 * SUM(CASE WHEN result_status = 'Fail' THEN 1 ELSE 0 END) / COUNT(*), 2) AS failure_rate_pct
FROM student_performance
GROUP BY 1;

-- -----------------------------------------------------------------------------
-- Query 3: Subject-wise Performance Ranking & Low-Performance Identification
-- Unpivots subject scores to evaluate average marks, pass count, and failure rate
-- Highlights which subjects have the highest failure rates (Low-performance areas)
-- -----------------------------------------------------------------------------
SELECT 
    subject_name,
    ROUND(AVG(score), 2) AS average_score,
    MIN(score) AS minimum_score,
    MAX(score) AS maximum_score,
    SUM(CASE WHEN score < 40 THEN 1 ELSE 0 END) AS failed_students_count,
    ROUND(100.0 * SUM(CASE WHEN score < 40 THEN 1 ELSE 0 END) / COUNT(*), 2) AS failure_rate_pct
FROM (
    SELECT 'Database Management Systems' AS subject_name, dbms_score AS score FROM student_performance
    UNION ALL
    SELECT 'Data Structures & Algorithms', dsa_score FROM student_performance
    UNION ALL
    SELECT 'Operating Systems', os_score FROM student_performance
    UNION ALL
    SELECT 'Computer Networks', cn_score FROM student_performance
    UNION ALL
    SELECT 'Business Intelligence', bi_score FROM student_performance
) AS subject_unpivot
GROUP BY subject_name
ORDER BY failure_rate_pct DESC;

-- -----------------------------------------------------------------------------
-- Query 4: Department-wise Academic Breakdown
-- Evaluates academic performance and risk distribution across disciplines
-- -----------------------------------------------------------------------------
SELECT 
    department,
    COUNT(*) AS student_count,
    ROUND(AVG(attendance_pct), 2) AS avg_attendance_pct,
    ROUND(AVG(overall_pct), 2) AS avg_percentage,
    ROUND(100.0 * SUM(CASE WHEN result_status = 'Pass' THEN 1 ELSE 0 END) / COUNT(*), 2) AS pass_percentage,
    SUM(CASE WHEN risk_category = 'High Risk' THEN 1 ELSE 0 END) AS high_risk_count
FROM student_performance
GROUP BY department
ORDER BY avg_percentage DESC;

-- -----------------------------------------------------------------------------
-- Query 5: Grade Distribution & Pass/Fail Trends
-- -----------------------------------------------------------------------------
SELECT 
    grade,
    COUNT(*) AS student_count,
    ROUND(100.0 * COUNT(*) / (SELECT COUNT(*) FROM student_performance), 2) AS percentage_share
FROM student_performance
GROUP BY grade
ORDER BY 
    CASE grade
        WHEN 'A+' THEN 1
        WHEN 'A' THEN 2
        WHEN 'B' THEN 3
        WHEN 'C' THEN 4
        WHEN 'D' THEN 5
        WHEN 'F' THEN 6
    END;

-- -----------------------------------------------------------------------------
-- Query 6: Top 10 High-Performing Students (Merit List)
-- -----------------------------------------------------------------------------
SELECT 
    student_id,
    full_name,
    department,
    semester,
    attendance_pct,
    total_score,
    overall_pct,
    grade
FROM student_performance
WHERE result_status = 'Pass'
ORDER BY overall_pct DESC, attendance_pct DESC
LIMIT 10;
