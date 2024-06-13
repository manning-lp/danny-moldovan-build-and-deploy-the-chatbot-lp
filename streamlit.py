import streamlit as st
import requests

st.title("Chat with LangChain & ChromaDB")

# Input for user's question
question = st.text_input("Ask a question:")

if st.button("Submit"):
    # API endpoint URL (replace with your actual URL)
    api_url = "http://localhost:8000/chat"

    # Create payload with question and chat history (if applicable)
    data = {"input": {"question": question}}
    
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Send POST request to LangServe API
    response = requests.post(api_url, json=data)

    # Handle response
    if response.status_code == 200:
        answer = response.json()["result"]
        st.session_state.messages.append({"role": "user", "content": question})
        st.session_state.messages.append({"role": "assistant", "content": answer})

        # Display chat history
        for message in st.session_state.messages:
            if message["role"] == "user":
                st.write(f"User: {message['content']}")
            elif message["role"] == "assistant":
                st.write(f"Bot:expand_more {message['content']}")
    else:
        st.error(f"Error: {response.status_code}")