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

# ----------------------------
# Submit Button
# ----------------------------
if st.button("Submit"):
    if name.strip() and subject.strip():
        st.session_state.records.append(
            {
                "Name": name,
                "Subject": subject,
                "Hours": hours
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

    # Dashboard
    st.subheader("📊 Dashboard")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("📚 Total Hours", f"{df['Hours'].sum():.1f}")
    col2.metric("📖 Subjects", df["Subject"].nunique())
    col3.metric("📝 Records", len(df))
    col4.metric("⏱️ Avg Hrs/Session", f"{df['Hours'].sum()/len(df):.2f}")

    top_subject = df.groupby("Subject")["Hours"].sum().idxmax()
    top_hours = df.groupby("Subject")["Hours"].sum().max()

    st.success(f"🏆 Most Studied Subject: {top_subject} ({top_hours} hours)")

    # Study Records
    st.subheader("📋 Study Records")
    st.dataframe(df, width='stretch')

    # Subject-wise Chart
    st.subheader("📈 Subject-wise Study Hours")

    subject_hours = df.groupby("Subject")["Hours"].sum()
    st.bar_chart(subject_hours)

    # Download CSV
    csv = df.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="📥 Download Study Records",
        data=csv,
        file_name="study_records.csv",
        mime="text/csv"
    )

# ----------------------------
# Grade Predictor
# ----------------------------
st.divider()
st.subheader("🎯 Grade Predictor (Machine Learning)")

train_hours = np.array([[1], [2], [3], [4], [5], [6], [7], [8]])
train_marks = np.array([35, 45, 55, 60, 68, 75, 85, 92])

model = LinearRegression()
model.fit(train_hours, train_marks)

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