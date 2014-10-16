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

# The most obvious case
assert_sequence_equal(trades, _validate(trades, capital = 500))

# Test for capital adequacy
assert_sequence_equal([], _validate(trades, capital = 0))
assert_sequence_equal(trades[0,3], _validate(trades, capital = 155))

# Short sale not to be allowed
trades[2].update({'M': 'S'})
assert_sequence_equal(trades[0,1,3:], _validate(trades, capital = 500))

# Using the allow_short option
assert_sequence_equal(trades, _validate(trades, capital = 500, allow_short = True))

# Using the max_holding option
trades[2].update({'M': 'B', 'Q': 12})
assert_sequence_equal(trades[0,1,3,4],
                     _validate(trades, capital = 500, max_holding = 0.4))

# Using max_holding and allow_short
assert_sequence_equal(trades[0,1,3:], _validate(trades, capital = 500,
                      max_holding = 0.4, allow_short = True))

# Using the min_holding option
