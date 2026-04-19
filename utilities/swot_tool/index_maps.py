NIFTY_SECTORS = {
    "NIFTY BANK": "^NSEBANK",
    "NIFTY IT": "^CNXIT",
    "NIFTY FMCG": "^CNXFMCG",
    "NIFTY AUTO": "^CNXAUTO",
    "NIFTY PHARMA": "^CNXPHARMA",
    "NIFTY ENERGY": "^CNXENERGY",
    "NIFTY METAL": "^CNXMETAL",
    "NIFTY REALTY": "^CNXREALTY",
    "NIFTY MEDIA": "^CNXMEDIA",
    "NIFTY PSU BANK": "^CNXPSUBANK",
    "NIFTY INFRA": "^CNXINFRA"
}


nifty_sector_peers = {
    "NIFTY BANK": ["HDFCBANK.NS", "ICICIBANK.NS", "SBIN.NS", "KOTAKBANK.NS", "AXISBANK.NS"],
    
    "NIFTY IT": ["TCS.NS", "INFY.NS", "HCLTECH.NS", "WIPRO.NS", "LTIM.NS"],
    
    "NIFTY AUTO": ["MARUTI.NS", "TATAMOTORS.NS", "M&M.NS", "BAJAJ-AUTO.NS", "EICHERMOT.NS"],
    
    "NIFTY ENERGY": ["RELIANCE.NS", "ONGC.NS", "IOC.NS", "BPCL.NS", "GAIL.NS"],
    
    "NIFTY FMCG": ["HINDUNILVR.NS", "ITC.NS", "NESTLEIND.NS", "BRITANNIA.NS", "DABUR.NS"],
    
    "NIFTY PHARMA": ["SUNPHARMA.NS", "DRREDDY.NS", "CIPLA.NS", "DIVISLAB.NS", "LUPIN.NS"],
    
    "NIFTY INFRA": ["LT.NS", "SIEMENS.NS", "ABB.NS", "CUMMINSIND.NS", "BEL.NS"],
    
    "NIFTY METAL": ["TATASTEEL.NS", "JSWSTEEL.NS", "HINDALCO.NS", "VEDL.NS", "NMDC.NS"],
    
    "NIFTY MEDIA": ["ZEEL.NS", "SUNTV.NS", "PVRINOX.NS", "INOXLEISUR.NS", "NETWORK18.NS"],
    
    "NIFTY REALTY": ["DLF.NS", "GODREJPROP.NS", "OBEROIRLTY.NS", "PHOENIXLTD.NS", "BRIGADE.NS"]
}

yf_to_nifty_map = {
    "Financial Services": "NIFTY FINANCIAL SERVICES",
    "Banks": "NIFTY BANK",
    "Technology": "NIFTY IT",
    "Energy": "NIFTY ENERGY",
    "Healthcare": "NIFTY PHARMA",
    "Consumer Cyclical": "NIFTY AUTO",
    "Consumer Defensive": "NIFTY FMCG",
    "Industrials": "NIFTY INFRA",
    "Basic Materials": "NIFTY METAL",
    "Communication Services": "NIFTY MEDIA",
    "Real Estate": "NIFTY REALTY",
    "Utilities": "NIFTY ENERGY"  
}

