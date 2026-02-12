import streamlit as st
from langchain_openai import ChatOpenAI
from langchain.chains import RetrievalQA
from services.embeddings import get_embeddings
from services.vectorstore import get_vectorstore
from config.settings import AppConfig

config = AppConfig()
pc = config.pinecone_client

index_name = 'processos-juridicos'

@st.cache_resource
def load_chain():
    embeddings = get_embeddings()
    vectorstore = get_vectorstore(index_name, embeddings)
    retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
    llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)
    return RetrievalQA.from_chain_type(llm=llm, retriever=retriever)

chain = load_chain()

st.title("Buscador Semântico Jurídico")

query = st.text_input("O que deseja pesquisar?")

if st.button("Pesquisar") and query:
    result = chain.invoke(query)
    st.write(result["result"])