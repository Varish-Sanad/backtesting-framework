"""
Buy and hold — the benchmark every other strategy actually has to beat.
No decisions, always long. If something fancier can't top this on a
risk-adjusted basis, the extra complexity isn't earning its keep.
"""

import pandas as pd

from ..signals import Signal, SignalGenerator


class BuyAndHold(SignalGenerator):
    def generate(self, history: pd.DataFrame) -> Signal:
        return Signal.LONG
