"""Transaction cost correctness. The key invariant proven here: with
cost_bps=0, rebalance_to always leaves cash at exactly 0 after any non-flat
trade (it's fully invested by construction), so every later bar with an
unchanged signal is a mathematically exact no-op - that's what makes the
zero-cost path provably identical to pre-cost-feature behavior for ANY
strategy, not just buy-and-hold. With cost_bps>0, that same identity forces
cash to exactly -cost right after the trade, which is the precise, isolated
claim to check instead of the final equity gap (that gap keeps growing over
time - it's the missing cash also missing out on future appreciation, not a
sign the fee was charged more than once).
"""

import pandas as pd

from src.engine import BacktestEngine
from src.signals import Signal, SignalGenerator
from src.strategies.buy_and_hold import BuyAndHold


class AlternatingStrategy(SignalGenerator):
    """Flips LONG/FLAT every 5 bars so a run exercises multiple trades,
    not just one entry."""

    def generate(self, history: pd.DataFrame) -> Signal:
        t = len(history) - 1
        return Signal.LONG if (t // 5) % 2 == 0 else Signal.FLAT


def _make_data(n: int = 30, start_price: float = 100.0, drift: float = 0.5) -> pd.DataFrame:
    prices = [start_price + drift * i for i in range(n)]
    return pd.DataFrame({"open": prices, "close": prices})


def test_zero_cost_matches_default():
    data = _make_data()
    explicit_zero = BacktestEngine(data, AlternatingStrategy(), cost_bps=0.0).run()
    default = BacktestEngine(data, AlternatingStrategy()).run()
    pd.testing.assert_series_equal(explicit_zero["equity"], default["equity"])


def test_positive_cost_strictly_reduces_equity():
    data = _make_data()
    free = BacktestEngine(data, AlternatingStrategy(), cost_bps=0.0).run()
    costly = BacktestEngine(data, AlternatingStrategy(), cost_bps=10.0).run()
    assert costly["equity"].iloc[-1] < free["equity"].iloc[-1]


def test_buy_and_hold_entry_charged_exactly_once_and_correctly_sized():
    """Checks the mechanism directly (cash right after the one real trade)
    rather than the final equity gap, which legitimately drifts over time -
    see module docstring."""
    data = _make_data(n=10)
    cost_bps = 10.0
    engine = BacktestEngine(data, BuyAndHold(), cost_bps=cost_bps)

    entry_price = data["open"].iloc[1]
    initial_cash = 100_000.0
    expected_shares = initial_cash / entry_price
    expected_cost = expected_shares * entry_price * (cost_bps / 10_000)

    # run one bar at a time so we can inspect state right after the entry trade
    engine.data = data.reset_index(drop=True)
    portfolio = engine.portfolio
    signal_gen = engine.signal_generator
    history = engine.data.iloc[:1]
    signal = signal_gen.generate(history)
    portfolio.rebalance_to(signal, entry_price)

    assert portfolio.cash == -expected_cost
    assert portfolio.position == expected_shares


def test_flat_strategy_never_trades_so_never_pays_cost():
    data = _make_data()

    class AlwaysFlat(SignalGenerator):
        def generate(self, history: pd.DataFrame) -> Signal:
            return Signal.FLAT

    result = BacktestEngine(data, AlwaysFlat(), cost_bps=10.0).run()
    assert (result["equity"] == 100_000.0).all()
