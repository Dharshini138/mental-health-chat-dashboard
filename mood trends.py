import streamlit as st
import pandas as pd
import os

def mood_trends():
    st.subheader("4. Mood Trends")
    if os.path.exists("mood_log.csv"):
        df = pd.read_csv("mood_log.csv")
        mood_counts = df["Mood"].value_counts()
        st.bar_chart(mood_counts)
    else:
        st.info("No mood data to show yet. Start tracking to see trends.")
