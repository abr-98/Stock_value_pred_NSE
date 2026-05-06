import requests
import json
import sys
from utilities.fundamental_document.parse_nse_annual_reports import parse_nse_annual_reports

def get_annual_reports_feed(symbol):
    """
    Fetch annual reports for a company from NSE API.
    
    Args:
        symbol: Company symbol (e.g., 'TCS', 'INFY')
        
    Returns:
        file_url: URL of the most recent annual report
        
    Raises:
        ValueError: If no reports found or API call fails
    """
    session = requests.Session()
    session.headers.update({
        "User-Agent": "Mozilla/5.0",
        "Accept": "application/json",
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": "https://www.nseindia.com/"
    })

    url = "https://www.nseindia.com/api/annual-reports"
    params = {
        "index": "cm",
        "symbol": symbol
    }

    try:
        print(f"Fetching annual reports for {symbol} from NSE API...", file=sys.stderr)
        response = session.get(url, params=params, timeout=10)
        response.raise_for_status()

        data = json.loads(response.content.decode("UTF-8"))
        reports = parse_nse_annual_reports(data)
        
        if not reports:
            error_msg = f"No annual reports found for symbol '{symbol}' from NSE API. Response data keys: {data.keys() if isinstance(data, dict) else 'unknown'}"
            print(error_msg, file=sys.stderr)
            raise ValueError(error_msg)
        
        # Get the most recent report (first one)
        annual_report = reports[0]["file_url"]
        
        if not annual_report:
            error_msg = f"Annual report file URL is empty for symbol '{symbol}'. First report: {reports[0]}"
            print(error_msg, file=sys.stderr)
            raise ValueError(error_msg)
        
        print(f"Successfully fetched annual report for {symbol}: {annual_report}", file=sys.stderr)
        return annual_report
        
    except requests.exceptions.Timeout:
        error_msg = f"Timeout fetching annual reports for {symbol}"
        print(error_msg, file=sys.stderr)
        raise ValueError(error_msg)
    except requests.exceptions.RequestException as e:
        error_msg = f"Failed to fetch annual reports for {symbol}: {str(e)}"
        print(error_msg, file=sys.stderr)
        raise ValueError(error_msg)
    except json.JSONDecodeError as e:
        error_msg = f"Invalid JSON response from NSE API for {symbol}: {str(e)}"
        print(error_msg, file=sys.stderr)
        raise ValueError(error_msg)
    except (KeyError, IndexError, TypeError) as e:
        error_msg = f"Unexpected response format from NSE API for {symbol}: {str(e)}"
        print(error_msg, file=sys.stderr)
        raise ValueError(error_msg)