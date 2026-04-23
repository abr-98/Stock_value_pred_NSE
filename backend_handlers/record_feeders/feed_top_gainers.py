from .market_positions.market_postion_executor import get_market_positions
from ..database_utilities.write_database import insert_dataframe


def feed_gainers():
    
    # 2. Fetch market positions
    gainers_df = get_market_positions()
    
    gainers_df.rename(columns={"index": "sector", "symbol": "company", "pChange": "pCHANGE", "date": "date"}, inplace=True)
    
    print(gainers_df.head())

    # 3. Insert into database
    insert_dataframe(gainers_df, "top_gainers_2")

    