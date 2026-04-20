from torch.cuda import device
import pandas as pd
import torch
from utilities.allocation.unified_sector_allocator_agent import UnifiedSectorAllocatorAgent
from utilities.allocation.read_top_gainers import read_top_gainers
from utilities.model_utilities.get_all_models import get_all_models
from utilities.datafeeds.get_nifty_50 import get_nifty_50
from utilities.datafeeds.prepare_feed_data import prepare_feed_data
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

  propositions["allocations"] = allocation
  
  top_gainers_in_sector = {}
  for sector in allocation.keys():
    gainers_df = read_top_gainers(sector)
    top_gainers_in_sector[sector] = gainers_df
    
  propositions["top_gainers_in_sector"] = top_gainers_in_sector
    

  return propositions
