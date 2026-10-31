"""
Dataset Generator & Preprocessor for Student Performance Analysis Dashboard
Author: Samiksha Prashant Vartak (Project Implementation)
Generates 250 realistic student records, produces raw flawed data and cleaned production data.
"""

import csv
import json
import random
import sqlite3
import os

# Set random seed for reproducibility
random.seed(42)

PROJECT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DATA_DIR = os.path.join(PROJECT_DIR, "data")
os.makedirs(DATA_DIR, exist_ok=True)

FIRST_NAMES_MALE = [
    "Aarav", "Rohan", "Aditya", "Prathamesh", "Omkar", "Sanket", "Tanmay", "Atharva",
    "Sahil", "Kunal", "Swapnil", "Harsh", "Akash", "Gaurav", "Nikhil", "Mayur",
    "Vedant", "Yash", "Suyash", "Tejas", "Siddhesh", "Tushar", "Suraj", "Chetan"
]

FIRST_NAMES_FEMALE = [
    "Samiksha", "Sneha", "Ananya", "Pranali", "Riddhi", "Siddhi", "Mrunal", "Pooja",
    "Shruti", "Tanvi", "Sakshi", "Neha", "Ishita", "Divya", "Sayali", "Vaishnavi",
    "Akshata", "Priyanka", "Deepali", "Mansi", "Arya", "Shreya", "Aditi", "Kavya"
]

LAST_NAMES = [
    "Vartak", "Patil", "Chavan", "Kadam", "Shinde", "Jadhav", "More", "Gawde",
    "Tambe", "Mhatre", "Deshmukh", "Pawar", "Sawant", "Thakur", "Rane", "Bhoir",
    "Kulkarni", "Joshi", "Bhave", "Salvi", "Dhumal", "Pandey", "Shah", "Mehta"
]

DEPARTMENTS = [
    "Computer Science & Business Systems",
    "Computer Engineering",
    "Information Technology",
    "Artificial Intelligence & Data Science"
]

SEMESTERS = [4, 5, 6]

def generate_students(num_students=250):
    raw_records = []
    clean_records = []

    for i in range(1, num_students + 1):
        stu_id = f"STU{1000 + i}"
        gender = "Female" if random.random() < 0.48 else "Male"
        first = random.choice(FIRST_NAMES_FEMALE if gender == "Female" else FIRST_NAMES_MALE)
        last = random.choice(LAST_NAMES)
        full_name = f"{first} {last}"
        dept = random.choice(DEPARTMENTS)
        sem = random.choice(SEMESTERS)

        # Attendance generation: skewed towards realistic distribution (mean ~78%)
        # 18% of students have low attendance (<75%)
        if random.random() < 0.20:
            attendance = round(random.uniform(42.0, 74.0), 1)
            is_low_att = True
        else:
            attendance = round(random.uniform(75.0, 98.5), 1)
            is_low_att = False

        # Subject marks (0-100) correlated with attendance
        # Students with low attendance have a higher risk of failing (<40)
        def get_subject_marks(subject_bias=0):
            if is_low_att:
                base = random.gauss(48, 16) + subject_bias
            else:
                base = random.gauss(68, 14) + subject_bias
            return max(20, min(99, int(round(base))))

        # DSA and OS typically have slightly tougher distributions
        marks_dbms = get_subject_marks(+2)
        marks_dsa = get_subject_marks(-5)   # DSA identified as low-performance subject
        marks_os = get_subject_marks(-3)    # OS identified as low-performance subject
        marks_cn = get_subject_marks(+1)
        marks_bi = get_subject_marks(+4)

        # Internal Assessment out of 25 (attendance-correlated)
        internal = round(min(25.0, max(8.0, (attendance / 100.0) * 20.0 + random.uniform(1.0, 5.0))), 1)

        # Total Marks out of 500
        total_marks = marks_dbms + marks_dsa + marks_os + marks_cn + marks_bi
        percentage = round(total_marks / 5.0, 2)

        # Failed subjects check (<40 is failing grade)
        failed_subjects = []
        if marks_dbms < 40: failed_subjects.append("DBMS")
        if marks_dsa < 40: failed_subjects.append("DSA")
        if marks_os < 40: failed_subjects.append("OS")
        if marks_cn < 40: failed_subjects.append("CN")
        if marks_bi < 40: failed_subjects.append("BI")

        failed_count = len(failed_subjects)
        passed_all = "Pass" if failed_count == 0 and percentage >= 40.0 else "Fail"

        # Grading logic
        if percentage >= 85.0 and passed_all == "Pass":
            grade = "A+"
        elif percentage >= 75.0 and passed_all == "Pass":
            grade = "A"
        elif percentage >= 60.0 and passed_all == "Pass":
            grade = "B"
        elif percentage >= 50.0 and passed_all == "Pass":
            grade = "C"
        elif percentage >= 40.0 and passed_all == "Pass":
            grade = "D"
        else:
            grade = "F"

        # Risk Classification for Faculty Intervention
        if attendance < 75.0 and (failed_count >= 1 or percentage < 45.0):
            risk = "High Risk"
        elif attendance < 75.0 or percentage < 50.0 or failed_count >= 1:
            risk = "Medium Risk"
        else:
            risk = "Low Risk"

        clean_records.append({
            "student_id": stu_id,
            "first_name": first,
            "last_name": last,
            "full_name": full_name,
            "gender": gender,
            "department": dept,
            "semester": sem,
            "attendance_pct": attendance,
            "dbms_score": marks_dbms,
            "dsa_score": marks_dsa,
            "os_score": marks_os,
            "cn_score": marks_cn,
            "bi_score": marks_bi,
            "internal_assessment": internal,
            "total_score": total_marks,
            "overall_pct": percentage,
            "failed_subject_count": failed_count,
            "failed_subjects": ", ".join(failed_subjects) if failed_subjects else "None",
            "result_status": passed_all,
            "grade": grade,
            "risk_category": risk
        })

        # Create raw representation with occasional flaws (dirty data)
        raw_dept = dept
        raw_name = full_name
        raw_att = str(attendance)

        # Flaw injection in ~8% of records
        if i % 15 == 0:
            raw_dept = dept.lower()  # Inconsistent casing
        elif i % 25 == 0:
            raw_name = f"  {full_name.upper()}  "  # Whitespace & casing
        elif i == 45:
            raw_att = ""  # Missing attendance in raw
        elif i == 88:
            raw_att = "104.5"  # Out-of-bound entry

        raw_records.append({
            "Student_ID": stu_id,
            "Student_Name": raw_name,
            "Gender": gender,
            "Branch": raw_dept,
            "Sem": sem,
            "Attendance": raw_att,
            "DBMS": marks_dbms,
            "DSA": marks_dsa,
            "OS": marks_os,
            "CN": marks_cn,
            "BI": marks_bi,
            "Internal_Score": internal
        })

        # Inject 2 intentional duplicates into raw dataset
        if i in (50, 120):
            raw_records.append(raw_records[-1].copy())

    return raw_records, clean_records

