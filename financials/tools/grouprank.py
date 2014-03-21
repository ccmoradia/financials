# Group Rank method

import pandas as pd
from pandas import DataFrame, Panel, concat
import h5py

class GroupRank(object):
    """
    Implements the group rank algorithm
    """
    def __init__(self, datasource = None, **options):
        """
        datasource: A valid datasource
        
        **options
        =========
        """
        self._datasource = datasource
        self._data = data
        self._groups = []
        
    def add_data(self, data, append = True):
        """
        Adds data
        
        data: DataFrame. data to add in OHLCV format
        
        append: Boolean/default True
        If True, data is appended to the available data
        If False, the old data is replaced by the new data
        """
        if append:
            self._data = concat([self._data, data])
        else:
            self._data = data
            
    def add_lag(self, on, lag = 1, name = None):
        """
        Add a new column based on the time lag of an existing column
        
        on: column on which the lag is to added
        
        lag: lag time in integer
            This number could be negative if lag is to be backward
         
        name: name of the new column
            If name is not given, an automatic name is generated        
        """
        if name is None:
            name = on + "Lag" + str(lag)
        self._data[name] = self._data[on].shift(lag)
        
    def add_rank(self, by, on, name = None, **options):
        """
        Add rank based on an existing column
        Ranks are based on the index and then the column given
        
        by: column by which data is to be grouped
        
        on: column to be ranked
           
        name: name of the new column
            If name is not given, an automatic name is generated
            
        **options: any of the options that could be passed to the rank function
        
        """
        if name is None:
            name = on + "Rank"
            
        p = df.set_index(by, append = True).to_panel()
        p = p.transpose(0,2,1)
        return p[on].rank(**options).stack()
        
    def add_group(name, items):
        """
        Add a group
        
        name: name of the group
        
        items: list/tuple of names in the group       
        """
        self._groups[name] = items
        
    @property
    def groups(self):
        """
        List the available groups
        """
        return self._groups.keys()
        
    def group(self, name, on):
        """
        Group data for further analysis
        
        name: name of the group
        
        on: column on which the group is to applied
            The column must contain string values
        """
        return self._data[self._data[on].isin(self._groups[name])]
