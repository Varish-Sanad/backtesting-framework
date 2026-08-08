"""PnL, Sharpe ratio, and max drawdown, computed off an equity curve."""

import numpy as np
import pandas as pd


def total_pnl(equity_curve: pd.Series) -> float:
    return float(equity_curve.iloc[-1] - equity_curve.iloc[0])


def sharpe_ratio(
    equity_curve: pd.Series,
    periods_per_year: int = 252,
    risk_free_rate: float = 0.0,
) -> float:
    returns = equity_curve.pct_change().dropna()
    excess = returns - risk_free_rate / periods_per_year
    if excess.std() == 0:
        return 0.0
    return float(excess.mean() / excess.std() * np.sqrt(periods_per_year))


def max_drawdown(equity_curve: pd.Series) -> float:
    running_max = equity_curve.cummax()
    drawdown = equity_curve / running_max - 1.0
    return float(drawdown.min())


def summarize(equity_curve: pd.Series, periods_per_year: int = 252) -> dict:
    return {
        "total_pnl": total_pnl(equity_curve),
        "total_return_pct": float(equity_curve.iloc[-1] / equity_curve.iloc[0] - 1.0) * 100,
        "sharpe_ratio": sharpe_ratio(equity_curve, periods_per_year),
        "max_drawdown_pct": max_drawdown(equity_curve) * 100,
    }
