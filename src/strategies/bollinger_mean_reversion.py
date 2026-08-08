"""
Bollinger band mean reversion — same bet as RSI (oversold snaps back), just
measured with volatility instead of a gain/loss ratio. Long when price
falls below the lower band: mean minus a couple standard deviations.
"""

import pandas as pd

from ..signals import Signal, SignalGenerator


class BollingerMeanReversion(SignalGenerator):
    def __init__(self, window: int = 20, num_std: float = 2.0):
        self.window = window
        self.num_std = num_std

    def generate(self, history: pd.DataFrame) -> Signal:
        if len(history) < self.window:
            return Signal.FLAT

        recent = history["close"].tail(self.window)
        lower_band = recent.mean() - self.num_std * recent.std()
        return Signal.LONG if recent.iloc[-1] < lower_band else Signal.FLAT
