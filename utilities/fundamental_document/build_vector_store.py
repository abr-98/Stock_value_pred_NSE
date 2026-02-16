from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from application.helpers.vectordb import VectorDB

def build_vector_store(documents, persist_dir="./fundamental_db"):
    texts = [d["text"] for d in documents]
    metadatas = [d["metadata"] for d in documents]

    embeddings = OpenAIEmbeddings(model="text-embedding-3-large")
    
    vectordb = VectorDB.get()

    vectordb.add_texts(
     texts=texts,
        metadatas=metadatas,
        embedding=embeddings
    )

    vectordb.persist()
    return vectordb