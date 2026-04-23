from backend_handlers.database_utilities.read_database import read_table_to_dataframe
from datetime import datetime

def read_top_gainers(sector):
    date_today = datetime.datetime.now().strftime("%Y-%m-%d")
    condition = f"Sector = '{sector.replace(' ', '%20')}' AND date = '{date_today}'"
    
    gainers_df = read_table_to_dataframe("top_gainers_2", condition)
    return gainers_df