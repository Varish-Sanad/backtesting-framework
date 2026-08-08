"""The day-by-day loop that runs a strategy against price history."""

import pandas as pd

from .portfolio import Portfolio
from .signals import SignalGenerator


class BacktestEngine:
    def __init__(
        self,
        data: pd.DataFrame,
        signal_generator: SignalGenerator,
        initial_cash: float = 100_000.0,
    ):
        required_cols = {"open", "close"}
        if not required_cols.issubset(data.columns):
            raise ValueError(f"data must contain columns {required_cols}")

        self.data = data.reset_index(drop=True)
        self.signal_generator = signal_generator
        self.portfolio = Portfolio(initial_cash=initial_cash)

    def run(self) -> pd.DataFrame:
        n = len(self.data)
        for t in range(n):
            # Only bars up to and including t — the signal generator
            # structurally cannot see the future because it's never given it.
            history = self.data.iloc[: t + 1]
            signal = self.signal_generator.generate(history)

            # Signal is decided using close[t]; fill happens at open[t+1] —
            # you can't trade at the exact price you just used to decide.
            if t + 1 < n:
                fill_price = self.data.loc[t + 1, "open"]
                self.portfolio.rebalance_to(signal, fill_price)

            self.portfolio.mark_to_market(self.data.loc[t, "close"])

        result = self.data.copy()
        result["equity"] = self.portfolio.equity_curve
        return result
