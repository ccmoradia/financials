"""
This module provides validation functions
"""

def _is_stock_available(avl, ord):
    """
    Whether the stock is available for sale (it must be in holdings)
    """
    return True if avl >= ord else False

def _is_capital_available(cap, ord, lim):
    """
    Whether sufficient capital is available for buying a stock
    """
    return True if (cap - ord) >= lim else False

def _validate_trades(trades, capital, limit = 0, allow_short = False):
    """
    validate whether the trade is feasible
    """
    value_counter = {}
    qty_counter = {}
    validated_trades = []
    invalidated_trades = []

    def _validate():
        if M == "S":
            if allow_short:
                return True
            else:
                if _is_stock_available(qty_counter[S], Q):
                    return True
                else:
                    return False
        elif M == "B":
            if _is_capital_available(capital, V, limit):
                return True
            else:
                False
        else:
            return False

    for trade in trades:
        S,P,Q,M = trade["S"], trade["P"], trade["Q"], trade["M"]
        qty_counter.setdefault(S, 0)
        value_counter.setdefault(S, 0)
        V = P*Q
        if _validate():
            validated_trades.append(trade)
            if M == "S":
                capital += V
                qty_counter[S] -= Q
                value_counter[S] -= V
            else:
                capital -= V
                qty_counter[S] += Q
                value_counter[S] += V
        else:
            invalidated_trades.append(trade)

    return validated_trades