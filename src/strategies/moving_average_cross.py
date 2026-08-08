"""
Moving average crossover — the classic trend-following signal. When the
short lookback average is running above the long one, recent price action
is outpacing the longer trend, so we ride it. No crossover, no position.
"""

import pandas as pd

from ..signals import Signal, SignalGenerator


class MovingAverageCross(SignalGenerator):
    def __init__(self, fast: int = 10, slow: int = 30):
        self.fast = fast
        self.slow = slow

    def generate(self, history: pd.DataFrame) -> Signal:
        if len(history) < self.slow:
            return Signal.FLAT
        fast_ma = history["close"].tail(self.fast).mean()
        slow_ma = history["close"].tail(self.slow).mean()
        return Signal.LONG if fast_ma > slow_ma else Signal.FLAT
