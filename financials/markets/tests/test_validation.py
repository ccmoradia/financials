import os
from financials.markets.validation import _validate_trades as _validate
from nose.tools import *

trades = [
("X", 10, 15, "B"),
("Y", 8, 10, "B"),
("Z", 20, 6, "B"),
("X", 11, 15, "S"),
("Y", 6, 10, "S"),
("Z", 22, 6, "S")
]

trades = [dict(S = a, P = b, Q = c, M = d) for a,b,c,d in trades]
tr = trades # An abbreviation for trades.

# The most obvious case
assert_sequence_equal(tr, _validate(trades, capital = 500))

# Test for capital adequacy
assert_sequence_equal([], _validate(trades, capital = 0))
assert_sequence_equal([tr[0],tr[3]], _validate(trades, capital = 155))
assert_sequence_equal([tr[0],tr[1],tr[3],tr[4]], _validate(trades, capital = 240))

# Short sale not allowed by default
trades[2].update({'M': 'S'})
assert_sequence_equal([tr[0],tr[1],tr[3],tr[4]], _validate(trades, capital = 500))

# Using the allow_short option
assert_sequence_equal(tr, _validate(trades, capital = 500, allow_short = True))

# All short trades
trades[0].update({"M": 'S'})
trades[1].update({'M': 'S'})
assert_sequence_equal([], _validate(trades, capital = 500))
assert_sequence_equal(tr, _validate(trades, capital = 500, allow_short = True))

# Short trades should be executed even without capital (Margins in a later version)
assert_sequence_equal(tr, _validate(trades, capital = 0, allow_short = True))

# Capital and allow_short option
trades[0].update({'M': 'B'})
assert_sequence_equal(tr[1:], _validate(trades, capital = 0, allow_short = True))
assert_sequence_equal(tr, _validate(trades, capital = 200, allow_short = True))
trades[1].update({'M': 'B'})
assert_sequence_equal(tr, _validate(trades, capital = 300, allow_short = True))
assert_sequence_equal([tr[0]] + tr[2:], _validate(trades, capital = 200, allow_short = True))