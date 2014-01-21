# Create in memory dataframes for csv, txt files

import os
from pandas.io.parsers import read_csv
from pandas import DataFrame, Panel

class TextConnection(object):
    """
    Text Connection object
    """
    
    def __init__(self, directory, **options):
        """
        Directory where file exists
        
        options - keyword arguments to be passed to read_csv function
        """
        self._dir = directory
        
        
    def aggregate_data(self):
        """
        Aggregate data into a dataframe by reading file by file
        """
        df = DataFrame()
        for (a,b,c) in os.walk(self._dir):
            for f in c:
                fn = os.path.join(a,f)
                df = concat([df, read_csv(fn, **options)])
                
        return df
