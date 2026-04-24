import os
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from apis.logging_config import setup_logging, log_service_io

# Get project root directory and create proper path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PERSIST_DIR_FUNDAMENTAL = os.path.join(PROJECT_ROOT, "fundamentals.db")

logger = setup_logging("service-vectordb")

class VectorDB:
    _instance = None

    @classmethod
    def get(cls):
        """Singleton access to Chroma DB"""
        if cls._instance is None:
            log_service_io(logger, "vectordb.get.cache_miss", inputs={"persist_dir": PERSIST_DIR_FUNDAMENTAL})
            cls._instance = cls._initialize()
        else:
            log_service_io(logger, "vectordb.get.cache_hit")
        return cls._instance

    @classmethod
    def _initialize(cls):
        embeddings = OpenAIEmbeddings(model="text-embedding-3-large")

        # If DB already exists → load
        if os.path.exists(PERSIST_DIR_FUNDAMENTAL) and os.listdir(PERSIST_DIR_FUNDAMENTAL):
            log_service_io(
                logger,
                "vectordb.initialize.load_existing",
                inputs={"persist_dir": PERSIST_DIR_FUNDAMENTAL},
            )
            return Chroma(
                persist_directory=PERSIST_DIR_FUNDAMENTAL,
                embedding_function=embeddings
            )

        # Otherwise → create empty DB
        log_service_io(
            logger,
            "vectordb.initialize.create_new",
            inputs={"persist_dir": PERSIST_DIR_FUNDAMENTAL},
        )
        return Chroma(
            persist_directory=PERSIST_DIR_FUNDAMENTAL,
            embedding_function=embeddings
        )

    @classmethod
    def initialize_vector_db(cls):
        return cls.get()