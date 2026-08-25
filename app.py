import streamlit as st
import pandas as pd
from sklearn.linear_model import LinearRegression
import numpy as np

# ----------------------------
# Page Configuration
# ----------------------------
st.set_page_config(page_title="Study Tracker", page_icon="📚")

st.title("📚 Study Tracker")
st.write("Track your daily study progress!")

# ----------------------------
# Session State
# ----------------------------
if "records" not in st.session_state:
    st.session_state.records = []

# ----------------------------
# User Input
# ----------------------------
name = st.text_input("Enter your name:")
subject = st.text_input("Enter subject studied today:")
hours = st.number_input(
    "Hours studied:",
    min_value=0.0,
    max_value=24.0,
    step=0.5
)
date = st.date_input("Date:")
marks = st.number_input(
    "Marks scored (out of 100):",
    min_value=0.0,
    max_value=100.0,
    step=1.0
)
# ----------------------------
# Submit Button
# ----------------------------
if st.button("Submit"):
    if name.strip() and subject.strip():
        st.session_state.records.append(
            {
                "Name": name,
                "Subject": subject,
                "Hours": hours,
                "Date": date,
                "Marks": marks
            }
        )
        st.success(f"Great job, {name}! You studied {subject} for {hours} hours today.")
    else:
        st.warning("Please enter your name and subject.")

