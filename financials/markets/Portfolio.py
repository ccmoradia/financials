from collections import Iterable
import numpy as np
from pandas import DataFrame, concat
import datetime

def _map_columns(column_index, mappings):
    """
    Map new column names to existing columns.
    Works even if only a few columns need to be changed
    
    column_index: list, usually a pandas index
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
    
def _normalize(values):
    """
    Given a set of values, normalize them
    values: pandas Series
    """
    S = values.sum().sum() + 0.0
    return values/S

class Portfolio(object):
    """
    Portfolio class
    """

    def __init__(self):
        self._funds = []
        self._trades = DataFrame(columns = ['TS', 'S', 'Q', 'P', 'M', '_Q', '_V'])          
        
    def _set_Q_P(self):
        """
        Sets the values for _Q and _P columns
        """
        d = {'BUY': 1, 'SELL': -1}
        self._trades['_Q'] = self._trades.S.map(d) * self._trades.Q
        self._trades['_P'] = self._trades.P * self.trades._Q
            
   
    def add_funds(self,amount):
        """
        Add funds to this portfolio
        
        Parameters
        ----------
        amount : int/float/tuple
            amount to be funded
        
        If date is required, pass it as a 2-tuple. There can be more values
        in the tuple but only the first and last value is considered, the
        first being the date and the last being the amount.
        """
        if isinstance(amount, Iterable):
            a = list(amount)
            a[-1] = abs(a[-1]) # Force the value to be positive
            self._funds.append(a)
        else:
            self._funds.append(abs(amount))

                
    def withdraw_funds(self,amount):
        """
        withdraw funds to this portfolio
        
        Parameters
        ----------
        amount : int/float/tuple
            amount to be withdrawn
        
        If date is required, pass it as a 2-tuple. There can be more values
        in the tuple but only the first and last value is considered, the
        first being the date and the last being the amount.
        """
        if isinstance(amount, Iterable):
            a = list(amount)
            a[-1] = -abs(a[-1]) # Force the value to be negative
            self._funds.append(a)
        else:
            self._funds.append(-abs(amount))
        
    def balance(self):
        """
        Gets the current funds position
        """  
        return sum([x[-1] if isinstance(x, Iterable) else x for x in self._funds])
        
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
        consitent with keywords and value            
        """
        dct = kwargs.copy()
        dct['S'] = S
        dct['Q'] = Q
        dct['P'] = P
        dct['M'] = M
        dct['TS'] = datetime.datetime.now() if datetime == 'auto' else TS
        df = DataFrame(array(dct.values().reshape(1, len(dct))), columns = dct.keys())
        self._trades = concat([self._trades, df])
        self._set_Q_P()
        return self._trades
        
        
    def add_trades_from_file(self, filename, mappings = None, **options):
        """
        Add trades from a csv file
        
        filename: filename with path
            The header names must match with the default column names.
            If not, a corresponding mapping must be provided.
            Columns not in the existing dataframe are considered new columns
        mapping: dict
            dictionary mapping headers in the file to default dataframe columns
        **options
            Any of the options that could be passed to the pandas read_csv function      
        """
        df = read_csv(filename, **options)
        if mappings is not None:
            df.columns = _map_columns(df.columns, mappings)
        self._trades = concat([self._trades, df])
        self._set_Q_P()
        return self._trades
        
        
    def weights(self, S = None):
        """
        Get the current weights of the all the stocks in portfolio
        By default, weights for all the stocks are returned
        Use S to restrict the stocks
        
        S: Symbol. string or list. 
            Symbol or list of symbols for which weight is required
        """
        df = self._trades
        df['V'] = _v(df)
        grp = df.groupby('Symbol')
        return _normalize(grp.V)
        
        
    def weight_history(self, S):
        """
        Get the weight history for a symbol
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
        
    
    
        
