import streamlit as st
import pandas as pd
from sklearn.linear_model import LinearRegression
import numpy as np

st.title("Study Tracker")
st.write("Track your daily study progress!")

if "records" not in st.session_state:
    st.session_state.records = []

name = st.text_input("Enter your name:")
subject = st.text_input("Enter subject studied today:")
hours = st.number_input("Hours studied:", min_value=0.0, max_value=24.0, step=0.5)

if st.button("Submit"):
    st.session_state.records.append({"Name": name, "Subject": subject, "Hours": hours})
    st.success(f"Great job, {name}! You studied {subject} for {hours} hours today.")

if st.session_state.records:
    st.subheader("Your Study Records")
    df = pd.DataFrame(st.session_state.records)
    st.dataframe(df, use_container_width=True)

    total_hours = df["Hours"].sum()
    st.write(f"**Total Hours Studied:** {total_hours}")

st.subheader("Grade Predictor (Real ML Model)")

train_hours = np.array([[1], [2], [3], [4], [5], [6], [7], [8]])
train_marks = np.array([35, 45, 55, 60, 68, 75, 85, 92])

model = LinearRegression()
model.fit(train_hours, train_marks)

predict_hours = st.number_input("Enter hours studied to predict marks:", min_value=0.0, max_value=24.0, step=0.5, key="predict")

if st.button("Predict Marks"):
    try:
        predicted = model.predict([[predict_hours]])
        predicted_marks = predicted[0]
        if predicted_marks > 100:
            predicted_marks = 100
        if predicted_marks < 0:
            predicted_marks = 0
        st.info(f"Estimated Marks: {predicted_marks:.2f}")
    except Exception as e:
        st.error("Something went wrong. Please try again.")