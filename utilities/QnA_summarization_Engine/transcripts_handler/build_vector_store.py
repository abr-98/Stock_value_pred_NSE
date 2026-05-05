import os
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings

def build_vector_store(documents=None, persist_dir="./transcripts_db"):
    os.makedirs(persist_dir, exist_ok=True)

    embeddings = OpenAIEmbeddings(model="text-embedding-3-large")

    if documents is None:
        return Chroma(
            persist_directory=persist_dir,
            embedding_function=embeddings,
        )

    texts = [d["text"] for d in documents]
    metadatas = [d["metadata"] for d in documents]

    vectordb = Chroma.from_texts(
        texts=texts,
        metadatas=metadatas,
        embedding=embeddings,
        persist_directory=persist_dir,
    )

    return vectordb