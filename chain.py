__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

import streamlit as st

from langchain.chains import ConversationalRetrievalChain
from langchain_community.chat_models import ChatOpenAI
# from langchain_community.embeddings import OpenAIEmbeddings
from langchain.memory import ConversationBufferMemory
# from langchain_community.vectorstores import Chroma
from langchain.vectorstores import Chroma
from langchain.embeddings.openai import OpenAIEmbeddings
import os
from dotenv import load_dotenv
import chromadb
from chromadb.config import DEFAULT_TENANT, DEFAULT_DATABASE, Settings


load_dotenv()

persist_directory = "chroma_db"

if 'OPENAI_API_KEY' in os.environ:
    openai_api_key = os.environ['OPENAI_API_KEY']
else:
    openai_api_key = st.secrets["OPENAI_API_KEY"]
    

embedding = OpenAIEmbeddings(openai_api_key=openai_api_key)
chroma_client = chromadb.PersistentClient(
    path="chroma_db",
    settings=Settings(),
    tenant=DEFAULT_TENANT,
    database=DEFAULT_DATABASE,
)
vector_store = Chroma(
    collection_name="langchain_store",  # The name of the collection in your Chroma DB
    client=chroma_client,  # The initialized Chroma client
    embedding_function=embedding
)

retriever = vector_store.as_retriever()

# Conversation memory
memory = ConversationBufferMemory(memory_key="chat_history", output_key='answer', return_messages=True)

# Initialize OpenAI language model
llm = ChatOpenAI(temperature=0, openai_api_key=os.environ['OPENAI_API_KEY'])

# Create ConversationalRetrievalChain
qa_chain = ConversationalRetrievalChain.from_llm(
    llm=llm,
    retriever=retriever,
    memory=memory,
    return_source_documents=True,
    verbose=True
)