import os
import openai
import streamlit as st

from streamlit.logger import get_logger
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.chat_models import ChatOllama


logger = get_logger('Langchain-Chatbot')


def enable_chat_history(func):
    if os.environ.get("OPENAI_API_KEY"):

        
        current_page = func.__qualname__
        if "current_page" not in st.session_state:
            st.session_state["current_page"] = current_page
        if st.session_state["current_page"] != current_page:
            try:
                st.cache_resource.clear()
                del st.session_state["current_page"]
                del st.session_state["messages"]
            except:
                pass

        
        if "messages" not in st.session_state:
            st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]
        for msg in st.session_state["messages"]:
            st.chat_message(msg["role"]).write(msg["content"])

    def execute(*args, **kwargs):
        func(*args, **kwargs)
    return execute

def display_msg(msg, author):
    
    st.session_state.messages.append({"role": author, "content": msg})
    st.chat_message(author).write(msg)


@st.cache_resource
def configure_embedding_model():
    api_key = st.secrets["OPENAI_API_KEY"]
    embedding_model = OpenAIEmbeddings(openai_api_key = api_key)
    return embedding_model

def sync_st_session():
    for k, v in st.session_state.items():
        st.session_state[k] = v