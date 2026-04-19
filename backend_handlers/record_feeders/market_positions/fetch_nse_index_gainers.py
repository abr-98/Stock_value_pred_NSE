import requests
import time
import warnings
import urllib3

# Suppress SSL warnings globally for NSE requests
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
warnings.filterwarnings('ignore', message='Unverified HTTPS request')

def fetch_nse_index(index_code: str, max_retries=2, timeout=15):
    """
    Fetch NSE index data with retry logic for handling connection issues.
    Returns None if fetching fails (graceful degradation).
    
    Args:
        index_code: NSE index code (e.g., "NIFTY%20BANK", "NIFTY%20IT")
        max_retries: Maximum number of retry attempts (default: 2)
        timeout: Request timeout in seconds (default: 15)
    
    Returns:
        List of stocks in the index with their data, or None if fails
    """
    url = f"https://www.nseindia.com/api/equity-stockIndices?index={index_code}"

    headers = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "application/json",
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": "https://www.nseindia.com/",
    }

    session = requests.Session()
    session.headers.update(headers)

    for attempt in range(2):
        # Visit homepage first to establish session and get cookies
        home_response = session.get(
            "https://www.nseindia.com", 
        )
        print(home_response.status_code)
        
        # Longer delay to ensure cookies are set
        time.sleep(1.5)

        # Fetch the actual index data
        response = session.get(url)
        response.raise_for_status()

        data = response.json()
        if "data" in data:
            return data["data"]
        else:
            print(f"Unexpected response format for {index_code}: {data}")
            return None
