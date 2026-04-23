from .get_nse_filings import get_nse_filings
from .extract_documents import extract_documents
from .get_pdf import download_pdf
import datetime
import pandas as pd
import re
from urllib.parse import urlparse, unquote

def get_safe_filename(url):
    # Extract path
    path = urlparse(url).path
    
    # Get last part
    filename = path.split("/")[-1]
    
    # Decode URL encoding (%20 → space, etc.)
    filename = unquote(filename)
    
    # Remove unsafe characters
    filename = re.sub(r'[<>:"/\\|?*]', '_', filename)
    
    return filename

def process_transcripts(symbol):
    filings = get_nse_filings(symbol)
    
    docs = extract_documents(filings)
    
    filtered_data = {
    key: [item for item in value if item.get("url") and item.get("url") != "-"]
    for key, value in docs.items()
    }
    data_cons = [filtered_data["transcript"][-1]] + filtered_data["results"][:3]
    
    path = "../../../transcripts/"
    date = datetime.datetime.now().strftime("%Y-%m-%d")
    version =1
    for item in data_cons:
        url = item["url"]
        title = item["title"]
        filename = get_safe_filename(f"{symbol}_{title}_{date}_{version}.pdf")
        version+=1
        download_pdf(url, save_dir=path, filename=filename)
    
        item["filepath"] = f"{path}/{filename}"
        
    df = pd.DataFrame(data_cons)
    df["symbol"] = symbol
    df["date"] = date
    
    return df