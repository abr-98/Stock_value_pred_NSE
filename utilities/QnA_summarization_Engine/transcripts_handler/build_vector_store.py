import os
import sys
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings

def _load_api_key_if_needed():
    """Load OpenAI API key from file if not already set."""
    if os.environ.get("OPENAI_API_KEY"):
        return
    
    try:
        # Try to find OpenAI-Key.txt in project root
        current_dir = os.path.dirname(os.path.abspath(__file__))
        # Navigate up to find the project root (go up from utilities/QnA.../transcripts_handler)
        project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(current_dir))))
        key_file = os.path.join(project_root, "OpenAI-Key.txt")
        
        if os.path.exists(key_file):
            with open(key_file) as f:
                api_key = f.readline().strip()
                if api_key:
                    os.environ["OPENAI_API_KEY"] = api_key
                    print(f"Loaded OpenAI API key from {key_file}", file=sys.stderr)
    except Exception as e:
        print(f"Warning: Could not load API key from file: {e}", file=sys.stderr)

def build_vector_store(documents=None, persist_dir="./transcripts_db"):
    # Ensure API key is loaded
    _load_api_key_if_needed()
    
    os.makedirs(persist_dir, exist_ok=True)

    # Get API key from environment
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY not found. Please set it in OpenAI-Key.txt or as environment variable.")
    
    embeddings = OpenAIEmbeddings(model="text-embedding-3-large", api_key=api_key)

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