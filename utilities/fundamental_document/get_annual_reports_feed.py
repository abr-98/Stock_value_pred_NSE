import requests
import json
from utilities.fundamental_document.parse_nse_annual_reports import parse_nse_annual_reports

def get_annual_reports_feed(symbol):

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

  response = session.get(url, params=params)
  response.raise_for_status()

  data = json.loads(response.content.decode("UTF-8"))
  annual_report = parse_nse_annual_reports(data)[0]["file_url"]
  return annual_report