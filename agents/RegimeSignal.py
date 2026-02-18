from dataclasses import dataclass
from typing import Dict, Optional

@dataclass
class RegimeSignal:
    regime: str                 # risk_on | risk_off | neutral
    confidence: float
    sector_bias: Dict[str, float]
    numeric_rationale: str
    structural_rationale: str