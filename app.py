import streamlit as st

st.title("Study Tracker")
st.write("Track your daily study progress!")

name = st.text_input("Enter your name:")
subject = st.text_input("Enter subject studied today:")
hours = st.number_input("Hours studied:", min_value=0.0, max_value=24.0, step=0.5)

if st.button("Submit"):
    st.success(f"Great job, {name}! You studied {subject} for {hours} hours today.")