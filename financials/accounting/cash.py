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

d = lambda x=None,y='%Y-%m-%d' : datetime.datetime.now() if x is None else datetime.datetime.strptime(x,y)

class Cash(object):
    """
    A simple cash register
    """
    def __init__(self, initial_amount = 0, date_format = '%Y-%m-%d'):
        """
        Initialize the cash register with an amount
        """
        self._cash = DataFrame(columns = ['A','TS','I'])
        self._funds = DataFrame(columns = ['A', 'TS', 'FD', 'I'])
        self._columns = ['A', 'TS', 'I']
        self._options = {}
        self._options['dtf'] = date_format
        df = DataFrame([[initial_amount, datetime.datetime.now(), 'Opening Balance']], columns = self._columns)
        self._cash = concat([self._cash, df])
        
    def __repr__(self):
        return str(self._cash)
        
    def add(self, A, TS = None, **kwargs):
        """
        Add cash to this register
        
        A: Amount of cash
        
        TS: Date or time in specified format
        
        **kwargs
        ========
        
        You could add any number of keyword arguments. Each argument is 
        added as a separate column.         
        """
        
        D = {'A': abs(A), 'TS': d(TS,self._options['dtf'])}
        D.update(kwargs) 
        df = DataFrame([D.values()], columns = D.keys())
        self._cash = concat([self._cash, df], ignore_index = True)
        return self._cash
        
        
    def wd(self, A, TS = None, **kwargs):
        """
        Withdraw cash from register
        
        A: Amount of cash
        TS: Date or time in specified format        
        """
        D = {'A': -abs(A), 'TS': d(TS, self._options['dtf'])}
        D.update(kwargs)
        df = DataFrame([D.values()], columns = D.keys())
        self._cash = concat([self._cash, df], ignore_index = True)
        return self._cash
        
    def balance(self):
        """
        Balance in your cash register
        """
        return sum(self._cash['A'])
        
    def ledger(self, from_date = None,to_date = None):
        """
        Show the cash ledger
        """
        df = self._cash[self._columns]
        df.set_index('TS', inplace = True)
        df.sort_index(inplace = True)
        df['balance'] = df['A'].cumsum()
        return df
        
    def clear(self):
        """
        Clear all entries in the cash register
        """
        self._cash = DataFrame(columns = ['A','TS','I'])
        
    def add_funds(self, A, TS = None, FD = None, **kwargs):
        """
        Add funds realizable in the future to the register
        
        A: Amount
        
        TS: Timestamp
        
        FD: Future date
        
        Future date on which the inflow is expected or allocation is
        to be met
        
        kwargs
        ------
        Any keyword arguments would be added as a separate column
        """
        D = {'A': abs(A), 'TS': d(TS,self._options['dtf']), 'FD': FD}
        D.update(kwargs) 
        df = DataFrame([D.values()], columns = D.keys())
        self._funds = concat([self._funds, df], ignore_index = True)
        return self._funds
        
    def cancel(self, ID):
        """
        Cancel an expected inflow or allocation
        """
        self._funds = self._funds.drop(ID)
        return self._funds
        
        
    def realize(self, ID):
        """
        Realize funds
        
        If funds are realized, move them from funds to cash.
       
        ID
        ID of the entry to realize        
        """
        f = self._funds.loc[ID]
        self.add(f['A'], f['FD'], I = f['I'])
        self._funds = self.cancel(ID)
        return self.balance()
        
    def allocate(self, A, TS = None, FD = None, **kwargs):
        """
        Allocate funds for the future
        
        A: Amount to allocate
        TS: TimeStamp
        FD: Future Date
        """
        D = {'A': -abs(A), 'TS': d(TS,self._options['dtf']), 'FD': FD}
        D.update(kwargs) 
        df = DataFrame([D.values()], columns = D.keys())
        self._funds = concat([self._funds, df], ignore_index = True)
        return self._funds
        
    def funds_position(self):
        """
        Get the funds position
        """
        return {
                'inflows': sum(self._funds[self._funds['A'] >= 0]['A']),
                'outflows': sum(self._funds[self._funds['A'] < 0]['A']),
                'Net': sum(self._funds['A'])
                }
                
    def reallocate(self):
        """
        Reallocate funds
        """
        pass
        
    def reconcile(self):
        """
        Reconcile cash and funds
        """
        pass
        
    def summary(self):
        """
        Summary snapshot
        """
        pass
        

        
   
