from utilites.fundamental_document.get_company_earning_analysis import get_company_earning_analysis

class FundamentalDocumentsAgent:

    def run(self, symbol: str):
       return get_company_earning_analysis(symbol)