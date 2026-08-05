# Backtesting Framework

A modular backtesting engine in Python that ingests historical OHLCV data and executes arbitrary strategy functions against it, tracking position, cash, and equity curve over time. Includes performance analytics (PnL, Sharpe ratio, max drawdown, win rate) with explicit safeguards against lookahead bias and survivorship bias, plus a pluggable signal interface so external models (e.g. a trading-signal classifier) can feed into the framework without modifying core logic.

## Status

In progress.

## Roadmap

- [ ] Historical OHLCV data ingestion
- [ ] Strategy execution loop (position, cash, equity tracking)
- [ ] Performance analytics: PnL, Sharpe ratio, max drawdown, win rate
- [ ] Lookahead-bias and survivorship-bias safeguards
- [ ] Pluggable external signal interface

## Tech Stack

Python, pandas, NumPy
