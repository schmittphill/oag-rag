import streamlit as st
import requests

# Open WebUI API configuration
API_URL = "http://77.93.154.36:8080/api/chat/completions"
API_KEY = "sk-f43d3c66e88943c6bac4816464c22fb2"

# Initialize chat history in session state
if "messages" not in st.session_state:
    st.session_state.messages = []

st.title("Welcome to OAG RAG Demo")
st.text("How can I assist you today?")

# Display chat messages from history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input
if prompt := st.chat_input("You:"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Prepare payload for API request
    payload = {
        "model": "oagmodel",
        "files": [
            {"type": "collection", "id": "4f0d35f4-9191-4366-afd9-0cc303e4d47a"}
        ],
        "messages": st.session_state.messages
    }
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    # Send request to Open WebUI API
    response = requests.post(API_URL, json=payload, headers=headers)

    if response.status_code == 200:
        # Extract assistant's reply
        assistant_reply = response.json()["choices"][0]["message"]["content"]
        # Add assistant's reply to chat history
        st.session_state.messages.append({"role": "assistant", "content": assistant_reply})
        with st.chat_message("assistant"):
            st.markdown(assistant_reply)
    else:
        st.error(f"Error {response.status_code}: {response.text}")
