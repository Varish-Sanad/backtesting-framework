"""Cash, position, and equity bookkeeping for a single backtest run."""

from dataclasses import dataclass, field

from .signals import Signal


@dataclass
class Portfolio:
    initial_cash: float
    cash: float = field(init=False)
    position: float = field(init=False, default=0.0)
    equity_curve: list[float] = field(init=False, default_factory=list)

    def __post_init__(self) -> None:
        self.cash = self.initial_cash

    def rebalance_to(self, signal: Signal, price: float) -> None:
        """Move to fully-invested long, fully-invested short, or flat at `price`.
        Naive all-in/all-out sizing — no position scaling or risk limits."""
        equity = self.cash + self.position * price
        if signal == Signal.LONG:
            target_position = equity / price
        elif signal == Signal.SHORT:
            target_position = -equity / price
        else:
            target_position = 0.0

        delta_shares = target_position - self.position
        self.cash -= delta_shares * price
        self.position = target_position

    def mark_to_market(self, price: float) -> float:
        equity = self.cash + self.position * price
        self.equity_curve.append(equity)
        return equity
