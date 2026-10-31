"""
Student Performance Analysis Dashboard - Streamlit Application
Author: Samiksha Prashant Vartak
Can be deployed to Streamlit Community Cloud (share.streamlit.io)
"""

import os
import sqlite3
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Student Performance Dashboard | Samiksha Vartak",
    page_icon="🎓",
    layout="wide"
)

# Database connection
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DB_PATH = os.path.join(BASE_DIR, "data", "student_performance.db")

@st.cache_data
def load_data():
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("SELECT * FROM students", conn)
    conn.close()
    return df

try:
    df = load_data()
except Exception:
    csv_path = os.path.join(BASE_DIR, "data", "cleaned_students_data.csv")
    df = pd.read_csv(csv_path)

# Header
st.title("🎓 Student Performance Analysis Dashboard")
st.markdown("**Academic Performance Audit & Faculty Intervention System** • Developed by **Samiksha Prashant Vartak**")

# Sidebar Filters
st.sidebar.header("🔍 Interactive Slicers")
dept_list = ["All"] + sorted(list(df["department"].unique()))
selected_dept = st.sidebar.selectbox("Department", dept_list)

sem_list = ["All"] + sorted([str(s) for s in df["semester"].unique()])
selected_sem = st.sidebar.selectbox("Semester", sem_list)

risk_list = ["All"] + sorted(list(df["risk_category"].unique()))
selected_risk = st.sidebar.selectbox("Faculty Risk Category", risk_list)

status_list = ["All", "Pass", "Fail"]
selected_status = st.sidebar.selectbox("Pass / Fail Trend", status_list)

# Apply filters
filtered_df = df.copy()
if selected_dept != "All":
    filtered_df = filtered_df[filtered_df["department"] == selected_dept]
if selected_sem != "All":
    filtered_df = filtered_df[filtered_df["semester"] == int(selected_sem)]
if selected_risk != "All":
    filtered_df = filtered_df[filtered_df["risk_category"] == selected_risk]
if selected_status != "All":
    filtered_df = filtered_df[filtered_df["result_status"] == selected_status]

# KPI Metric Cards
col1, col2, col3, col4, col5 = st.columns(5)
total_students = len(filtered_df)
pass_count = len(filtered_df[filtered_df["result_status"] == "Pass"])
pass_rate = round((pass_count / total_students * 100), 1) if total_students > 0 else 0
avg_att = round(filtered_df["attendance_pct"].mean(), 1) if total_students > 0 else 0
avg_score = round(filtered_df["overall_pct"].mean(), 1) if total_students > 0 else 0
high_risk_count = len(filtered_df[filtered_df["risk_category"] == "High Risk"])

col1.metric("Total Students", total_students)
col2.metric("Pass Rate", f"{pass_rate}%", f"{pass_count} passed")
col3.metric("Avg Attendance", f"{avg_att}%")
col4.metric("Avg Score", f"{avg_score}%")
col5.metric("High-Risk Count", high_risk_count, delta="Requires Attention", delta_color="inverse")

# Alert Banner
st.info(
    "💡 **Key Finding:** Students with attendance < 75% exhibit an **85.7% failure rate** vs 11.9% for regular students. "
    "**Data Structures (DSA)** and **Operating Systems (OS)** are identified as critical low-performance areas."
)

# Tabs
tab1, tab2, tab3 = st.tabs(["📊 Performance Charts", "📋 Student Roster & Drill-Down", "📑 Faculty Review Report"])

with tab1:
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Subject-Wise Average Score & Low-Performance Areas")
        subj_avg = pd.DataFrame({
            "Subject": ["DBMS", "DSA (Low)", "OS (Low)", "CN", "BI"],
            "Average Marks": [
                filtered_df["dbms_score"].mean(),
                filtered_df["dsa_score"].mean(),
                filtered_df["os_score"].mean(),
                filtered_df["cn_score"].mean(),
                filtered_df["bi_score"].mean()
            ]
        }).set_index("Subject")
        st.bar_chart(subj_avg)

    with c2:
        st.subheader("Attendance vs Overall Score (Risk Quadrants)")
        st.scatter_chart(
            data=filtered_df,
            x="attendance_pct",
            y="overall_pct",
            color="risk_category"
        )

    c3, c4 = st.columns(2)
    with c3:
        st.subheader("Department-Wise Average Percentage")
        dept_avg = filtered_df.groupby("department")["overall_pct"].mean()
        st.bar_chart(dept_avg)

    with c4:
        st.subheader("Grade Distribution")
        grade_counts = filtered_df["grade"].value_counts()
        st.bar_chart(grade_counts)

with tab2:
    st.subheader("Student Master Roster")
    st.dataframe(filtered_df[[
        "student_id", "full_name", "department", "semester", "attendance_pct",
        "overall_pct", "dbms_score", "dsa_score", "os_score", "cn_score", "bi_score",
        "result_status", "grade", "risk_category", "failed_subjects"
    ]], use_container_width=True)

    csv = filtered_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download Filtered Student Data as CSV",
        data=csv,
        file_name='student_performance_filtered.csv',
        mime='text/csv',
    )

with tab3:
    st.subheader("Faculty Review Summary & Intervention Strategy")
    st.markdown("""
    ### 1. Executive Summary
    - **Scope:** 250 engineering students audited across semesters 4 to 6.
    - **High-Risk Threshold:** Attendance < 75% or failure in $\\ge$ 1 course.
    
    ### 2. Identified Vulnerabilities
    - **DSA & OS:** Identified as primary low-performance areas with lowest cohort averages and highest failure rates (12.0%).
    - **Attendance Link:** 85.7% of attendance defaulters failed end-semester assessments.
    
    ### 3. Recommended Actions
    1. Mandatory remedial lab clinics for DSA & OS.
    2. Attendance warning letters to parents of 49 attendance defaulters.
    3. Bi-weekly formative quizzes to prevent concept lag.
    """)
