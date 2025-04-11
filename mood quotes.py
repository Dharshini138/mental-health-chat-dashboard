import streamlit as st
import random

def mood_quotes(current_mood):
    st.subheader("5. Personalized Inspiration")

    MOOD_QUOTES = {
        "Happy": ["Keep shining!", "Joy is contagious—spread it!"],
        "Sad": ["It’s okay to cry. Healing starts there.", "Every storm runs out of rain."],
        "Angry": ["Breathe. You are in control.", "Let go, not for them, but for you."],
        "Anxious": ["One step at a time.", "You’ve survived 100% of your worst days."],
        "Excited": ["Chase that spark!", "Embrace the moment fully."],
        "Neutral": ["Stillness is powerful.", "Every day is a fresh start."]
    }

    if st.button("Get Mood-Based Quote"):
        quote = random.choice(MOOD_QUOTES.get(current_mood, ["Stay strong."]))
        st.success(f"**{quote}**")
