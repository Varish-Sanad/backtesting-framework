"""
Breakout / momentum — go long when price sets a new N-day high, betting
that recent strength keeps carrying instead of snapping back. Opposite bet
from the mean-reversion strategies below.
"""

import pandas as pd

from ..signals import Signal, SignalGenerator


class Breakout(SignalGenerator):
    def __init__(self, window: int = 20):
        self.window = window

    def generate(self, history: pd.DataFrame) -> Signal:
        if len(history) < self.window:
            return Signal.FLAT
        recent = history["close"].tail(self.window)
        return Signal.LONG if recent.iloc[-1] >= recent.max() else Signal.FLAT
