import requests

def fetch_nse_index(index_code: str):
    url = f"https://www.nseindia.com/api/equity-stockIndices?index={index_code}"

    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept": "application/json",
        "Referer": "https://www.nseindia.com/"
    }

    session = requests.Session()
    session.headers.update(headers)

    # Mandatory for NSE
    session.get("https://www.nseindia.com")

    response = session.get(url)
    response.raise_for_status()

    return response.json()["data"]
