import os
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings

def build_vector_store(documents, persist_dir="./fundamental_db"):
    texts = [d["text"] for d in documents]
    metadatas = [d["metadata"] for d in documents]

    embeddings = OpenAIEmbeddings(model="text-embedding-3-large")

    if os.path.exists(persist_dir):
        vectordb = Chroma(
            persist_directory=persist_dir,
            embedding_function=embeddings
        )
        vectordb.add_texts(texts=texts, metadatas=metadatas)
    else:
        vectordb = Chroma.from_texts(
            texts=texts,
            metadatas=metadatas,
            embedding=embeddings,
            persist_directory=persist_dir
        )

    return vectordb