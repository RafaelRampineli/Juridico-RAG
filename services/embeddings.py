from langchain_openai import OpenAIEmbeddings

def get_embeddings():
    return OpenAIEmbeddings(model='text-embedding-ada-002')