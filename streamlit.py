import streamlit as st
import os

os.environ['OPENAI_API_KEY_SECRET']=  st.secrets["OPENAI_API_KEY"]


import requests 
import server as danny_server
from fastapi import FastAPI
import uvicorn
import threading

BACKEND = "localhost"


app = danny_server.app
def start_server():
    uvicorn.run(app, host=BACKEND, port=8000)

# Start the FastAPI server in a separate thread
threading.Thread(target=start_server).start()

# App title
st.set_page_config(page_title="LangChain Chatbot")


# Store LLM generated responses
if "messages" not in st.session_state.keys():
    st.session_state.messages = [{"role": "assistant", "content": "How may I help you?"}]

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Function for generating LLM response
def generate_response(prompt_input):
    inputs = {"input": {"question": prompt_input}}
    response = requests.post("http://localhost:8000/invoke", json=inputs)
    answer = response.json()["output"]["answer"]
    supporting_doc_url = response.json()['output']['source_documents'][0]['page_content'].split("'source':")[1].replace("'", "").replace("}", "").strip()

    return answer + " supporting document: " + supporting_doc_url

# User-provided prompt
if prompt := st.chat_input():
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

# Generate a new response if last message is not from assistant
if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = generate_response(prompt) 
            st.write(response) 
    message = {"role": "assistant", "content": response}
    st.session_state.messages.append(message)
