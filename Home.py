import openai
import requests
import traceback
import os
import streamlit as st
from datetime import datetime
from langchain_openai import OpenAIEmbeddings  # Replace with actual import
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import ChatOpenAI
from langchain.vectorstores import Chroma

from langchain.chains import ConversationalRetrievalChain


from langchain.chains.combine_documents import create_stuff_documents_chain
from utils import enable_chat_history,  sync_st_session, display_msg  # Ensure utils are set up correctly
import validators

from langchain.chains import conversational_retrieval
from langchain_core.prompts import ChatPromptTemplate
from langchain.memory import ConversationBufferMemory
from langchain.schema import Document



class ChatbotWeb:
    def __init__(self):
        sync_st_session()
        self.embedding_model = OpenAIEmbeddings(api_key=st.secrets["OPENAI_API_KEY"])
        self.llm = llm = ChatOpenAI(model="gpt-3.5-turbo-0125", temperature=0.2)

    def scrape_website(self, url):
        """Scrape the content of a given URL."""
        content = ""
        try:
            base_url = "https://r.jina.ai/"
            final_url = base_url + url
            headers = {
                'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:88.0) Gecko/20100101 Firefox/88.0'
            }
            response = requests.get(final_url, headers=headers)
            content = response.text
        except Exception as e:
            traceback.print_exc()
        return content

    @st.cache_resource(show_spinner='Analyzing webpage', ttl=3600)
    def setup_vectordb(_self, websites):
        docs = []
        for url in websites:
            content = _self.scrape_website(url)
            doc = Document(page_content=content, metadata={"source": url})
            docs.append(doc)
        
        text_splitter = RecursiveCharacterTextSplitter(chunk_size = 1000, chunk_overlap = 200)
        splits = text_splitter.split_documents(docs)

        vector_store = Chroma.from_documents(documents = splits, embedding = OpenAIEmbeddings())   
        return vector_store 
    
    def format_docs(docs):
        return "\n\n".join(doc["page_content"] for doc in docs)

    
    
    
    def chain(self, user_query, vector_store):
        retriever = vector_store.as_retriever()

        memory = ConversationBufferMemory(
            memory_key='chat_history',
            output_key='answer',
            return_messages=True
        )

        prompt = ChatPromptTemplate.from_template("""
            Answer the following questions based only on the provided context.
            Think step by step before providing a detailed answer.
            <context>
            {context}
            </context>
            Question: {input}
        """)

        document_chain = create_stuff_documents_chain(self.llm, prompt)

        
        qa_chain = ConversationalRetrievalChain.from_llm(
            llm=self.llm,
            retriever=retriever,
            memory=memory,
            return_source_documents=True,
            verbose=False)
         

        
        response = qa_chain({"question":user_query})

        
        answer = response.get("answer")
        docs = response.get("source_documents", [])

        return answer, docs

        
        
    
    
    @enable_chat_history
    def main(self):
        """Main function to run the Streamlit app."""
        if "websites" not in st.session_state:
            st.session_state["websites"] = []

        web_url = st.sidebar.text_area(
            label='Enter Website URL',
            placeholder="https://",
            help="To add another website, modify this field after adding the website."
        )

        if st.sidebar.button(":heavy_plus_sign: Add Website"):
            valid_url = web_url.startswith('http') and validators.url(web_url)
            if not valid_url:
                st.sidebar.error("Invalid URL! Please check the website URL you have entered.", icon="⚠️")
            else:
                st.session_state["websites"].append(web_url)

        if st.sidebar.button("Clear", type="primary"):
            st.session_state["websites"] = []

        websites = list(set(st.session_state["websites"]))

        if not websites:
            st.error("Please enter a website URL to continue!")
            st.stop()
        else:
            st.sidebar.info("Websites:\n - {}".format('\n - '.join(websites)))

            
            vector_store = self.setup_vectordb(websites)

            user_query = st.chat_input(placeholder="Ask me anything!")
            if user_query:
                response, docs = self.chain(user_query, vector_store)

               
                display_msg(user_query, 'user')
                display_msg(response, 'assistant')

                
                for idx, doc in enumerate(docs, 1):
                    url = os.path.basename(doc.metadata['source'])
                    ref_title = f":blue[Reference {idx}: *{url}*]"
                    with st.expander(ref_title):
                        st.caption(doc.page_content)  

if __name__ == "__main__":
    chatbot = ChatbotWeb()
    chatbot.main()
    