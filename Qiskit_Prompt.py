import os
from dotenv import load_dotenv
from llama_index.core.node_parser import SimpleNodeParser
from llama_index.llms.openai import OpenAI
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.core import download_loader, ServiceContext, VectorStoreIndex,SimpleDirectoryReader,StorageContext,set_global_service_context
from llama_index.vector_stores.pinecone import PineconeVectorStore
from llama_index.core.node_parser import SentenceSplitter

from llama_index.core import Settings

from pinecone import Pinecone,ServerlessSpec
import streamlit as st
load_dotenv()





index_name = "qiskit-documentation-helper"
cloud = os.environ.get('PINECONE_CLOUD') or 'aws'
region = os.environ.get('PINECONE_REGION') or 'us-east-1'

spec = ServerlessSpec(cloud=cloud, region=region)

@st.cache_resource(show_spinner = False)
def get_index()->VectorStoreIndex:
   
   # initialize connection to pinecone (get API key at app.pinecone.io)
   api_key = os.environ.get('PINECONE_API_KEY') or 'PINECONE_API_KEY'
# configure client
   pc = Pinecone(api_key=api_key)

# connect to index
   
   pinecone_index= pc.Index(index_name)
   vector_store=PineconeVectorStore(pinecone_index= pinecone_index)
   return VectorStoreIndex.from_vector_store(vector_store=vector_store)



if __name__ == "__main__":
   index = get_index()
   if "chat_engine" not in st.session_state:
     #chat_engine = index.as_chat_engine(chat_mode = "context",verbose = True)
       chat_engine = index.as_chat_engine(chat_mode="condense_question", verbose=True)



       st.set_page_config(page_title="Chat with Qiskit Docs, powered by QuantumBot",
                   page_icon = "",
                   layout = "centered",
                   initial_sidebar_state="auto",
                   menu_items = None,
                   )

       st.title("Chat with Qiskit documentation helper") 


   if "messages" not in st.session_state:
       st.session_state.messages=[
        {
         
         "role" : "assistant",
         "content" : "Ask me a question about Qiskit open source framework for quantum computing?",
        }
          ]

   if prompt:= st.chat_input("Your Question"):
       st.session_state.messages.append({

        "role" : "User",
        "content": prompt
    })


   for message in st.session_state.messages:
        with st.chat_message(message["role"]):
             st.write(message["content"])


   if st.session_state.messages[-1]["role"] != "assistant":
        with st.chat_message("assistant"):
             with st.spinner("Thinking...."):
                  response = chat_engine.chat(prompt)
                  st.write(response.response)
                  message = {"role": "assistant", "content": response.response}
                  st.session_state.messages.append(message) # Add response to message history

