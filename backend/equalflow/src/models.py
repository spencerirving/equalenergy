#State class which represents a state as an object

from dataclasses import dataclass, field
from typing import List, Tuple

@dataclass
class State:
    name: str #state name
    produced_bcf: float #
    consumed_bcf: float
    # Derived fields in MMBtu (filled later by engine)
    produced_mmbtu: float = 0.0
    consumed_mmbtu: float = 0.0
    net_mmbtu: float = 0.0

    # Transactions
    sell_to: List[Tuple[str, float]] = field(default_factory=list)  # (buyer, mmbtu)
    buy_from: List[Tuple[str, float]] = field(default_factory=list) # (seller, mmbtu)

    # Results
    fulfilled: bool = False
    price_usd_per_mmbtu: float = 0.0

    def __post_init__(self):
        # Nothing yet; conversion done in engine to use configured constants in config.py
        pass
