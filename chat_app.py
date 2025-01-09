import streamlit as st
import requests

#from openai import OpenAI
import uuid
import sys
import json
import readline  # For better input handling
from rich import print as rprint
from rich.console import Console
from rich.prompt import Prompt
from rich.progress import Progress

# ANSI escape codes for text colors
BLUE = "\033[1;34m"
GREEN = "\033[1;32m"
RED = "\033[1;31m"
RESET = "\033[0m"

# Open WebUI API configuration
API_URL = "http://77.93.154.36:8080/api/chat/completions"
API_KEY = "sk-8231b72c44d943608ad23784e3f4a095"
RESPONSE = ""

st.subheader("OAG RAG Demo", divider="red", anchor=False)

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
        
def print_highlight(message, color=BLUE):
    print(f"\n{color}{message}{RESET}")

def process_stream_response(response):
    #full_response = ""
    for line in response.iter_lines():
        if line:
            try:
                json_response = json.loads(line.decode('utf-8').split('data: ')[1])
                if 'choices' in json_response and json_response['choices']:
                    content = json_response['choices'][0].get('delta', {}).get('content', '')
                    if content:
                        print(f"{BLUE}{content}{RESET}", end='', flush=True)
                        full_response += content
                elif 'usage' in json_response:
                    print(f"\n\n{GREEN}Usage: {json_response['usage']}{RESET}")
            except json.JSONDecodeError:
                if b'data: [DONE]' in line:
                    continue  # Skip the [DONE] message
                print(f"{RED}Error decoding JSON: {line}{RESET}")
    print()  # Add a newline at the end
    return full_response

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
            "stream_options": {"include_usage": True},
            #"files": [
            #    {"type": "collection", "id": "656f6122-d11b-45d1-a1f7-1dac7bbf8097"}
            #],
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

        

    def defunc_code():

        for line in chat_reponse.iter_lines():
            if line:
                print(line)

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

        try:
            RESPONSE = ""
            with requests.post(API_URL, json=payload, headers=headers, stream=True) as chat_response:
                chat_response.raise_for_status()
                ##ai_response = process_stream_response(chat_response)
                #messages.append({"role": "assistant", "content": ai_response})

                for line in chat_response.iter_lines():
                    if line:
                        try:
                            json_response = json.loads(line.decode('utf-8').split('data: ')[1])
                            if 'choices' in json_response and json_response['choices']:
                                content = json_response['choices'][0].get('delta', {}).get('content', '')
                                if content:
                                    print(f"{BLUE}{content}{RESET}", end='', flush=True)
                                    RESPONSE += content
                            elif 'usage' in json_response:
                                print(f"\n\n{GREEN}Usage: {json_response['usage']}{RESET}")
                        except json.JSONDecodeError:
                            if b'data: [DONE]' in line:
                                continue  # Skip the [DONE] message
                            print(f"{RED}Error decoding JSON: {line}{RESET}")

                st.session_state.messages.append({"role": "assistant", "content": RESPONSE})
                with st.chat_message("assistant"):
                    st.markdown(RESPONSE)

        except requests.RequestException as e:
            print_highlight(f"Error: {e}", RED)