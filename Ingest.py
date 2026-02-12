import json
from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from utils.hashing import generate_hash
from services.embeddings import get_embeddings
from services.vectorstore import get_vectorstore
from config.settings import AppConfig

index_name = 'processos-juridicos'

config = AppConfig()
pc = config.pinecone_client
index = pc.Index(index_name)

def load_documents():
    # carregar json
    with open("data/docs.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    documents = []

    for item in data:
        # montar texto consolidado
        content = f"""
        Processo: {item.get('processo')}
        Classe Processual: {item.get('classe_processual')}
        Relator: {item.get('relator')}
        Data Publicação: {item.get('data_publicacao')}    
        Tese: {item.get('tese')}
        Ementa: {item.get('ementa')}
        """

        doc_hash = generate_hash(content)

        # criar documento no padrão LangChain
        documents.append(
            Document(
                page_content=content.strip(),
                metadata={
                    "processo": item.get("processo"),
                    "relator": item.get("relator"),
                    "data_publicacao": item.get("data_publicacao"),
                    "classe_processual": item.get("classe_processual"),
                    "doc_hash": doc_hash
                }
            )
        )   

    return documents

def run_ingestion():
    documents = load_documents()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,  
        chunk_overlap=200,
        length_function=len
    )

    embeddings = get_embeddings()
    vectorstore = get_vectorstore(index_name, embeddings)

    for doc in documents:
        processo = doc.metadata["processo"]
        doc_hash = doc.metadata["doc_hash"]

        # Verifica se já existe vetor com esse doc_hash
        response = index.fetch(ids=[f"{doc_hash}_0"])
    
        if response.vectors:
            print(f"{processo} sem alteração. Pulando.")
            continue

        # Se mudou ou não existe → deletar versão antiga pelo processo
        index.delete(filter={"processo": {"$eq": processo}})
        print(f"{processo} alterado ou novo. Reindexando.")

        chunked_docs = splitter.split_documents([doc])

        # Gerar IDs únicos por chunk
        ids = []
        for i, chunk in enumerate(chunked_docs):
            chunk_id = f"{doc_hash}_{i}"
            chunk .metadata["chunk_id"] = chunk_id
            ids.append(chunk_id)

        vectorstore.add_documents(
            chunked_docs,
            ids= ids
    )

    print("Ingestão concluída.")


if __name__ == "__main__":
    run_ingestion()