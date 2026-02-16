import os
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma

PERSIST_DIR_FUNDAMENTAL = "/fundamentals.db"   # choose your path once

class VectorDB:
    _instance = None

    @classmethod
    def get(cls):
        """Singleton access to Chroma DB"""
        if cls._instance is None:
            cls._instance = cls._initialize()
        return cls._instance

    @classmethod
    def _initialize(cls):
        embeddings = OpenAIEmbeddings(model="text-embedding-3-large")

        # If DB already exists → load
        if os.path.exists(PERSIST_DIR_FUNDAMENTAL) and os.listdir(PERSIST_DIR_FUNDAMENTAL):
            print("Loading existing Chroma DB...")
            return Chroma(
                persist_directory=PERSIST_DIR_FUNDAMENTAL,
                embedding_function=embeddings
            )

        # Otherwise → create empty DB
        print("Creating new Chroma DB...")
        return Chroma(
            persist_directory=PERSIST_DIR_FUNDAMENTAL,
            embedding_function=embeddings
        )

    def initialize_vector_db(self):
        return self.get()