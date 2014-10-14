"""
This module provides validation functions
"""
from collections import Counter


_is_stock_available = lambda avl, ord: True if avl >= ord else False
_is_min_holding = lambda cap, hol, per: True if hol/cap >= per else False
_is_max_holding = lambda cap, hol, per: True if hol/cap <= per else False
_is_capital_available = lambda cap, ord, lim: True if (cap - ord) >= lim else False

def _validate_trades(trades, capital, limit = 0, allow_short = False,
                    min_holding = 0, max_holding = 1,
                    part_fill = False):
    qty_counter = {}
    value_counter = {}
    validated_trades = []
    invalidated_trades = []

    def _validate():
        if trade["M"] == "S":
            if _is_stock_available(qty_counter[S], Q):
                if _is_min_holding(capital, value_counter[S], min_holding):
                    return True
                else:
                    return False
            else:
                return False
        elif trade["M"] == "B":
            if _is_capital_available(capital, V, limit):
                if _is_max_holding(capital, value_counter[S], max_holding):
                    return True
                else:
                    return False
            else:
                return False
        else:
            return False

    for trade in trades:
        S,P,Q,M = trade["S"], trade["P"], trade["Q"], trade["M"]
        V = P*Q
        if _validate():
            validated_trades.append(trade)
            if M == "S":
                capital += V
                qty_counter[S] -= S
                value_counter[S] -= S
            else:
                capital -= V
                qty_counter[S] += V
                value_counter[S] += V
        else:
            invalidated_trades.append(trade)

    return validated_trades