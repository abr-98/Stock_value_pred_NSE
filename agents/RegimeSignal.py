from dataclasses import dataclass
from typing import Dict, Optional

@dataclass
class RegimeSignal:
    regime: str                 # risk_on | risk_off | neutral
    confidence: float
    sector_bias: Dict[str, float]
    rationale: str