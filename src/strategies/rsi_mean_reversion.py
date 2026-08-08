"""
RSI mean reversion — RSI scores recent gains vs. losses on a 0-100 scale.
Below the oversold threshold means the price has fallen unusually hard
relative to its own recent behavior, and the bet is it bounces back.
"""

import pandas as pd

from ..signals import Signal, SignalGenerator


class RSIMeanReversion(SignalGenerator):
    def __init__(self, window: int = 14, oversold: float = 30.0):
        self.window = window
        self.oversold = oversold

    def generate(self, history: pd.DataFrame) -> Signal:
        if len(history) < self.window + 1:
            return Signal.FLAT

        changes = history["close"].tail(self.window + 1).diff().dropna()
        avg_gain = changes.clip(lower=0).mean()
        avg_loss = -changes.clip(upper=0).mean()

        if avg_loss == 0:
            return Signal.FLAT

        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))
        return Signal.LONG if rsi < self.oversold else Signal.FLAT
