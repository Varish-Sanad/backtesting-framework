"""Quick end-to-end smoke test — fake price data through the MA-cross strategy."""

import numpy as np
import pandas as pd

from src.engine import BacktestEngine
from src.metrics import summarize
from src.strategies.moving_average_cross import MovingAverageCross


def make_synthetic_ohlcv(n: int = 300, seed: int = 7) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    returns = rng.normal(loc=0.0003, scale=0.01, size=n)
    close = 100 * np.cumprod(1 + returns)
    open_ = np.roll(close, 1)
    open_[0] = close[0]
    return pd.DataFrame({
        "date": pd.date_range("2023-01-01", periods=n, freq="B"),
        "open": open_,
        "close": close,
    })


if __name__ == "__main__":
    data = make_synthetic_ohlcv()
    engine = BacktestEngine(data, MovingAverageCross(fast=10, slow=30))
    result = engine.run()

    stats = summarize(result["equity"])
    print(result[["date", "close", "equity"]].tail())
    print()
    for key, value in stats.items():
        print(f"{key}: {value:.4f}")
