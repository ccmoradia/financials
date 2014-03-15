from collections import Iterable
import numpy as np
from pandas import DataFrame, concat
from pandas.io.parsers import read_csv
from pandas.tseries.offsets import DateOffset
from financials.accounting import cash
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

class Portfolio(object):
    """
    Portfolio class
    """

    def __init__(self, date_format = '%Y-%m-%d'):
        self._cash = DataFrame(columns = ['TS', 'A', 'I'])
        self._trades = DataFrame(columns = ['TS', 'S', 'Q', 'P', 'M', '_Q', '_V'])  
        
    def __repr__(self):
        df = self._trades[['TS', 'S', 'Q', 'P', 'M', '_V']]
        return str(df.set_index('TS'))
        
    def _set_Q_V(self):
        """
        Sets the values for _Q and _P columns
        """
        d = {'BUY': 1, 'SELL': -1}
        self._trades['_Q'] = self._trades.M.map(d) * self._trades.Q
        self._trades['_V'] = self._trades.P * self._trades._Q
            
   
    def add_funds(self, A, TS = None, **kwargs):
        """
        Add funds to this portfolio
        
        Parameters
        ----------
        A : Amount of funds         
        TS: Date/time in specified format        
        """
        D = {'A': abs(A), 'TS': d(TS)}
        D.update(kwargs)
        df = DataFrame([D.values()], columns = D.keys())
        self._cash = concat([self._cash, df], ignore_index = True)
        return self._cash

                
    def withdraw_funds(self, A , TS = None, **kwargs):
        """
        withdraw funds from this portfolio
        
        Parameters
        ----------
        A: Amount of cash to be withdrawn
        TS: Date/time in specified format
        """
        D = {'A': -abs(A), 'TS': d(TS)}
        D.update(kwargs)
        df = DataFrame([D.values()], columns = D.keys())
        self._cash = concat([self._cash, df], ignore_index = True)
        return self._cash        
        
    expense = withdraw_funds # Helper function to add an expense
    
    def cash_ledger(self, from_date = None, to_date = None):
        """
        Display the cash ledger for the specified period
        By default, ledger for the last 30 days are shown        
        """
        to_date = datetime.date.today() if to_date is None else to_date
        from_date = to_date + DateOffset(days = -30) if from_date is None else from_date 
        cash = self._cash[(self._cash.TS >= from_date) & (self._cash.TS <= to_date)]
        trades = self._trades[(self._trades.TS >= from_date) & (self._trades.TS <= to_date)].groupby('TS')._V.sum()
        trades = -trades
        df = DataFrame(trades, columns = ["A"])
        df['I'] = "Trades"
        ledger = concat([df, cash.set_index('TS')])
        return ledger.sort_index()      

    @property
    def cash_balance(self):
        """
        Gets the current funds position
        """  
        return self._cash.A.sum() - self._trades._V.sum()
        
    def add_trades(self,S,Q,P,M,TS='auto',**kwargs):
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
            or any valid python datetiem      
            Time of order execution
            By default, the present time is taken
                   
        **kwargs
        --------
        You could any number of arguments. Each keyword is stored as a
        separate column of information. To get best reports, try to be
        consistent with keywords and value
          
        """
        dct = kwargs.copy()
        dct.update([('S', S), ('Q', Q), ('P', P), ('M', M),
                    ('TS', datetime.datetime.now() if TS == 'auto' else TS)])
        df = DataFrame(np.array(dct.values()).reshape(1, len(dct)), columns = dct.keys())
        self._trades = concat([self._trades, df])
        self._set_Q_V()
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
        df = self._trades
        grp = df.groupby('S')
        return _normalize(grp._V.sum())
        
        
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
    
        
