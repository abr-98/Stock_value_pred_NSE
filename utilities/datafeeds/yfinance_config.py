"""
YFinance SSL Configuration Module

Usage:
    from utilities.datafeeds.yfinance_config import yf
    ticker = yf.Ticker("RELIANCE.NS")
"""

import yfinance as yf
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import certifi
import os
import urllib3

# Disable SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def get_yfinance_session():
    session = requests.Session()

    retry_strategy = Retry(
        total=3,
        backoff_factor=0.3,
        status_forcelist=[429, 500, 502, 503, 504],
    )

    adapter = HTTPAdapter(max_retries=retry_strategy)

    session.mount("https://", adapter)
    session.mount("http://", adapter)

    # Disable SSL verification to avoid certificate issues
    session.verify = False

    session.headers.update({
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0 Safari/537.36"
        )
    })

    return session


_session = get_yfinance_session()

# Configure yfinance session
try:
    yf.utils.get_yf_session = lambda: _session
except AttributeError:
    pass

# Disable SSL verification for curl_cffi (used by newer yfinance versions)
os.environ["CURL_CA_BUNDLE"] = ""
os.environ["SSL_CERT_FILE"] = ""
os.environ["REQUESTS_CA_BUNDLE"] = ""

# Patch curl_cffi if yfinance is using it
try:
    from curl_cffi import requests as curl_requests
    # Monkey patch curl_cffi to disable SSL verification
    original_request = curl_requests.Session.request
    
    def patched_request(self, method, url, **kwargs):
        kwargs['verify'] = False
        return original_request(self, method, url, **kwargs)
    
    curl_requests.Session.request = patched_request
except ImportError:
    # curl_cffi not installed or not used
    pass

__all__ = ["yf"]
