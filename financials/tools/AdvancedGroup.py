# Group Rank method

import pandas as pd
from pandas import DataFrame, Panel, concat

_getarg = lambda x,y: x if x is not None else y
_autoname = lambda x,y,z: x if x is not None else str(y) + str(z)

class AdvancedGroup(object):
    """
    Implements the group rank algorithm
    """
    def __init__(self, dataframe, inplace = False, **kwargs):
        """
        dataframe: A pandas dataframe
        
        inplace: default False
            If True, changes are made to the existing dataframe
            If False, the existing dataframe is copied and
            changes are made to the new dataframe
        
        **options   
        =========
        
        TS: TimeStamp column
        Symbol: Symbol column    
        """
        if inplace:
            self._data = dataframe
        else:
            self._data = dataframe.copy()
        self._groups = {}
        options = {"TS": "TS", "Symbol": "Symbol"}
        options.update(kwargs)        
        self.TS = options.get("TS")
        self.Symbol = options.get("Symbol")
        
    def _select(self, group):
        """
        Given a group name, required data is selected
        
        group: group name
        """
        Group = self._groups.get(group)
        if Group is None:
            return "Group does not exist"
         
        group_type, columns, items = Group
        if group_type == "simple":
            if isinstance(columns, (list, tuple)):
                df = self._data.copy()
                for c,i in zip(columns, items):
                    df = df[df[c].isin(i)]
                return df
            else:
                return self._data[self._data[columns].isin(items)]
        elif group_type == "mapped":
            df = self._data.copy()
            if isinstance(columns, (list, tuple)):
                for c,i in zip(columns, items):
                    df["map"+c] = df[c].map(i)
                return df
            else:
                df[group] = df[columns].map(items)
                return df                  
                
        else:
            return "Group type must be simple or mapped"
    
    
    def add_group(self, name, items, on = None):
        """
        Add a group
        
        name: name of the group
          
        items: list/tuple of names in the group
        
        on: Column by which the items are to be grouped
            This column must be in the dataframe  
            
        If you want to add multiple columns, pass a list of
        lists or tuples for both items and the on argument.
        The length of the items and on columns must match
        """
        self._groups[name] = ("simple", _getarg(on, self.Symbol), items)
        
    def add_mapped_group(self, name, mappings, on = None):
        """
        Add a mapped group based on an existing column
        
        name: name of the group
        
        mappings: dict/Series with the mappings
            Mappings provide a one-one to correspondence between
            two groups. 
         
        on: Column by which the items are to be grouped
            This column must be in the dataframe            
                    
        """
        self._groups[name] = ("mapped", _getarg(on, self.Symbol), mappings)
        
       
    @property
    def groups(self):
        """
        List all the available groups
        """
        return self._groups.keys()
        
    @property
    def d(self):
        """
        return the entire data
        """
        return self._data
        
    def get_group(self, name, isprint = True):
        """
        Print data for the group
        
        name: name of the group
        """
        if isprint:
            print "Group name: {0} \nType: {1[0]} \n Members: {1[1]}".format(name, self._groups[name])
        return self._groups.get(name)
        
    def get_all_groups(self):
        """
        Get data for all groups
        """
        return self._groups        

       
    def add_rank(self, col, on = None, by = None, group = None, name = None, **kwargs):
        """
        Add rank based on a column
        
        col: column for which rank is to be calculated
        
        on: column on which rank is to be calculated
        
        by: column by which rank is assigned
        
        group: group for which rank is to be calculated
            If None, the entire data is selected
        
        name: name of the new column
        
        **options: kwargs to the pandas rank function
        """
        options = {"method": "first", "ascending": False, "axis": 0}
        options.update(kwargs)
        on = _getarg(on, self.TS)
        by = _getarg(by, self.Symbol)
        name = _autoname(name, "Rank", col)        
       
        def rank_it(df):
            df = df.set_index([on, by])
            df2 = df.unstack(level = on)
            df[name] = df2.xs(col, axis = 1, level = 0).rank(**options).unstack(by)
            return df.reset_index()             
    
        if group is None:
            self._data = rank_it(self._data)
            return self._data
        else:            
            if isinstance(group, (list, tuple)):
                return {g: rank_it(self._select(g)) for g in group}
            else:
                return rank_it(self._select(group))
                
    def add_lag(self, col, lag = 1, on = None, by = None, group = None, name = None):
        """
        Adds a time lag to the data
        
        col: column for which lag is to be added
        
        lag: int
            Time lag to add
        """
        on = _getarg(on, self.Symbol)
        by = _getarg(by, self.TS)
        name = _autoname(name, "Lag", col)
        
        def lag_it(df):
            df = df.set_index([on, by])
            df2 = df.unstack(level = on)
            df[name] = df2.xs(col, axis = 1, level = 0).shift(lag).unstack(by)
            return df.reset_index()
            
        if group is None:
            self._data = lag_it(self._data)
            return self._data
        else:
            if isinstance(group, (list, tuple)):
                return {g: lag_it(self._select(g)) for g in group}
            else:
                return lag_it(self._select(group))
                
    def add_agg_col(self, by, col, agg_func, group = None, name = None, **kwargs):
        """
        Adds an aggregated column to the dataframe based on some function
        
        by: column by which aggregation is to be done
        
        col: column on which the aggregation is to be done        
   
        agg_func : the aggregate function
        
        **kwargs
        keyword arguments to the aggregate function
        """
        name = _autoname(name, agg_func.__name__, col)
        
        def agg_it(df):
            s = df.groupby(by)[col].agg(agg_func, **kwargs)
            df[name] = df[by].map(s)
            return df.reset_index(drop = True)        
            
        if group is None:
            self._data = agg_it(self._data)
            return self._data
        else:
            if isinstance(group, (list, tuple)):
                return {g:agg_it(self._select(g)) for g in group}                
            else:
                return agg_it(self._select(group)) 
