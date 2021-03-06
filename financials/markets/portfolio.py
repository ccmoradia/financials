from collections import Iterable
import numpy as np
from pandas import DataFrame, concat
from pandas.io.parsers import read_csv
from pandas.tseries.offsets import DateOffset
from financials.accounting.cash import Cash
from financials.tools.AdvancedGroup import AdvancedGroup
from financials.markets.metrics import Metrics
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


def _validate_trades(trades, capital, mode_keys = ("B", "S"), limit = 0,
                    allow_short = False, max_weight = 1.0):

    """
    Validate trades
    trades
        list containing trades in the prescribed format
    mode_keys
        a two tuple indicating the BUY and SELL keys
    limit
        limit below which capital shouldn't fall
    allow_short
        True to allow short sales
    max_weight
        maximum weight for a symbol

    returns a dict with passed trades and failed trades

    #TO DO: Error code for messages
    """
    from collections import Counter
    initial_capital = capital + 0.0 #convert to float
    B,S = mode_keys
    passed = []
    failed = []
    q_counter = Counter()
    v_counter = Counter()
    for trade in trades:
        V = trade["Q"] * trade["P"]
        if trade["M"] == B:
            if V < capital:
                if (v_counter[trade["S"]] + V)/initial_capital < max_weight:
                    q_counter[trade["S"]] = trade["Q"]
                    v_counter[trade["S"]] = V
                    capital -= V
                    passed.append(trade)
                else:
                    failed.append((trade, "Max_weight exceeded"))
            else:
                failed.append((trade, "Lack of capital"))
        elif trade["M"] == S:
            if q_counter[trade["S"]] >= trade["Q"]:
                q_counter[trade["S"]] = -trade["Q"]
                v_counter[trade["S"]] = -V
                capital += V
            else:
                failed.append((trade, "Stock not in holdings"))
        else:
            failed.append((trade, "Mode different"))
    return {"passed": passed, "failed": failed}


class Portfolio(object):
    """
    Portfolio class
    """
    def __init__(self, capital = 0, buy = "BUY", sell = "SELL",
                 limit = 0, allow_short = True, TS = datetime.datetime.now(),
                 validate_mode = False):
        """
        kwargs
        ------
        buy
            buy code
        sell
            sell code
        limit
            the amount beyond which cash shouldn't fall
        allow_short
            allow for short trades
            If True, negative positions are included
        """
        self._cash = Cash(capital, TS = TS)
        self._trades = []
        self._default_columns = ['TS', 'S', 'Q', 'P', 'M', 'V']
        self._buy = buy
        self._sell = sell
        self._limit = limit
        self.metrics = Metrics(self)

    def __repr__(self):
        df = DataFrame(self._trades).set_index("TS")
        return "Balance: {B}, Transactions: {T}".format \
                (B = self.cash_balance, T = len(df))

    def __add__(self, pf):
        """
        Adds two portfolios
        """
        return self.summary + pf.summary

    def __sub__(self, pf):
        """
        Shows the difference between two portfolios
        """
        return self.summary - pf.summary

    def validate_trades(self, replace = False):
        """
        Validates all the trades
        replace
            If True, replace the existing trades with validated trades
            Use this option with caution since it reconstructs the entire
            portfolio
        """
        return self.cash_ledger()[self.cash_ledger().balance < self._limit]

    def validate_positions(self):
        """
        Validates for positions
        """
        trades = self.trades.groupby("S")["Q"].cumsum()
        return self.trades[trades < 0]   #TO DO: A better algorithm

    def add_funds(self, A, TS = None, I = "Capital", **kwargs):
        """
        Add funds to this portfolio

        Parameters
        ----------
        A : Amount of funds
        TS: Date/time in specified format
        """
        return self._cash.add(A, TS, I = I, **kwargs)

    def withdraw_funds(self, A, TS = None, **kwargs):
        """
        withdraw funds from this portfolio

        Parameters
        ----------
        A: Amount of cash to be withdrawn
        TS: Date/time in specified format
        """
        return self._cash.wd(A, TS, **kwargs)

    def expense(self, A, TS = None, **kwargs):
        """
        Add an expense
        """
        return self._cash.wd(A, TS, I = "Expense", **kwargs)

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

    def add_trades(self,S,Q,P,M, I = "Trade", TS=None,**kwargs):
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
        dct.update([('S', S), ('Q', Q if M == self._buy else -Q), ('P', P),
                    ('M', M), ('TS', TS)])
        self._trades.append(dct)
        if M == self._buy:
            self.withdraw_funds(P * Q, TS = TS, I = I)
        else:
            self.add_funds(P * Q, TS = TS, I = I)
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


    def weights(self, method = "transaction", S = None, **kwargs):
        """
        Get the current weights of the all the stocks in portfolio
        By default, weights for all the stocks are returned
        Use S to restrict the stocks
        method
            method to calculate weights
            In case of valuation, a price dataframe to be given
            'transaction' - based on BUY and SELL
            'valuation' - based on present price

        S: Symbol. string or list.
            Symbol or list of symbols for which weight is required

        """
        df = self.summary[self.summary.Q != 0]
        return n(df.V)

    def weight_history(self, S, freq = "M"):
        """
        Get the weight history for a symbol
        S
            Symbol
        freq
            frequency to calculate history
        """
        pass

    @property
    def trades(self):
        """
        Gets the list of trades
        """
        return DataFrame(self._trades).set_index("TS")

    @property
    def summary(self):
        """
        Provides a summary of the portfolio by symbols
        """
        df = DataFrame(self._trades)
        df["V"] = df.P * -df.Q
        return df.groupby("S").agg({"Q": sum, "V": sum})

    def clear_trades(self):
        """
        Clear all trades
        """
        self._trades = []

    @property
    def holdings(self):
        """
        Gets the list of positions
        """
        return DataFrame(self._trades).groupby(['S']).agg({'Q': np.sum})

    def valuation(self, price):
        """
        Get the current valuation
        price
            current price of the stocks as series
        """
        df = DataFrame(self._trades).groupby("S").agg({"Q": sum})
        df["P"] = price.ix[df.index]
        df["V"] = df.Q * df.P
        return df

    def price(self, method = 'average'):
        """
        Average price of the shares
        """
        df = DataFrame(self._trades)
        df["V"] = df.Q * df.P + 0.0
        df2 = df.groupby(["S", "M"]).agg({"Q": sum, "V": sum}).unstack()
        return df2.V/df2.Q

    def infer(self, what, FROM, relation, function):
        """
        Infer required columns from existing columns
        """
        pass

    def f(self, f):
        """
        Filter trades based on conditions
        f
            Any valid pandas dataframe query
        """
        df = DataFrame(self._trades)
        return df.query(f)
