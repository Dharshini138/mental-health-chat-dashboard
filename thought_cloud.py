import streamlit as st
import os
from wordcloud import WordCloud
import matplotlib.pyplot as plt

def thought_cloud():
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
