from torch.cuda import device
import pandas as pd
import torch
from utilites.allocation.unified_sector_allocator_agent import UnifiedSectorAllocatorAgent
from utilites.model_utilities.get_all_models import get_all_models
from utilites.datafeeds.get_nifty_50 import get_nifty_50
from utilites.datafeeds.prepare_feed_data import prepare_feed_data
from utilites.allocation.top_gainers_in_sector import top_gainers_in_sector
from utilites.allocation.sector_explaination_dashboard import sector_explanation_dashboard


def get_propositions(present_weights=None):
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
    weights_existing=present_weights,
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
  for sector in allocation_sectors:
      if sector in ["GOLDBEES", "SILVERBEES"]:
          stock_based.append(sector)
      else:
        if sector in ["ENERGY"]:
          sector = "ENERGY"
        top_gainers_sector = top_gainers_in_sector(f"NIFTY%20{sector}")
        top_gainers_sector.head()
        if top_gainers is None:
          top_gainers = top_gainers_sector
        else:
          top_gainers = pd.concat([top_gainers, top_gainers_sector])
  top_gainers = top_gainers.sort_values("pChange", ascending=False)
  propositions["top_gainers_in_sector"] = top_gainers
  stock_to_invest = stock_based + top_gainers["symbol"].tolist()[:5]
  propositions["stock_to_invest"] = stock_to_invest
  return propositions
