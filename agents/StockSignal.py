from dataclasses import dataclass
from typing import Dict, Optional

@dataclass
class StockSignal:
    symbol: str
    agent: str
    score: float        # [-1, +1]
    confidence: float   # [0, 1]
    horizon: str        # short | medium | long
    numeric_rationale: str
    structural_rationale: str
    evidence: Optional[Dict] = None