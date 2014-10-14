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


