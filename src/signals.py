"""The plug interface every strategy has to implement to hook into the engine."""

from abc import ABC, abstractmethod
from enum import IntEnum

import pandas as pd


class Signal(IntEnum):
    SHORT = -1
    FLAT = 0
    LONG = 1


class SignalGenerator(ABC):
    """Pluggable strategy interface. Anything that can look at price
    history up to the current bar and emit a directional call implements
    this — a moving-average rule today, an ML classifier later."""

    @abstractmethod
    def generate(self, history: pd.DataFrame) -> Signal:
        """`history` is sliced by the engine to bars up to and including
        the current one. Never assume you can see beyond it."""
        raise NotImplementedError
