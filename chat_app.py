import streamlit as st
import requests

# Open WebUI API configuration
API_URL = "http://77.93.154.36:8080/api/chat/completions"
API_KEY = "sk-8231b72c44d943608ad23784e3f4a095"

# Initialize chat history in session state
if "messages" not in st.session_state:
    st.session_state.messages = []

st.title("Welcome to OAG RAG Demo")

def creds_entered():
    if st.session_state["user"].strip() == "test@oagrag.demo" and st.session_state["passwd"].strip() == "adm!n12E":
        st.session_state["authenticated"] = True
    else:
        st.session_state["authenticated"] = False 
        st.error("Invalid Username/Password :face_with_raised_eye_brow:")


def authenticate_user():
    if "authenticated" not in st.session_state:
        st.text("Please enter Username/Password to have access")
        st.text_input(label="Username: ", value="", key="user", on_change=creds_entered)
        st.text_input(label="Password: ", value="", key="passwd", type="password", on_change=creds_entered)
    else:
        if st.session_state["authenticated"]:
            return True
        else:
            st.text("Please enter Username/Password to have access")
            st.text_input(label="Username: ", value="", key="user", on_change=creds_entered)
            st.text_input(label="Password: ", value="", key="passwd", type="password", on_change=creds_entered)
            return False

if authenticate_user():
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
            #"model": "llama3.2:latest",
            "model": "oagmodel",
            "files": [
                {"type": "collection", "id": "656f6122-d11b-45d1-a1f7-1dac7bbf8097"}
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
