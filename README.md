# Intelligent Document Ingestion Pipeline for RAG Systems

This project implements a controlled ingestion pipeline for a Retrieval-Augmented Generation (RAG) system. The focus is not on prompt engineering, but on vector lifecycle management, ensuring:

- Deterministic document versioning
- Hash-based change detection
- Safe reindexing
- Metadata-governed deletion
- Cost-efficient embedding usage
  
The goal is to simulate a production-ready ingestion layer.

# How to use:

1. After configured YAML API KEYS, you should run the file Ingest.py as a python run to ingest all data in pinecone vectors;
2. Run streamlit run app.py to open Streamlit website and iteract using Semanthic Searchs about publics Brazilian legal documents. 

<img width="1310" height="509" alt="image" src="https://github.com/user-attachments/assets/0097f643-5acf-403d-9166-91ac6bcaf209" />



What Is Implemented

✔ JSON Loader -> Structured legal documents are loaded from a JSON source.

✔ Text Consolidation -> Each document is transformed into a unified structured text block.

✔ Intelligent Hashing -> A deterministic doc_hash is generated from document content.

If:

Hash exists → skip ingestion
Hash changed → delete old vectors and reindex

✔ Chunking Strategy
RecursiveCharacterTextSplitter
chunk_size: 1000
chunk_overlap: 200

✔ Deterministic Vector IDs
Vector ID pattern: {doc_hash}_{chunk_index}

✔ Metadata Governance
Each chunk stores:

- processo
- relator
- data_publicacao
- classe_processual
- doc_hash
- chunk_id

Allows:

- Targeted deletion
- Scoped queries
- Controlled lifecycle
- Architecture Focus

This project emphasizes: Data Engineering principles applied to AI, Idempotent ingestion, Reprocessing safety, Vector consistency, Operational control

Tech Stack

- Python
- OpenAI Embeddings
- Pinecone
- LangChain
- YAML-based configuration
- Streamlit

What Is NOT Implemented **YET**

- Retrieval layer
- LLM answer generation
- API interface
- Hybrid search
- Monitoring
- CI/CD
- Cloud deployment

Why This Matters: Most RAG tutorials ignore ingestion control. In real production systems, Reindexing blindly increases cost, Duplicate vectors degrade retrieval, Lack of versioning creates data drift and Deletion without filters wipes indexes.
This project addresses those risks directly.Juridico-RAG


project/
│
├── config/
│   └── settings.py
│
├── data/
│   ├── docs.json
|
|── services/
│   ├── embeddings.py
│   └── vector_store.py
│
├── utils/
│   └── hashing.py
│
└── app.py
└── ingest.py
└── config.yaml
└── requirements.txt
