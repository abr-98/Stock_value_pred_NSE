"""
Dependency Checker for Stock Predictor Project
Checks if all required packages are installed and reports any issues
"""
import sys
import os

# Add project root to path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

def check_package(package_name, import_name=None):
    """Check if a package is installed"""
    if import_name is None:
        import_name = package_name
    
    try:
        __import__(import_name)
        print(f"  ✓ {package_name}")
        return True
    except ImportError as e:
        print(f"  ✗ {package_name} - MISSING ({str(e)})")
        return False
    except Exception as e:
        print(f"  ? {package_name} - ERROR ({str(e)})")
        return False


def check_all_dependencies():
    """Check all required dependencies"""
    print("=" * 70)
    print("Checking Package Dependencies")
    print("=" * 70)
    
    required_packages = [
        # Core packages
        ("pandas", "pandas"),
        ("numpy", "numpy"),
        ("matplotlib", "matplotlib"),
        ("torch", "torch"),
        
        # Data fetching
        ("nsetools", "nsetools"),
        ("nselib", "nselib"),
        ("yfinance", "yfinance"),
        ("feedparser", "feedparser"),
        ("requests", "requests"),
        
        # NLP and AI
        ("vaderSentiment", "vaderSentiment"),
        ("openai", "openai"),
        ("tiktoken", "tiktoken"),
        
        # LangChain
        ("langchain", "langchain"),
        ("langchain-openai", "langchain_openai"),
        ("langchain-chroma", "langchain_chroma"),
        ("chromadb", "chromadb"),
        
        # PDF processing
        ("pymupdf", "fitz"),
        
        # ML interpretability
        ("lime", "lime"),
        
        # FastAPI and web
        ("fastapi", "fastapi"),
        ("uvicorn", "uvicorn"),
        ("pydantic", "pydantic"),
        ("pydantic-settings", "pydantic_settings"),
        ("python-multipart", "multipart"),
    ]
    
    print("\nCore Dependencies:")
    results = []
    
    for package_name, import_name in required_packages:
        results.append((package_name, check_package(package_name, import_name)))
    
    print("\n" + "=" * 70)
    print("Summary")
    print("=" * 70)
    
    total = len(results)
    installed = sum(1 for _, status in results if status)
    missing = total - installed
    
    print(f"Total packages: {total}")
    print(f"Installed: {installed}")
    print(f"Missing: {missing}")
    
    if missing > 0:
        print("\n" + "=" * 70)
        print("Missing Packages - Install with:")
        print("=" * 70)
        missing_packages = [pkg for pkg, status in results if not status]
        print("pip install " + " ".join(missing_packages))
    
    return missing == 0


def check_model_files():
    """Check if model files exist"""
    print("\n" + "=" * 70)
    print("Checking Model Files")
    print("=" * 70)
    
    models_dir = os.path.join(project_root, "models")
    
    if not os.path.exists(models_dir):
        print(f"✗ Models directory not found: {models_dir}")
        return False
    
    expected_models = [
        "best_lstm_return_model.pt",
        "best_lstm_return_model_NIFTY AUTO.pt",
        "best_lstm_return_model_NIFTY BANK.pt",
        "best_lstm_return_model_NIFTY CONSUMER DURABLES.pt",
        "best_lstm_return_model_NIFTY FINANCIAL SERVICES.pt",
        "best_lstm_return_model_NIFTY FMCG.pt",
        "best_lstm_return_model_NIFTY IT.pt",
        "best_lstm_return_model_NIFTY MEDIA.pt",
        "best_lstm_return_model_NIFTY METAL.pt",
        "best_lstm_return_model_NIFTY PHARMA.pt",
        "best_lstm_return_model_NIFTY PRIVATE BANK.pt",
        "best_lstm_return_model_NIFTY PSU BANK.pt",
        "best_lstm_return_model_NIFTY REALTY.pt",
    ]
    
    found = 0
    missing = 0
    
    for model_file in expected_models:
        model_path = os.path.join(models_dir, model_file)
        if os.path.exists(model_path):
            size_mb = os.path.getsize(model_path) / (1024 * 1024)
            print(f"  ✓ {model_file} ({size_mb:.2f} MB)")
            found += 1
        else:
            print(f"  ✗ {model_file} - NOT FOUND")
            missing += 1
    
    print(f"\nModel files found: {found}/{len(expected_models)}")
    
    if missing > 0:
        print(f"\nWarning: {missing} model file(s) missing.")
        print("Models are optional but required for allocation predictions.")
    
    return missing == 0


def check_openai_key():
    """Check if OpenAI API key file exists"""
    print("\n" + "=" * 70)
    print("Checking OpenAI API Key")
    print("=" * 70)
    
    key_file = os.path.join(project_root, "OpenAI-Key.txt")
    
    if os.path.exists(key_file):
        print(f"  ✓ OpenAI-Key.txt found")
        with open(key_file, 'r') as f:
            key = f.read().strip()
            if key:
                print(f"  ✓ Key present (starts with: {key[:10]}...)")
                return True
            else:
                print(f"  ✗ File exists but is empty")
                return False
    else:
        print(f"  ✗ OpenAI-Key.txt not found at: {key_file}")
        print(f"\n  Create this file and add your OpenAI API key to it.")
        return False


if __name__ == "__main__":
    print("\n")
    print("╔═══════════════════════════════════════════════════════════════════╗")
    print("║   Stock Predictor - Dependency & Configuration Checker           ║")
    print("╚═══════════════════════════════════════════════════════════════════╝")
    print()
    
    deps_ok = check_all_dependencies()
    key_ok = check_openai_key()
    models_ok = check_model_files()
    
    print("\n" + "=" * 70)
    print("FINAL STATUS")
    print("=" * 70)
    
    if deps_ok and key_ok:
        print("✓ System is ready to run!")
        if not models_ok:
            print("  ⚠ Some model files are missing (optional for some features)")
    else:
        print("✗ System has missing requirements:")
        if not deps_ok:
            print("  - Install missing Python packages")
        if not key_ok:
            print("  - Create OpenAI-Key.txt with your API key")
        if not models_ok:
            print("  - Model files missing (may be optional)")
    
    print("=" * 70)
