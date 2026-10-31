-- ==============================================================================
-- Project: Student Performance Analysis Dashboard
-- Developer: Samiksha Prashant Vartak
-- Component: 04_faculty_reports.sql - Faculty Review Views & Intervention Reports
-- ==============================================================================

-- -----------------------------------------------------------------------------
-- View 1: At-Risk Students Requiring Faculty Intervention
-- Filters students with High or Medium risk status for counseling and remedial classes
-- -----------------------------------------------------------------------------
CREATE OR REPLACE VIEW view_at_risk_students AS
SELECT 
    student_id,
    full_name,
    department,
    semester,
    attendance_pct,
    overall_pct,
    failed_subject_count,
    failed_subjects,
    risk_category,
    CASE 
        WHEN attendance_pct < 75.0 AND failed_subject_count > 0 
            THEN 'Critical: Mandatory remedial sessions + Guardian consultation'
        WHEN attendance_pct < 75.0 
            THEN 'Warning: Attendance shortage warning letter'
        WHEN failed_subject_count > 0 
            THEN 'Academic: Subject-specific tutoring required'
        ELSE 'Monitor: General mentoring'
    END AS faculty_recommended_action
FROM student_performance
WHERE risk_category IN ('High Risk', 'Medium Risk')
ORDER BY 
    CASE risk_category WHEN 'High Risk' THEN 1 ELSE 2 END,
    failed_subject_count DESC,
    attendance_pct ASC;

-- -----------------------------------------------------------------------------
-- View 2: Faculty Subject-Level Vulnerability Matrix
-- Identifies specific subjects needing syllabus pacing adjustment or lab re-inforcement
-- -----------------------------------------------------------------------------
CREATE OR REPLACE VIEW view_subject_vulnerability_matrix AS
SELECT 
    subject_code,
    subject_title,
    ROUND(AVG(marks), 2) AS average_score,
    SUM(CASE WHEN marks < 40 THEN 1 ELSE 0 END) AS failing_students,
    ROUND(100.0 * SUM(CASE WHEN marks < 40 THEN 1 ELSE 0 END) / COUNT(*), 2) AS failure_rate_pct,
    SUM(CASE WHEN marks >= 75 THEN 1 ELSE 0 END) AS distinction_students
FROM (
    SELECT 'DBMS' AS subject_code, 'Database Management Systems' AS subject_title, dbms_score AS marks FROM student_performance
    UNION ALL
    SELECT 'DSA' AS subject_code, 'Data Structures & Algorithms' AS subject_title, dsa_score AS marks FROM student_performance
    UNION ALL
    SELECT 'OS' AS subject_code, 'Operating Systems' AS subject_title, os_score AS marks FROM student_performance
    UNION ALL
    SELECT 'CN' AS subject_code, 'Computer Networks' AS subject_title, cn_score AS marks FROM student_performance
    UNION ALL
    SELECT 'BI' AS subject_code, 'Business Intelligence' AS subject_title, bi_score AS marks FROM student_performance
) AS subject_data
GROUP BY subject_code, subject_title
ORDER BY failure_rate_pct DESC;

-- -----------------------------------------------------------------------------
-- Query for Faculty Meeting: Departmental Defaulters & Action List
-- -----------------------------------------------------------------------------
SELECT 
    department,
    COUNT(CASE WHEN attendance_pct < 75.0 THEN 1 END) AS attendance_defaulters,
    COUNT(CASE WHEN result_status = 'Fail' THEN 1 END) AS failed_students,
    COUNT(CASE WHEN risk_category = 'High Risk' THEN 1 END) AS high_risk_students,
    ROUND(AVG(attendance_pct), 1) AS dept_avg_attendance
FROM student_performance
GROUP BY department;
