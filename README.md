# Backtesting Framework

A modular backtesting engine in Python that ingests historical OHLCV data and executes arbitrary strategy functions against it, tracking position, cash, and equity curve over time. Includes performance analytics (PnL, Sharpe ratio, max drawdown, win rate) with explicit safeguards against lookahead bias and survivorship bias, plus a pluggable signal interface so external models (e.g. a trading-signal classifier) can feed into the framework without modifying core logic.

## Status

Core engine working end-to-end (see `examples/run_backtest.py`).

## Roadmap

- [x] Historical OHLCV data ingestion (`src/data.py`)
- [x] Strategy execution loop (position, cash, equity tracking) (`src/engine.py`, `src/portfolio.py`)
- [x] Performance analytics: PnL, Sharpe ratio, max drawdown (`src/metrics.py`) — win rate not yet added
- [x] Lookahead-bias safeguard: engine only ever exposes bars up to the current one to the signal generator, and fills orders at next-bar open, not the bar the signal was computed on
- [ ] Survivorship-bias safeguard: not solvable in the engine — needs a point-in-time universe from the data vendor; flagged as a known limitation in `src/data.py` for now
- [x] Pluggable external signal interface (`src/signals.py::SignalGenerator`, example plug-in in `src/strategies/moving_average_cross.py`)

## Tech Stack

Python, pandas, NumPy
