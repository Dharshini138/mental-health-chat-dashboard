import streamlit as st
import pandas as pd
import openai
from datetime import date
import os
import random
import matplotlib.pyplot as plt
from wordcloud import WordCloud

# ---------- BACKGROUND CSS ----------
def set_bg_with_overlay():
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("https://images.unsplash.com/photo-1507525428034-b723cf961d3e");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}
        
        .main-container {{
            background: rgba(255, 255, 255, 0.6);
            backdrop-filter: blur(10px);
            padding: 2rem;
            border-radius: 15px;
            box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);
            max-width: 900px;
            margin: 2rem auto;
        }}

        .block-container {{
            padding-top: 3rem;
            padding-bottom: 3rem;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# ---------- APPLY STYLING ----------
set_bg_with_overlay()

# ---------- SETTINGS ----------
st.set_page_config(page_title="Mental Health Dashboard", layout="centered")
openai.api_key = "YOUR_OPENAI_API_KEY"  # Replace with your API key

# ---------- UTILS ----------
MOOD_EMOJIS = {
    "Happy": "😊", "Sad": "😢", "Angry": "😠",
    "Anxious": "😰", "Excited": "😄", "Neutral": "😐"
}
MOOD_LIST = list(MOOD_EMOJIS.keys())
CSV_FILE = "mood_log.csv"
QUOTE_LIST = [
    "This too shall pass.",
    "You are stronger than you think.",
    "Be kind to yourself.",
    "Feelings are just visitors. Let them come and go.",
    "Healing takes time, and that's okay."
]
MOOD_QUOTES = {
    "Happy": ["Keep shining!", "Joy is contagious—spread it!"],
    "Sad": ["It’s okay to cry. Healing starts there.", "Every storm runs out of rain."],
    "Angry": ["Breathe. You are in control.", "Let go, not for them, but for you."],
    "Anxious": ["One step at a time.", "You’ve survived 100% of your worst days."],
    "Excited": ["Chase that spark!", "Embrace the moment fully."],
    "Neutral": ["Stillness is powerful.", "Every day is a fresh start."]
}

# ---------- MAIN APP CONTENT ----------
with st.container():
    st.markdown('<div class="main-container">', unsafe_allow_html=True)

    # ---------- HEADER ----------
    st.title("Mental Health Dashboard")
    st.caption("Track your mood, reflect through journaling, and chat with a friendly AI.")

    # ---------- MOOD TRACKER ----------
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

    # ---------- JOURNAL ----------
    st.subheader("2. Daily Journal")
    journal = st.text_area("Write anything that's on your mind...", height=200)
    if st.button("Save Journal"):
        with open(f"journal_{date.today()}.txt", "w") as f:
            f.write(journal)
        st.success("Journal entry saved for today.")

    # ---------- CHATBOT ----------
    st.subheader("3. Chat with MindMate AI")

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = [{"role": "system", "content": "You are a supportive mental health assistant."}]

    user_input = st.chat_input("How are you feeling today?")
    if user_input:
        st.session_state.chat_history.append({"role": "user", "content": user_input})

        with st.spinner("MindMate is listening..."):
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=st.session_state.chat_history
            )
            reply = response.choices[0].message["content"]
            st.session_state.chat_history.append({"role": "assistant", "content": reply})

    for msg in st.session_state.chat_history[1:]:  # Skip system prompt
        st.chat_message(msg["role"]).write(msg["content"])

    # ---------- MOOD TRENDS ----------
    st.subheader("4. Mood Trends")
    if os.path.exists(CSV_FILE):
        df = pd.read_csv(CSV_FILE)
        mood_counts = df["Mood"].value_counts()
        st.bar_chart(mood_counts)
    else:
        st.info("No mood data to show yet. Start tracking to see trends.")

    # ---------- MOOD-BASED QUOTE ----------
    st.subheader("5. Personalized Inspiration")
    if st.button("Get Mood-Based Quote"):
        quote = random.choice(MOOD_QUOTES[mood])
        st.success(f"**{quote}**")

    # ---------- WORD CLOUD FROM JOURNALS ----------
    st.subheader("6. Your Thought Cloud")

    journal_words = ""
    for fname in os.listdir():
        if fname.startswith("journal_") and fname.endswith(".txt"):
            with open(fname, "r") as f:
                journal_words += f.read() + " "

    if journal_words.strip():
        wordcloud = WordCloud(width=800, height=300, background_color="white").generate(journal_words)
        fig, ax = plt.subplots()
        ax.imshow(wordcloud, interpolation='bilinear')
        ax.axis("off")
        st.pyplot(fig)
    else:
        st.info("No journal entries found yet. Start writing to see your thought cloud!")

    # ---------- FOOTER ----------
    st.markdown("---")
    st.markdown("Created with love using Streamlit. Remember, your feelings are valid.")

    st.markdown('</div>', unsafe_allow_html=True)
