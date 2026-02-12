from langchain_community.vectorstores import Pinecone as PineconeVectorStore
from pinecone import Pinecone
import os

def get_vectorstore(index_name, embeddings):
    pc = Pinecone(api_key=os.environ["PINECONE_API_KEY"])

    return PineconeVectorStore.from_existing_index(
        index_name=index_name,
        embedding=embeddings
    )