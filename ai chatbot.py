import streamlit as st
import openai

def ai_chatbot():
    st.subheader("3. Chat with MindMate AI")

    openai.api_key = "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"  # Replace securely in deployment

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

    for msg in st.session_state.chat_history[1:]:
        st.chat_message(msg["role"]).write(msg["content"])
