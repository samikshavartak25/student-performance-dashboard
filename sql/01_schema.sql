-- ==============================================================================
-- Project: Student Performance Analysis Dashboard
-- Developer: Samiksha Prashant Vartak
-- Component: 01_schema.sql - Database Schema Definition
-- Compatible with: MySQL 8.0+, PostgreSQL 14+, SQLite 3
-- ==============================================================================

-- Drop tables if already existing for clean deployment
DROP TABLE IF EXISTS student_performance;
DROP TABLE IF EXISTS raw_students_staging;

-- 1. Raw Staging Table (For data ingestion from Excel/CSV before cleaning)
CREATE TABLE raw_students_staging (
    stage_id INT AUTO_INCREMENT PRIMARY KEY,
    Student_ID VARCHAR(20),
    Student_Name VARCHAR(100),
    Gender VARCHAR(15),
    Branch VARCHAR(100),
    Sem INT,
    Attendance VARCHAR(20),
    DBMS INT,
    DSA INT,
    OS INT,
    CN INT,
    BI INT,
    Internal_Score DECIMAL(4, 1),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. Production Student Performance Table (Cleaned & Normalized)
CREATE TABLE student_performance (
    student_id VARCHAR(20) PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    full_name VARCHAR(100) NOT NULL,
    gender ENUM('Male', 'Female') NOT NULL,
    department VARCHAR(100) NOT NULL,
    semester INT NOT NULL CHECK (semester BETWEEN 1 AND 8),
    attendance_pct DECIMAL(5, 2) NOT NULL CHECK (attendance_pct BETWEEN 0.0 AND 100.0),
    dbms_score INT NOT NULL CHECK (dbms_score BETWEEN 0 AND 100),
    dsa_score INT NOT NULL CHECK (dsa_score BETWEEN 0 AND 100),
    os_score INT NOT NULL CHECK (os_score BETWEEN 0 AND 100),
    cn_score INT NOT NULL CHECK (cn_score BETWEEN 0 AND 100),
    bi_score INT NOT NULL CHECK (bi_score BETWEEN 0 AND 100),
    internal_assessment DECIMAL(4, 1) NOT NULL,
    total_score INT NOT NULL,
    overall_pct DECIMAL(5, 2) NOT NULL,
    failed_subject_count INT NOT NULL DEFAULT 0,
    failed_subjects VARCHAR(100) DEFAULT 'None',
    result_status ENUM('Pass', 'Fail') NOT NULL,
    grade VARCHAR(5) NOT NULL,
    risk_category ENUM('Low Risk', 'Medium Risk', 'High Risk') NOT NULL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- 3. Performance Indexes for Query Optimization
CREATE INDEX idx_student_dept ON student_performance (department);
CREATE INDEX idx_student_sem ON student_performance (semester);
CREATE INDEX idx_student_attendance ON student_performance (attendance_pct);
CREATE INDEX idx_student_result ON student_performance (result_status);
CREATE INDEX idx_student_risk ON student_performance (risk_category);
