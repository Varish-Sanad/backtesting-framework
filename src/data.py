"""CSV loader for OHLCV price history."""

import pandas as pd


def load_ohlcv(path: str) -> pd.DataFrame:
    """Loads a CSV with a `date` column plus OHLCV columns, sorted ascending.

    Known limitation: does not address survivorship bias — if `path` only
    contains tickers that exist today, delisted/bankrupt names are silently
    absent and returns will be biased upward. Fixing that requires a
    point-in-time universe from the data vendor, not a code change here.
    """
    df = pd.read_csv(path, parse_dates=["date"])
    df.columns = [c.lower() for c in df.columns]
    df = df.sort_values("date").reset_index(drop=True)
    return df
