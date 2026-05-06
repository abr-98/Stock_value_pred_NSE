import os
import sys
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from apis.logging_config import setup_logging, log_service_io

# Get project root directory and create proper path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PERSIST_DIR_FUNDAMENTAL = os.path.join(PROJECT_ROOT, "fundamentals.db")

logger = setup_logging("service-vectordb")

def _ensure_api_key():
    """Ensure OpenAI API key is loaded."""
    if os.environ.get("OPENAI_API_KEY"):
        return
    
    try:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(os.path.dirname(os.path.dirname(current_dir)))
        key_file = os.path.join(project_root, "OpenAI-Key.txt")
        if os.path.exists(key_file):
            with open(key_file) as f:
                api_key_value = f.readline().strip()
                if api_key_value:
                    os.environ["OPENAI_API_KEY"] = api_key_value
                    print(f"Loaded OpenAI API key from {key_file}", file=sys.stderr)
    except Exception as e:
        print(f"Warning: Could not load API key: {e}", file=sys.stderr)

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
        _ensure_api_key()
        api_key = os.environ.get("OPENAI_API_KEY")
        embeddings = OpenAIEmbeddings(model="text-embedding-3-large", api_key=api_key)

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