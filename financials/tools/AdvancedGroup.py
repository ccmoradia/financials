# Group Rank method

import pandas as pd
from pandas import DataFrame, Panel, concat

_getarg = lambda x,y: x if x is not None else y
_autoname = lambda x,y,z: x if x is not None else str(y) + str(z)

class AdvancedGroup(object):
    """
    Implements the group rank algorithm
    """
    def __init__(self, dataframe, **kwargs):
        """
        dataframe: A pandas dataframe

        **options
        =========

        TS: TimeStamp column
        Symbol: Symbol column
        """
        self._data = dataframe.copy()
        self._groups = {}
        self._batch = []
        self._dispatch = {"add_col": self.add_col,
                          "add_agg_col": self.add_agg_col,
                          "add_transform_col": self.add_transform_col,
                          "add_feature": self.add_feature}
        options = {"TS": "TS", "S": "S"}
        options.update(kwargs)
        for k,v in options.iteritems():
            setattr(self, k, v)
        self.TS = options.get("TS")
        self.S = options.get("S")

    def _select(self, group):
        """
        Given a group name, select data

        group: group name
        """
        Group = self._groups.get(group)
        if Group is None:
            return "Groups does not exist"

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
        on = _getarg(on, self.S)
        self._groups[name] = ("simple", on, items)

    def add_mapped_group(self, name, mappings, on = None):
        """
        Add a mapped group based on an existing column

        name: name of the group

        mappings: dict/Series with the mappings
            Mappings must provide a one-one to correspondence between
            two groups.

        on: Column by which the items are to be grouped
            This column must be in the dataframe

        """
        on = _getarg(on, self.S)
        self._groups[name] = ("mapped", on, mappings)


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

    @property
    def get_all_groups(self):
        """
        Get the description for all the groups
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
        by = _getarg(by, self.S)
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
        on = _getarg(on, self.S)
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

    @staticmethod
    def add_agg_col(df, by, col, agg_func, group = None, name = None, **kwargs):
        """
        Adds an aggregated column to the dataframe based on some function

        df: dataframe

        by: column by which aggregation is to be done

        col: column on which the aggregation is to be done

        agg_func : the aggregate function

        **kwargs
        keyword arguments to the aggregate function
        """
        name = _autoname(name, agg_func.__name__, col)
        s = df.groupby(by)[col].agg(agg_func, **kwargs)
        df[name] = df[by].map(s)
        return df.reset_index(drop = True)

    @staticmethod
    def add_col(df, name, formula):
        """
        Add a column to the existing dataframe based on a formula
        df: dataframe
        name: name of the column to add
        formula: a valid formula as string
            names in the formula must have columns in the dataframe
            only the operations +,-,*,/,** are supported
        """
        formula = name + "=" + formula
        return df.eval(formula)

    @staticmethod
    def add_transform_col(df, by, cols, trans_func, group = None, name = None, **kwargs):
        """
        Add a transformed column to the dataframe
        df: dataframe
        by: column to group by
        cols: columns for which transformation is to be applied
        trans_func: transformation function
        """
        trans =  df.groupby(by)[cols].transform(trans_func, **kwargs)
        return df.join(trans, lsuffix = "x_", rsuffix = "y_")


    @staticmethod
    def add_feature(df, feature, *args, **kwargs):
        """
        Add a feature as a column to the dataframe
        Useful when creating a dataframe with a lot of properties
        feature
            name of the feature as string. A mapping must exist between
            this string and a function
        args
            arguments to the function
        kwargs
            keyword arguments to the function
        """
        import _features
        mapping = _features.__dict__
        f = mapping[feature]
        return f(df, *args, **kwargs)

    def add_to_batch(self, function, group = None, *args, **kwargs):
        """
        batch functionality for dataframe
        function
            abbr for the function
        """
        self._batch.append((function, group, args, kwargs))

    def do_batch(self):
        """
        Perform all operations in the batch
        """
        result = {}
        for function, group, args, kwargs in self._batch:
            if group is None:
                func = self._dispatch[function]
                print func, func.__name__
                func(self.d, *args, **kwargs)
            else:
                for g in group:
                    if result.get(g) is None:
                        result[g] = self._select(g)
                    func = self._dispatch[function]
                    func(result[g], *args, **kwargs)
        self._batch = []
        return result if len(result) > 0 else self.d


