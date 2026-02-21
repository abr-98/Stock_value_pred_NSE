from utilities.fundamental_document.download_pdf import download_pdf
from utilities.fundamental_document.get_annual_reports_feed import get_annual_reports_feed


class DataFetchersReport:

    @staticmethod
    def fetch_annual_report(symbol):
        try:
            annual_report_url = get_annual_reports_feed(symbol)
            path = download_pdf(annual_report_url, f"{symbol}.pdf")
            if not path:
                raise ValueError(f"Failed to download annual report for {symbol}")
            return path
        except Exception as e:
            raise ValueError(f"Error fetching annual report for {symbol}: {str(e)}")
