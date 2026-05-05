import os
import shutil
import sys
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings

def _ensure_api_key():
    """Ensure OpenAI API key is loaded from environment or file."""
    if os.environ.get("OPENAI_API_KEY"):
        return
    
    try:
        # Try to find OpenAI-Key.txt in project root
        current_dir = os.path.dirname(os.path.abspath(__file__))
        # Navigate up to find the project root (go up from utilities/fundamental_document)
        project_root = os.path.dirname(os.path.dirname(os.path.dirname(current_dir)))
        key_file = os.path.join(project_root, "OpenAI-Key.txt")
        
        if os.path.exists(key_file):
            with open(key_file) as f:
                api_key = f.readline().strip()
                if api_key:
                    os.environ["OPENAI_API_KEY"] = api_key
                    print(f"Loaded OpenAI API key from {key_file}", file=sys.stderr)
                    return
        
        raise ValueError(f"OpenAI-Key.txt not found at {key_file}")
    except Exception as e:
        print(f"Warning: Could not load API key from file: {e}", file=sys.stderr)
        raise ValueError("OPENAI_API_KEY not found. Please set it in OpenAI-Key.txt or as environment variable.")

def build_vector_store(documents, persist_dir="./fundamental_db", reset=False):
    _ensure_api_key()
    
    texts = [d["text"] for d in documents]
    metadatas = [d["metadata"] for d in documents]

    api_key = os.environ.get("OPENAI_API_KEY")
    embeddings = OpenAIEmbeddings(model="text-embedding-3-large", api_key=api_key)

    try:
        os.makedirs(os.path.dirname(os.path.abspath(persist_dir)), exist_ok=True)

        if reset and os.path.exists(persist_dir):
            shutil.rmtree(persist_dir)

        if os.path.exists(persist_dir):
            try:
                # Try to load existing vector store
                vectordb = Chroma(
                    persist_directory=persist_dir,
                    embedding_function=embeddings
                )
                # Verify the database is functional by querying the collection.
                vectordb.similarity_search("financial performance", k=1)
            except Exception as e:
                # If the existing database is corrupted, backup and recreate it
                print(f"Existing vector store appears corrupted: {e}", file=__import__('sys').stderr)
                backup_dir = persist_dir + ".backup"
                if os.path.exists(backup_dir):
                    shutil.rmtree(backup_dir)
                shutil.move(persist_dir, backup_dir)
                print(f"Backed up corrupted database to {backup_dir}", file=__import__('sys').stderr)
                
                # Create new vector store
                vectordb = Chroma.from_texts(
                    texts=texts,
                    metadatas=metadatas,
                    embedding=embeddings,
                    persist_directory=persist_dir
                )
        else:
            vectordb = Chroma.from_texts(
                texts=texts,
                metadatas=metadatas,
                embedding=embeddings,
                persist_directory=persist_dir
            )

        return vectordb
    except Exception as e:
        print(f"Critical error building vector store: {e}", file=__import__('sys').stderr)
        raise