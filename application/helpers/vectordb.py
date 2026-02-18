import os
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma

# Get project root directory and create proper path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PERSIST_DIR_FUNDAMENTAL = os.path.join(PROJECT_ROOT, "fundamentals.db")

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

    @classmethod
    def initialize_vector_db(cls):
        return cls.get()