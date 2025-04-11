import streamlit as st
import pandas as pd
from datetime import date
import os

def mood_tracker():
    MOOD_EMOJIS = {
        "Happy": "😊", "Sad": "😢", "Angry": "😠",
        "Anxious": "😰", "Excited": "😄", "Neutral": "😐"
    }
    MOOD_LIST = list(MOOD_EMOJIS.keys())
    CSV_FILE = "mood_log.csv"

    st.subheader("1. Daily Mood Tracker")
    mood = st.selectbox("How are you feeling today?", MOOD_LIST)
    st.markdown(f"**Mood Selected:** {MOOD_EMOJIS[mood]} {mood}")
    reason = st.text_area("Would you like to share why? (optional)")

    if st.button("Save Mood"):
        new_entry = pd.DataFrame([[str(date.today()), mood, reason]], columns=["Date", "Mood", "Reason"])
        if os.path.exists(CSV_FILE):
            old = pd.read_csv(CSV_FILE)
            updated = pd.concat([old, new_entry], ignore_index=True)
        else:
            updated = new_entry
        updated.to_csv(CSV_FILE, index=False)
        st.success("Your mood has been saved!")
