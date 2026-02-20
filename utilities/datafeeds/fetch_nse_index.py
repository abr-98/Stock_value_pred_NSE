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
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "*/*",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Referer": "https://www.nseindia.com/market-data/live-equity-market",
        "Connection": "keep-alive",
        "Cache-Control": "no-cache",
        "Pragma": "no-cache"
    }
    
    session = requests.Session()
    session.headers.update(headers)

    for attempt in range(max_retries):
        try:
            # Visit homepage first to establish session and get cookies
            home_response = session.get(
                "https://www.nseindia.com", 
                timeout=timeout, 
                verify=False,
                allow_redirects=True
            )
            
            # Longer delay to ensure cookies are set
            time.sleep(1.5)

            # Fetch the actual index data
            response = session.get(url, timeout=timeout, verify=False, allow_redirects=True)
            response.raise_for_status()

            data = response.json()
            if "data" in data and data["data"]:
                return data["data"]
            else:
                # Empty data or unexpected format
                return None

        except Exception as e:
            if attempt < max_retries - 1:
                wait_time = 3 + (attempt * 2)  # 3s, 5s
                time.sleep(wait_time)
                continue
            else:
                # All retries exhausted - return None for graceful degradation
                return None

    return None
