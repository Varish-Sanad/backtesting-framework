# Backtesting Framework

A small backtesting engine for testing trading strategies against historical price data, built to avoid the two classic ways a backtest lies to you: lookahead bias and survivorship bias.

The idea is simple — feed it OHLCV data and a strategy, it walks through the price history day by day like a time machine, tracks your (simulated) cash and positions, and spits out PnL, Sharpe ratio, and max drawdown at the end.

## Why this exists

Most toy backtesters let a strategy cheat without you noticing — either by peeking at future prices, or by only testing on stocks that survived to today. I wanted the cheating to be structurally impossible rather than something you have to remember not to do. The engine only ever hands the strategy price history up through the current bar, and fills every trade at the next bar's open, never the price the strategy just used to decide.

## What's built

- OHLCV loading from CSV (`src/data.py`)
- Strategy execution loop with cash/position/equity tracking (`src/engine.py`, `src/portfolio.py`)
- PnL, Sharpe ratio, and max drawdown (`src/metrics.py`) — win rate is still on the list
- Lookahead-bias protection baked into the loop itself, not just documented
- A pluggable `SignalGenerator` interface — adding a new strategy means writing one class, no changes to the engine
- Five example strategies: buy-and-hold, moving average crossover, breakout/momentum, RSI mean-reversion, Bollinger band mean-reversion

## What's not solved (on purpose)

Survivorship bias isn't something the engine can fix. If the price data fed into it only includes tickers still trading today, the backtest will look better than it should — that's a data-sourcing problem, not a code problem. It's flagged as a known limitation in `data.py` rather than silently ignored.

## Quick start

```python
from src.data import load_ohlcv
from src.engine import BacktestEngine
from src.strategies.moving_average_cross import MovingAverageCross

data = load_ohlcv("prices.csv")
engine = BacktestEngine(data, MovingAverageCross(fast=10, slow=30))
result = engine.run()
```

`examples/run_backtest.py` has a full working example with synthetic data if you don't have a CSV handy.

## Stack

Python, pandas, NumPy
