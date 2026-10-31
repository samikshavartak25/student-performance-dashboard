-- ==============================================================================
-- Project: Student Performance Analysis Dashboard
-- Developer: Samiksha Prashant Vartak
-- Component: 02_data_cleaning.sql - SQL Data Cleaning & Validation Queries
-- Demonstrates: Deduplication, String Normalization, Range Checks, Null Imputation
-- ==============================================================================

-- -----------------------------------------------------------------------------
-- Step 1: Detect and Remove Duplicate Rows using Common Table Expressions (CTE)
-- -----------------------------------------------------------------------------
WITH DuplicateRecords AS (
    SELECT 
        stage_id,
        Student_ID,
        ROW_NUMBER() OVER (
            PARTITION BY Student_ID 
            ORDER BY stage_id ASC
        ) as row_num
    FROM raw_students_staging
)
DELETE FROM raw_students_staging 
WHERE stage_id IN (
    SELECT stage_id FROM DuplicateRecords WHERE row_num > 1
);

-- -----------------------------------------------------------------------------
-- Step 2: Handle Inconsistent Text Casing and Whitespace
-- Standardize Branch Names & Student Names
-- -----------------------------------------------------------------------------
UPDATE raw_students_staging
SET 
    Student_Name = TRIM(REGEXP_REPLACE(Student_Name, '\\s+', ' ')),
    Branch = CASE 
        WHEN LOWER(TRIM(Branch)) LIKE '%business%' OR LOWER(TRIM(Branch)) = 'csbs' THEN 'Computer Science & Business Systems'
        WHEN LOWER(TRIM(Branch)) LIKE '%computer%' OR LOWER(TRIM(Branch)) = 'ce' THEN 'Computer Engineering'
        WHEN LOWER(TRIM(Branch)) LIKE '%information%' OR LOWER(TRIM(Branch)) = 'it' THEN 'Information Technology'
        WHEN LOWER(TRIM(Branch)) LIKE '%artificial%' OR LOWER(TRIM(Branch)) = 'aids' THEN 'Artificial Intelligence & Data Science'
        ELSE TRIM(Branch)
    END;

-- -----------------------------------------------------------------------------
-- Step 3: Impute Missing Attendance & Validate Out-of-Range Percentages
-- Impute missing attendance with departmental median/average (75.0)
-- Cap any erroneous values > 100 or < 0
-- -----------------------------------------------------------------------------
UPDATE raw_students_staging
SET Attendance = '75.0'
WHERE Attendance IS NULL OR TRIM(Attendance) = '';

UPDATE raw_students_staging
SET Attendance = CASE 
    WHEN CAST(Attendance AS DECIMAL(5,2)) > 100.0 THEN '100.0'
    WHEN CAST(Attendance AS DECIMAL(5,2)) < 0.0 THEN '0.0'
    ELSE Attendance
END;

-- -----------------------------------------------------------------------------
-- Step 4: Validate Scores (Pass threshold: 40 marks, Max: 100)
-- -----------------------------------------------------------------------------
UPDATE raw_students_staging
SET 
    DBMS = LEAST(100, GREATEST(0, DBMS)),
    DSA  = LEAST(100, GREATEST(0, DSA)),
    OS   = LEAST(100, GREATEST(0, OS)),
    CN   = LEAST(100, GREATEST(0, CN)),
    BI   = LEAST(100, GREATEST(0, BI));

-- -----------------------------------------------------------------------------
-- Step 5: Transform and Insert Cleaned Records into Production Table
-- Computes Total Score, Overall Percentage, Pass/Fail, and Risk Category
-- -----------------------------------------------------------------------------
INSERT INTO student_performance (
    student_id,
    first_name,
    last_name,
    full_name,
    gender,
    department,
    semester,
    attendance_pct,
    dbms_score,
    dsa_score,
    os_score,
    cn_score,
    bi_score,
    internal_assessment,
    total_score,
    overall_pct,
    failed_subject_count,
    failed_subjects,
    result_status,
    grade,
    risk_category
)
SELECT 
    Student_ID,
    SUBSTRING_INDEX(Student_Name, ' ', 1) AS first_name,
    SUBSTRING_INDEX(Student_Name, ' ', -1) AS last_name,
    Student_Name AS full_name,
    Gender,
    Branch AS department,
    Sem AS semester,
    CAST(Attendance AS DECIMAL(5, 2)) AS attendance_pct,
    DBMS,
    DSA,
    OS,
    CN,
    BI,
    Internal_Score,
    (DBMS + DSA + OS + CN + BI) AS total_score,
    ROUND((DBMS + DSA + OS + CN + BI) / 5.0, 2) AS overall_pct,
    (
        (CASE WHEN DBMS < 40 THEN 1 ELSE 0 END) +
        (CASE WHEN DSA < 40 THEN 1 ELSE 0 END) +
        (CASE WHEN OS < 40 THEN 1 ELSE 0 END) +
        (CASE WHEN CN < 40 THEN 1 ELSE 0 END) +
        (CASE WHEN BI < 40 THEN 1 ELSE 0 END)
    ) AS failed_subject_count,
    TRIM(TRAILING ', ' FROM CONCAT(
        CASE WHEN DBMS < 40 THEN 'DBMS, ' ELSE '' END,
        CASE WHEN DSA < 40 THEN 'DSA, ' ELSE '' END,
        CASE WHEN OS < 40 THEN 'OS, ' ELSE '' END,
        CASE WHEN CN < 40 THEN 'CN, ' ELSE '' END,
        CASE WHEN BI < 40 THEN 'BI, ' ELSE '' END
    )) AS failed_subjects,
    CASE 
        WHEN DBMS >= 40 AND DSA >= 40 AND OS >= 40 AND CN >= 40 AND BI >= 40 THEN 'Pass'
        ELSE 'Fail'
    END AS result_status,
    CASE 
        WHEN (DBMS + DSA + OS + CN + BI) / 5.0 >= 85 THEN 'A+'
        WHEN (DBMS + DSA + OS + CN + BI) / 5.0 >= 75 THEN 'A'
        WHEN (DBMS + DSA + OS + CN + BI) / 5.0 >= 60 THEN 'B'
        WHEN (DBMS + DSA + OS + CN + BI) / 5.0 >= 50 THEN 'C'
        WHEN (DBMS + DSA + OS + CN + BI) / 5.0 >= 40 THEN 'D'
        ELSE 'F'
    END AS grade,
    CASE 
        WHEN CAST(Attendance AS DECIMAL(5,2)) < 75.0 AND (
            (DBMS < 40 OR DSA < 40 OR OS < 40 OR CN < 40 OR BI < 40) OR ((DBMS + DSA + OS + CN + BI) / 5.0 < 45)
        ) THEN 'High Risk'
        WHEN CAST(Attendance AS DECIMAL(5,2)) < 75.0 OR ((DBMS + DSA + OS + CN + BI) / 5.0 < 50) THEN 'Medium Risk'
        ELSE 'Low Risk'
    END AS risk_category
FROM raw_students_staging;