# ----------------------------
# Display Records
# ----------------------------
if st.session_state.records:

    df = pd.DataFrame(st.session_state.records)
    df["Subject"] = df["Subject"].str.strip().str.title()
    df["Performance"] = df["Marks"].apply(
        lambda x: "🌟 Excellent" if x >= 85 else ("✅ Good" if x >= 70 else "⚠️ Needs Improvement")
    )

    # Dashboard
    st.subheader("📊 Dashboard")

    col1, col2, col3, col4, col5 = st.columns(5)

    col1.metric("📚 Total Hours", f"{df['Hours'].sum():.1f}")
    col2.metric("📖 Subjects", df["Subject"].nunique())
    col3.metric("📝 Records", len(df))
    col4.metric("⏱️ Avg Hrs/Session", f"{df['Hours'].sum()/len(df):.2f}")
    col5.metric("📅 Days Tracked", df["Date"].nunique())

    # Study Streak Counter
    st.subheader("🔥 Study Streak")
    unique_dates = sorted(df["Date"].unique(), reverse=True)
    streak = 0
    today = pd.Timestamp.now().normalize().date()
    for i, d in enumerate(unique_dates):
        expected_date = today - pd.Timedelta(days=i)
        if d == expected_date:
            streak += 1
        else:
            break
    st.metric("Current Streak", f"{streak} days")

    st.subheader("📅 This Week's Summary")
    
    last_7_days = pd.Timestamp.now().normalize().date() - pd.Timedelta(days=7)
    df["Date"] = pd.to_datetime(df["Date"]).dt.date
    week_df = df[df["Date"] >= last_7_days]

    if not week_df.empty:
        col1, col2, col3 = st.columns(3)
        col1.metric("Hours This Week", f"{week_df['Hours'].sum():.1f}")
        col2.metric("Avg Marks", f"{week_df['Marks'].mean():.1f}")
        col3.metric("Sessions", len(week_df))
    else:
        st.info("No study sessions in the last 7 days.")

    st.subheader("📆 This Month's Summary")
    
    df["Date"] = pd.to_datetime(df["Date"])
    current_month = pd.Timestamp.now().month
    current_year = pd.Timestamp.now().year
    month_df = df[(df["Date"].dt.month == current_month) & (df["Date"].dt.year == current_year)]

    if not month_df.empty:
        col1, col2, col3 = st.columns(3)
        col1.metric("Hours This Month", f"{month_df['Hours'].sum():.1f}")
        col2.metric("Avg Marks", f"{month_df['Marks'].mean():.1f}")
        col3.metric("Sessions", len(month_df))
    else:
        st.info("No study sessions this month.")

    top_subject = df.groupby("Subject")["Hours"].sum().idxmax()
    top_hours = df.groupby("Subject")["Hours"].sum().max()

    st.success(f"🏆 Most Studied Subject: {top_subject} ({top_hours} hours)")

    # Study Records
    st.subheader("📋 Study Records")
    selected_subject = st.selectbox(
        "Filter by subject:",
        options=["All"] + list(df["Subject"].unique())
    )
    if selected_subject != "All":
        filtered_df = df[df["Subject"] == selected_subject]
    else:
        filtered_df = df
    st.dataframe(filtered_df, width='stretch')

    # Subject-wise Chart
    st.subheader("📈 Subject-wise Study Hours")
    subject_hours = df.groupby("Subject")["Hours"].sum()
    st.bar_chart(subject_hours)

    # Subject-wise Average Marks
    st.subheader("📊 Subject-wise Average Marks")
    subject_avg_marks = df.groupby("Subject")["Marks"].mean()
    st.bar_chart(subject_avg_marks)

    # Grade Distribution using pd.cut()
    st.subheader("🎓 Grade Distribution")
    df["Grade"] = pd.cut(
        df["Marks"],
        bins=[0, 35, 55, 65, 77, 85, 100],
        labels=["F", "E", "D", "C", "B", "A"]
    )
    grade_counts = df["Grade"].value_counts().sort_index()
    st.bar_chart(grade_counts)

    # Study Pattern by Day of Week
    st.subheader("📅 Study Pattern by Day")
    df["Day_of_Week"] = pd.to_datetime(df["Date"]).dt.day_name()
    day_hours = df.groupby("Day_of_Week")["Hours"].sum()
    st.bar_chart(day_hours)

    st.subheader("📊 Best & Worst Study Day")

    day_hours = df.groupby("Day_of_Week")["Hours"].sum()
    best_day = day_hours.idxmax()
    worst_day = day_hours.idxmin()

    col1, col2 = st.columns(2)
    col1.metric("🏆 Best Day", best_day, f"{day_hours.max():.1f} hrs")
    col2.metric("📉 Needs Focus", worst_day, f"{day_hours.min():.1f} hrs")

    # Marks Trend Chart
    st.subheader("📈 Marks Trend Over Time")
    df_sorted = df.sort_values("Date")
    st.line_chart(df_sorted.set_index("Date")["Marks"])

    st.subheader("📈 Cumulative Study Hours")
    df_sorted_cum = df.sort_values("Date")
    df_sorted_cum["Cumulative_Hours"] = df_sorted_cum["Hours"].cumsum()
    st.line_chart(df_sorted_cum.set_index("Date")["Cumulative_Hours"])

    # Download CSV
    csv = df.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="📥 Download Study Records",
        data=csv,
        file_name="study_records.csv",
        mime="text/csv"
    )

    # Edit a Record
    st.subheader("✏️ Edit a Record")
    record_to_edit = st.selectbox(
        "Select record to edit:",
        options=range(len(df)),
        format_func=lambda i: f"{df.iloc[i]['Name']} - {df.iloc[i]['Subject']} - {df.iloc[i]['Date']}",
        key="edit_select"
    )

    with st.form("edit_form"):
        edit_subject = st.text_input("Subject", value=st.session_state.records[record_to_edit]["Subject"])
        edit_hours = st.number_input(
            "Hours", value=float(st.session_state.records[record_to_edit]["Hours"]),
            min_value=0.0, max_value=24.0, step=0.5
        )
        edit_marks = st.number_input(
            "Marks", value=float(st.session_state.records[record_to_edit]["Marks"]),
            min_value=0.0, max_value=100.0, step=1.0
        )
        update_submitted = st.form_submit_button("Update Record")

        if update_submitted:
            st.session_state.records[record_to_edit]["Subject"] = edit_subject
            st.session_state.records[record_to_edit]["Hours"] = edit_hours
            st.session_state.records[record_to_edit]["Marks"] = edit_marks
            st.success("Record updated!")
            st.rerun()

        
    # Delete Individual Record
    st.subheader("🗑️ Delete a Record")
    record_to_delete = st.selectbox(
        "Select record to delete:",
        options=range(len(df)),
        format_func=lambda i: f"{df.iloc[i]['Name']} - {df.iloc[i]['Subject']} - {df.iloc[i]['Date']}"
    )
    if st.button("Delete Selected Record"):
        st.session_state.records.pop(record_to_delete)
        st.rerun()

    # Clear All Records
    if st.button("🗑️ Clear All Records"):
        st.session_state.records = []
        st.rerun()
# ----------------------------
# Grade Predictor
# ----------------------------
st.divider()
st.subheader("🎯 Grade Predictor (Machine Learning)")

if len(st.session_state.records) >= 2:
    df_ml = pd.DataFrame(st.session_state.records)
    X = df_ml[["Hours"]].values
    y = df_ml["Marks"].values

    model = LinearRegression()
    model.fit(X, y)

    predict_hours = st.number_input(
        "Enter study hours to predict marks:",
        min_value=0.0,
        max_value=24.0,
        step=0.5,
        key="predict"
    )

    if st.button("Predict Marks"):
        predicted_marks = model.predict([[predict_hours]])[0]
        predicted_marks = max(0, min(100, predicted_marks))
        st.success(f"📈 Estimated Marks: {predicted_marks:.2f}")
else:
    st.warning("⚠️ Add at least 2 study records with marks to enable predictions.")