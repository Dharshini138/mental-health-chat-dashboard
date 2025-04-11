import streamlit as st
from mood_tracker import mood_tracker
from daily_journal import daily_journal
from ai_chatbot import ai_chatbot
from mood_trends import mood_trends
from mood_quotes import mood_quotes
from thought_cloud import thought_cloud
from footer import show_footer

st.set_page_config(page_title="Mental Health Dashboard", layout="centered")

st.title("🧠 Mental Health Dashboard")
st.caption("Track your mood, reflect, and chat with a friendly AI.")

# Mood tracking first to share mood variable
mood_tracker()
daily_journal()
ai_chatbot()
mood_trends()
mood_quotes(st.session_state.get("mood", "Neutral"))
thought_cloud()
show_footer()
