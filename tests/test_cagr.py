"""CAGR is a geometric, not arithmetic, annualization - see src/metrics.py.
The +100%/-50% case below is the canonical proof: arithmetic mean of those
two returns is +25%, but the account is back to exactly where it started,
and CAGR must report 0% to be correct.
"""

import pandas as pd

from src.metrics import cagr


def test_cagr_zero_for_round_trip():
    # +100% then -50%, one year each: 100 -> 200 -> 100
    equity = pd.Series([100.0, 200.0, 100.0])
    assert cagr(equity, periods_per_year=1) == 0.0


def test_cagr_matches_simple_case_over_multiple_years():
    # doubles over 2 years -> CAGR should be sqrt(2) - 1, not the naive 50%
    # a flat average of "+100% total over 2 years" would suggest
    equity = pd.Series([100.0, 141.42135623730951, 200.0])
    result = cagr(equity, periods_per_year=1)
    assert abs(result - (2 ** 0.5 - 1)) < 1e-9


def test_cagr_zero_for_single_bar():
    equity = pd.Series([100.0])
    assert cagr(equity) == 0.0
