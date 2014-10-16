Building a data store for price data
=====================

We would try mimicking a stock index.

The following data are required to build a data store right from scratch

 * End of day data
 * Dividends
 * Split/Bonus
 * Symbol Change

Other data

 * Indices
 * Change to indices

Fundamentals

 * Quarterly results

Lets go through each of them

End of day data
==========
End of day data is preferred to avoid survivorship bias
The following fields are mandatory
 * Timestamp
 * Symbol
 * Open
 * High
 * Low
 * Close
 * Volume
 * Turnover
 
Dividends
======
 * Timestamp
 * Symbol
 * Dividend

Split/Bonus
=======
 * Timestamp
 * Symbol
 * Multiplier

Symbol Change
==========
 * Timestamp
 * Old Symbol
 * New Symbol

Indices
=====
 * Symbol

Change to indices
===========
 * Timestamp
 * Symbol
 * Inclusion/Exclusion into index

Fundamental data
===========
Its better to store fundamental data as key value pairs or csv files for separate symbols. They take the form
{Symbol: {key_1:  value_1 , key_2: value_2, key_n: value_n}}
This could also be
{Revenue: {Symbol_1: value_1, Symbol_2: value_2, Symbol_n: value_n}}
By iterating over key/value pairs, they could be transformed to arrays.
A few keys for fundamental data
 * Revenue/Earnings
 * Cash
 * Assets
 * Operating Profit
 * EBIT
 * Earnings after tax
and more