# Group Rank method

import pandas as pd
from pandas import DataFrame, Panel
import h5py

class GroupRank(object):
    """
    Implements the group rank algorithm
    """
    def __init__(self, datasource = None, data = None, **options):
        """
        datasource: string. Path to a HDF5 file
        data: DataFrame. Data in OHLCV format
        """
        self._datasource = datasource
        self._data = data
        
    def add_data(self, data, append = True):
        """
        Adds data
        
        data: DataFrame. data to add
        
        append: Boolean/default True
        If True, data is appended to the available data
        If False, the old data is replaced by the new data
        """
        if append:
            self.data = pd.concat([self._data, data])
        else:
            self._data = data
