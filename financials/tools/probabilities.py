import numpy as np
from pandas import DataFrame

class Probability(object):
    """
    A Probability class for dataframes
    """
    def __init__(self, dataframe):
        """
        Initialize the probability class with a dataframe
        """
        self._df = dataframe
        self._options = {"func": np.size}
        
      
    def get_frequencies(self, rows, columns, values, func = np.size):
        """
        Create a frequency table
        
        rows: row binding
        
        columns : column binding
        
        values: value columns
     
        """
        c = crosstab(rows, columns, values = values, aggfunc = func)
        return c.fillna(0, inplace = True)
        
    def get_probability_table(self, rows, columns, values, func = np.size):
        """
        Create a probability distribution table
        """
        c = get_frequencies(rows, columns, values = values, aggfunc = func)
        return c.div(c.sum(axis = 1), axis = 0)
        
        
    def get_p(self, on, **kwargs):
        """
        Get probability for a particular case
        
        on: column name
        
        kwargs: probability equivalents
        """
        df = self._df[self._df[kwargs.keys()[0]] == kwargs.values()[0]]
        kwargs.popitem()
        for k,v in kwargs.items():
            df = df[df2[k] == v]
        return len(df)/float(len(self._df))
            

