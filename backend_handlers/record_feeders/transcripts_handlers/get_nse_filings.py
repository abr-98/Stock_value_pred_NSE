import requests


def get_nse_filings(symbol):
    session = requests.Session()

    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept": "application/json",
        "Referer": "https://www.nseindia.com/",
        "Accept-Language": "en-US,en;q=0.9"
    }

    # ✅ Step 1: initialize session
    session.get("https://www.nseindia.com", headers=headers)

    # ✅ Step 2: correct endpoint
    url = f"https://www.nseindia.com/api/corporate-announcements?index=equities&symbol={symbol}"

    res = session.get(url, headers=headers)

    if res.status_code != 200:
        print("Failed:", res.status_code)
        print(res.text[:300])
        return []

    try:
        return res.json()
    except:
        print("Not JSON:")
        print(res.text[:300])
        return []