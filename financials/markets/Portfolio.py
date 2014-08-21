from collections import Iterable
import numpy as np
from pandas import DataFrame, concat
from pandas.io.parsers import read_csv
from pandas.tseries.offsets import DateOffset
from financials.accounting.cash import Cash
from functools import partial
import datetime

def _map_columns(column_index, mappings):
    """
    Map new column names to existing columns.
    Works even if only a few columns need to be changed

    column_index: list, usually a pandas column index
    mappings: dictionary
        mapping of existing columns to new columns
    """
    d = []
    k = mappings.keys()
    v = mappings.values()
    for c in column_index:
        if c in k:
            d.append(mappings[c])
        else:
            d.append(c)
    return d


# Set default dates
d = lambda x=None,y='%Y-%m-%d' : datetime.datetime.now() if x is None else datetime.datetime.strptime(x,y)
# Normalize values
n = lambda x: x/sum(x)

def _set_Q_V(df):
    """
    Sets the values for _Q and _V columns
    """
    d = {'BUY': 1, 'SELL': -1}
    df['_Q'] = df['M'].map(d) * df['Q']
    df['_V'] = df['P'] * df['_Q']
    return df

class Portfolio(object):
    """
    Portfolio class
    """
    def __init__(self, capital = 0, date_format = '%Y-%m-%d'):
        self._cash = Cash(capital)
        self._trades = []
        self._default_columns = ['TS', 'S', 'Q', 'P', 'M', '_V']

    def __repr__(self):
        df = DataFrame(self._trades)
        return str(df.set_index('TS'))

    def add_funds(self, A, TS = None, **kwargs):
        """
        Add funds to this portfolio

        Parameters
        ----------
        A : Amount of funds
        TS: Date/time in specified format
        """
        return self._cash.add(A, TS, **kwargs)

    def withdraw_funds(self, A , TS = None, **kwargs):
        """
        withdraw funds from this portfolio

        Parameters
        ----------
        A: Amount of cash to be withdrawn
        TS: Date/time in specified format
        """
        return self._cash.wd(A, TS, **kwargs)

    def expense(self, A, TS = None, I = "expense", **kwargs):
        """
        Add an expense
        """
        return self._cash.wd(A, TS, I, **kwargs)

    def cash_ledger(self, from_period = None, to_period = None, freq = None):
        """
        Display the cash ledger
        """
        return self._cash.ledger(from_period, to_period, freq)

    @property
    def cash_balance(self):
        """
        Gets the current funds position
        """
        return self._cash.balance

    def add_trades(self,S,Q,P,M,TS=None,**kwargs):
        """
        Add trades to the existing portfolio

        Parameters
        ----------
        S: Symbol. string
            Ticker or stock symbol
        Q: Qty. integer
            The number of shares traded
        P: Price. float
            price at the which the shares are traded
        M: Mode. string
            Whether the stocks are bought or sold
            B for bought and S for sold.
        TS: timestamp. date/time in YY-MM-DD HH:MM:SS format
            or any valid python datetime
            Time of order execution
            By default, the present time is taken

        **kwargs
        --------
        You could use any number of arguments. Each keyword is stored as a
        separate column of information. To get best reports, try to be
        consistent with keywords and value

        """
        dct = kwargs.copy()
        dct.update([('S', S), ('Q', Q), ('P', P), ('M', M), ('TS', TS),
                    ('V', -P*Q if M == "BUY" else P*Q)])
        self._trades.append(dct)
        if M == "BUY":
            self.withdraw_funds(P * Q, TS = TS, I = "Trade")
        else:
            self.add_funds(P * Q, TS = TS, I = "Trade")
        return self._trades


    def add_trades_from_file(self, filename, mappings = None, **options):
        """
        Add trades from a csv file

        filename: filename with path
            The header names must match with the default column names.
            If not, a corresponding mapping must be provided.
            Columns not in the existing dataframe are considered new columns
        mappings: dict
            dictionary mapping headers in the file to default dataframe columns
        **options
            Any of the options that could be passed to the pandas read_csv function
        """
        df = read_csv(filename, **options)
        if mappings is not None:
            df.columns = _map_columns(df.columns, mappings)
        self._trades = concat([self._trades, df])
        self._set_Q_V()
        return self._trades['TS', 'S', 'Q', 'P', 'M']


    def weights(self, S = None):
        """
        Get the current weights of the all the stocks in portfolio
        By default, weights for all the stocks are returned
        Use S to restrict the stocks

        S: Symbol. string or list.
            Symbol or list of symbols for which weight is required

        """
        df = DataFrame(self._trades)
        grp = df.groupby('S')
        return n(grp.V.sum())


    def weight_history(self, S):
        """
        Get the weight history for a symbol
        >>> 10+5
        15
        """

    def ledger(self):
        """
        Gets the ledger info
        """
        pass

    def trades(self):
        """
        Gets the list of trades
        """
        return self._trades

    def clear_trades(self):
        """
        Clear all trades
        """
        cols = self._trades.columns
        print cols
        self._trades = DataFrame(columns = cols)

    def positions(self):
        """
        Gets the list of positions
        """
        return self._trades.groupby(['S']).aggregate({'_Q': np.sum, '_V': np.sum})

    def valuation(self):
        """
        Get the current valuation
        """
        pass

    def shares(self):
        """
        Get the list of shares
        """
        t = self._trades
        q = trades['Trade'].map(_d) * trades.Q


    def price(self, method = 'average'):
        """
        Average price of the shares
        """
        pass

    def infer(self, what, FROM, relation, function):
        """
        Infer required columns from existing columns
        """
        pass

    def filter_trades(self, f = None, t = None, **kwargs):
        """
        Filter trades based on conditions
        """
        pass

    def sort_on(self):
        """
        Toggles sorting and conversion of timestamp data

        Timestamp conversion and sorting is done only when needed
        This could take time in case of a large portfolio.
        Toggling this option converts and sorts data at initialization
        so that processing time could be a bit faster.
        """
        pass