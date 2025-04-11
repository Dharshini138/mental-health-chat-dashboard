import streamlit as st
from datetime import date

def daily_journal():
    st.subheader("2. Daily Journal")
    journal = st.text_area("Write anything that's on your mind...", height=200)
    if st.button("Save Journal"):
        with open(f"journal_{date.today()}.txt", "w") as f:
            f.write(journal)
        st.success("Journal entry saved for today.")
