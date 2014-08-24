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
from functools import wraps

d = lambda x=None,y='%Y-%m-%d' : datetime.datetime.now() if x is None else datetime.datetime.strptime(x,y)

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
    def __init__(self, initial_amount = 0, TS = None, date_format = '%Y-%m-%d', **kwargs):
        """
        Initialize the cash register with an amount

        kwargs
        =====
        TS : TimeStamp for the data
        """
        self._cash = DataFrame(columns = ['A','TS','I'])
        self._funds = DataFrame(columns = ['A', 'TS', 'FD', 'I'])
        self._columns = ['A', 'TS', 'I']
        self._options = {}
        self._options['dtf'] = date_format
        df = DataFrame([[initial_amount, d(TS), 'Opening Balance']], columns = self._columns)
        self._cash = concat([self._cash, df])

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

        D = {'A': abs(A), 'TS': TS, 'I': I}
        D.update(kwargs)
        df = DataFrame([D.values()], columns = D.keys())
        self._cash = concat([self._cash, df], ignore_index = True)
        return self._cash[self._columns].set_index("TS")


    def wd(self, A, TS = datetime.datetime.now(), I = "Cash withdrawn", **kwargs):
        """
        Withdraw cash from register

        A: Amount of cash
        TS: Date or time in specified format
        """
        D = {'A': -abs(A), 'TS': TS, 'I': I}
        D.update(kwargs)
        df = DataFrame([D.values()], columns = D.keys())
        self._cash = concat([self._cash, df], ignore_index = True)
        return self._cash[self._columns].set_index("TS")

    @property
    def balance(self):
        """
        Balance in your cash register
        """
        return sum(self._cash['A'])

    @_set_freq
    def ledger(self, from_date = None, to_date = None, freq = None):
        """
        Show the cash ledger
        """
        df = self._cash[self._columns].set_index('TS')
        df.sort_index(inplace = True)
        df['balance'] = df['A'].cumsum()
        return df.reset_index() # Hack to make decorator work

    def clear(self):
        """
        Clear all entries in the cash register
        """
        self._cash = DataFrame(columns = ['A','TS','I'])

    @_set_freq
    def inflows(self, from_period = None, to_period = None, freq = None):
        """
        Cash inflows for the given period
        """
        return self._cash[self._cash.A > 0]

    @_set_freq
    def outflows(self, from_period = None, to_period = None, freq = None):
        """
        Cash outflows for the given period
        """
        return self._cash[self._cash.A < 0]

    @_set_freq
    def zeroflows(self, from_period = None, to_period = None, freq = None):
        """
        Outflows equal to zero
        This is just for theoretical usage
        """
        return self._cash[self._cash == 0]

    def summarize(self, tags = ["I"], from_period = None, to_period = None):
        """
        Tags as list
        """
        return self._cash.groupby(tags).agg({"A": sum}).loc[from_period: to_period]

    def f(self, query):
        """
        Filter data based on query
        query
            A valid pandas dataframe query
        """
        return self._cash.query(query)

