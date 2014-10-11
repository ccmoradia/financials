# A simple cash register
"""
TO DO

 * Part realization and cancellation of funds
 * Date specific filters
 * Recurring inflows and outflows
 * Split allocations
 * Allow for reallocations
 * Reconcile between cash and funds

"""

import numpy as np
import datetime
from pandas import DataFrame, concat
from pandas.io.parsers import read_csv
from pandas.tslib import Timestamp
from functools import wraps
from financials.utilities.decorators import dataframe

def _set_freq(func):
    """
    Decorator to set frequency
    """
    @wraps(func)
    def wrapped(self, from_period = None, to_period = None, freq = None):
        df = func(self, from_period, to_period)
        df = df.set_index("TS").sort_index().loc[from_period:to_period]
        if freq == None:
            return df
        elif freq == "D":
            t = lambda x: (x.year, x.month, x.day)
        elif freq == "M":
            t = lambda x: (x.year, x.month)
        elif freq == "Y":
            t = lambda x: x.year
        elif freq == "W":
            t = lambda x: (x.year, x.week)
        elif freq == "WD":
            t = lambda x: (x.year, x.weekday())
        else:
            return df
        return df.groupby(t).agg({"A": sum})
    return wrapped

class Cash(object):
    """
    A simple cash register
    """

    def __init__(self, initial_amount = 0, TS = datetime.datetime.now(), **kwargs):
        """
        Initialize the cash register with an amount

        kwargs
        =====
        TS : TimeStamp for the data
        """
        self._cash = []
        self._columns = ['A', 'TS', 'I']
        self._cash.append({"A": initial_amount, "TS": Timestamp(TS), "I": "Opening Balance"})

    def __repr__(self):
        b = self.balance
        i = sum(self._cash.A[self._cash.A > 0])
        o = b - i
        l = 5 if len(self._cash) > 5 else len(self._cash)
        return "Cash Balance: {B:10}\nNet inflows:  {I:10}\nNet outflows: {O:10} \
                \n{D1:*<50}\nLast 5 transactions\n{D2:-^50}\n{D3}".format \
                (B = b, I = i, O = o, D1 = "*", D2 = "-",
                D3 = self._cash.iloc[-l:,:3].set_index("TS").sort_index() if l > 0 else None)


    @property
    def d(self):
        """
        Get the entire cash register
        """
        return self._cash

    def add(self, A, TS = datetime.datetime.now(), I = "Cash added", **kwargs):
        """
        Add cash to this register

        A: Amount of cash

        TS: Date or time in specified format

        **kwargs
        ========

        You could add any number of keyword arguments. Each argument is
        added as a separate column.
        """

        D = {'A': abs(A), 'TS': Timestamp(TS), 'I': I}
        self._cash.append(D)
        return self.balance

    def wd(self, A, TS = datetime.datetime.now(), I = "Cash withdrawn", **kwargs):
        """
        Withdraw cash from register

        A: Amount of cash
        TS: Date or time in specified format
        """
        D = {'A': -abs(A), 'TS': TS, 'I': I}
        self._cash.append(D)
        return self.balance


    @property
    def balance(self):
        """
        Balance in your cash register
        """
        return sum(x["A"] for x in self._cash)

    @_set_freq
    def ledger(self, from_date = None, to_date = None, freq = None):
        """
        Show the cash ledger
        """
        df = DataFrame(self._cash)[self._columns]
        df.set_index("TS", inplace = True)
        df.sort_index(inplace = True)
        df['balance'] = df['A'].cumsum()
        return df.reset_index() # Hack to make decorator work

    def clear(self):
        """
        Clear all entries in the cash register
        """
        self._cash = []

    @_set_freq
    def inflows(self, from_date = None, to_date = None, freq = None):
        """
        Cash inflows for the given period
        """
        df = DataFrame(self._cash)[self._columns]
        return df[df.A > 0]

    @_set_freq
    def outflows(self, from_period = None, to_period = None, freq = None):
        """
        Cash outflows for the given period
        """
        df = DataFrame(self._cash)[self._columns]
        return df[df.A < 0]

    @_set_freq
    def zeroflows(self, from_period = None, to_period = None, freq = None):
        """
        Outflows equal to zero
        This is just for theoretical usage
        """
        df = DataFrame(self._cash)[self._columns]
        return df[df.A == 0]

    def summarize(self, tags = ["I"], from_period = None, to_period = None):
        """
        Tags as list
        """
        df = DataFrame(self._cash)
        return df.groupby(tags).agg({"A": sum}).loc[from_period: to_period]

    def f(self, query):
        """
        Filter data based on query
        query
            A valid pandas dataframe query
        """
        df = DataFrame(self._cash)
        return df.query(query)