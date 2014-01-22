# Create in memory dataframes for csv, txt files

import os
from pandas.io.parsers import read_csv
from pandas import DataFrame, Panel, concat

class TextConnection(object):
    """
    Text Connection object
    """
    
    def __init__(self, directory):
        """
        Directory where file exists
        
        options - keyword arguments to be passed to read_csv function
        """
        self._dir = directory
        
        
    def aggregate_data(self, fns = False, **kwargs):
        """
        Given a directory path, aggregate data from csv files into a dataframe 
        
        fns (filename as symbol): Boolean/ default False
            adds the filename as the symbol column in the dataframe
        
        kwargs: Could pass all options to the pandas read_csv function
        """
        df = DataFrame()
        for root,dirs,files in os.walk(self._dir):
            for f in files:
                fn = os.path.join(root, f)
                d = read_csv(fn, **kwargs)
                d['SYMBOL'] = f[:-4]
                df = concat([df, d])
        self._df  = df                
         
    def get_data(self, symbols, **kwargs):
        """
        Get data for the required symbols
        
        symbols: string/list
            list of symbols
            TO DO: list of symbols to be implemented
        """
        df = self._df
        return df[df['SYMBOL'] == symbols]
