from torch.cuda import device
import pandas as pd
import torch
from utilities.allocation.unified_sector_allocator_agent import UnifiedSectorAllocatorAgent
from utilities.model_utilities.get_all_models import get_all_models
from utilities.datafeeds.get_nifty_50 import get_nifty_50
from utilities.datafeeds.prepare_feed_data import prepare_feed_data
from utilities.allocation.top_gainers_in_sector import top_gainers_in_sector
from utilities.allocation.sector_explaination_dashboard import sector_explanation_dashboard


def get_propositions(sector_weights=None, fetch_nse_data=True):
  """
  Get allocation propositions with sector recommendations and stock picks.
  
  Args:
      sector_weights: Optional dict of current sector weights for diversification
      fetch_nse_data: Whether to fetch live NSE data for top gainers (default: True)
                      Set to False to skip NSE fetching if connection is unstable
  
  Returns:
      dict with 'allocations', 'top_gainers_in_sector', and 'stock_to_invest'
  """
  # Handle empty dict or None
  if sector_weights and len(sector_weights) == 0:
     sector_weights = None
  propositions = {}
  agent = UnifiedSectorAllocatorAgent()
  models = get_all_models()
  nifty_df, nifty_X, nifty_model = get_nifty_50(models)
  FEATURE_COLS = [
      "RSI", "MACD", "Upper", "Mid", "Lower",
      "EMA_50", "EMA_200", "ATR", "ADX"
  ]
  device = "cuda" if torch.cuda.is_available() else "cpu"
  feed_data = prepare_feed_data()

  allocation, explanations = agent.decide(
    nifty_df=nifty_df,
    nifty_X=nifty_X,
    nifty_model=nifty_model,
    sector_inputs=feed_data,
    feature_names=FEATURE_COLS,
    weights_existing=sector_weights,
    device=device,
    explain=True
  )

  sector_explanation_dashboard(
      allocation,
      explanations
  )
  allocation_sectors = allocation.keys()

  propositions["allocations"] = allocation

  stock_based = []
  top_gainers = None

  """
  
  # Only fetch NSE data if requested
  if fetch_nse_data:
    for sector in allocation_sectors:
        if sector in ["GOLDBEES", "SILVERBEES"]:
            stock_based.append(sector)
        else:
          if sector in ["ENERGY"]:
            sector = "ENERGY"
          top_gainers_sector = top_gainers_in_sector(f"NIFTY%20{sector}")
          
          # Only add if we got results
          if not top_gainers_sector.empty:
            if top_gainers is None:
              top_gainers = top_gainers_sector
            else:
              top_gainers = pd.concat([top_gainers, top_gainers_sector])
  else:
    # NSE fetching disabled - only include precious metals
    stock_based = [s for s in allocation_sectors if s in ["GOLDBEES", "SILVERBEES"]]
  
  # Handle case where top_gainers might be None or empty
  if top_gainers is not None and not top_gainers.empty:
    top_gainers = top_gainers.sort_values("pChange", ascending=False)
    propositions["top_gainers_in_sector"] = top_gainers
    stock_to_invest = stock_based + top_gainers["symbol"].tolist()[:5]
    propositions["nse_data_available"] = True
  else:
    # If we couldn't fetch any top gainers, just return the stock-based allocations
    propositions["top_gainers_in_sector"] = pd.DataFrame(columns=["symbol", "lastPrice", "pChange"])
    stock_to_invest = stock_based
    propositions["nse_data_available"] = False
  
  propositions["stock_to_invest"] = stock_to_invest
  """
  return propositions