def main():
    raw_data, clean_data = generate_students(250)

    # 1. Save Raw Data
    raw_csv_path = os.path.join(DATA_DIR, "raw_students_data.csv")
    with open(raw_csv_path, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(raw_data[0].keys()))
        writer.writeheader()
        writer.writerows(raw_data)
    print(f"Generated raw data: {raw_csv_path} ({len(raw_data)} rows)")

    # 2. Save Cleaned Data
    clean_csv_path = os.path.join(DATA_DIR, "cleaned_students_data.csv")
    with open(clean_csv_path, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(clean_data[0].keys()))
        writer.writeheader()
        writer.writerows(clean_data)
    print(f"Generated cleaned data: {clean_csv_path} ({len(clean_data)} rows)")

    # 3. Save JSON for web dashboard
    json_path = os.path.join(PROJECT_DIR, "web", "students_data.json")
    with open(json_path, mode="w", encoding="utf-8") as f:
        json.dump(clean_data, f, indent=2)
    print(f"Generated web dashboard JSON: {json_path}")

    # 4. Populate SQLite Database
    db_path = os.path.join(DATA_DIR, "student_performance.db")
    if os.path.exists(db_path):
        os.remove(db_path)

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Create tables
    cursor.execute("""
    CREATE TABLE students (
        student_id TEXT PRIMARY KEY,
        first_name TEXT NOT NULL,
        last_name TEXT NOT NULL,
        full_name TEXT NOT NULL,
        gender TEXT NOT NULL,
        department TEXT NOT NULL,
        semester INTEGER NOT NULL,
        attendance_pct REAL NOT NULL,
        dbms_score INTEGER NOT NULL,
        dsa_score INTEGER NOT NULL,
        os_score INTEGER NOT NULL,
        cn_score INTEGER NOT NULL,
        bi_score INTEGER NOT NULL,
        internal_assessment REAL NOT NULL,
        total_score INTEGER NOT NULL,
        overall_pct REAL NOT NULL,
        failed_subject_count INTEGER NOT NULL,
        failed_subjects TEXT NOT NULL,
        result_status TEXT NOT NULL,
        grade TEXT NOT NULL,
        risk_category TEXT NOT NULL
    );
    """)

    insert_sql = """
    INSERT INTO students (
        student_id, first_name, last_name, full_name, gender, department, semester,
        attendance_pct, dbms_score, dsa_score, os_score, cn_score, bi_score,
        internal_assessment, total_score, overall_pct, failed_subject_count,
        failed_subjects, result_status, grade, risk_category
    ) VALUES (
        :student_id, :first_name, :last_name, :full_name, :gender, :department, :semester,
        :attendance_pct, :dbms_score, :dsa_score, :os_score, :cn_score, :bi_score,
        :internal_assessment, :total_score, :overall_pct, :failed_subject_count,
        :failed_subjects, :result_status, :grade, :risk_category
    );
    """
    cursor.executemany(insert_sql, clean_data)
    conn.commit()
    conn.close()
    print(f"Populated SQLite database: {db_path} with {len(clean_data)} records.")

if __name__ == "__main__":
    main()
