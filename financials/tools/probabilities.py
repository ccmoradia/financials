import numpy as np
from pandas import DataFrame
from collections import Iterable

def frequency_table(dataframe, on, by, agg = 'size', stackby = None, fillNaN = True, fillvalue = 0, aggfunc = {}):
    """
    Calculate a frequency distribution table for a discrete distribution

    dataframe
        a pandas dataframe object
    on
        column for which frequency distribution table is to be calculated
    by
        columns by which the table is to be aggregated
    agg
        aggregation function to used
        size: counts the number of occurences
        sum: sums the number of occurences
    stackby
        colums by which the results are to be stacked
    fillNaN
        fill Nan values. Default True
    fillvalue
        value to fill for Nan values
    aggfunc
        list of function for each of the on variables
    """
    grouped = dataframe.groupby(by, sort = False)
    func_dict = {k: aggfunc[k] if aggfunc.get(k) is not None else agg for k in on}
    grp = grouped.aggregate(func_dict)

    if stackby is not None:
        grp = grp.unstack(stackby)
        if fillNaN:
            grp.fillna(fillvalue, inplace = True)

    return grp

def normalize(s):
    """
    Normalize a series or dataframe such that the sum is one
    Given a dataframe, columns are assumed to be independent events

    s: pandas Series/DataFrame
    """
    S = sum(s.values.ravel()) + 0.0
    return s/S

class Probability(object):
    """
    A Probability class for easy manipulation
    """
    def __init__(self, dataframe):
        """
        Initializes the object with the given dataframe
        """
        self._df = dataframe
        self._tables = {}

    def __repr___(self):
        """
        String representation
        """
        return "# of tables : " + str(len(self.tables))

    def add_table(self, on, by, name ="auto", **options):
        """
        Add a probability distribution table for faster lookups
        """
        if name == "auto":
            name = "table" + str(len(self.tables))
        self._tables[name] = normalize(frequency_table(self._df, on ,by, **options))

    def remove_table(self, name):
        """
        Remove a table
        """
        del self._tables[name]

    def remove_all_tables(self):
        """
        Removes all the tables
        """
        self._tables = {}

    @property
    def get_tables(self):
        """
        Returns the list of tables
        """
        return self._tables.keys()

    def lookup(self, table, key):
        """
        Lookup the probability value of the key in the given table
        The probability of this key must exist in the table
        otherwise nan is returned

        table:
            table to look into

        key:
            key to look up
        """
        try:
            return self._tables[table].loc[key]
        except KeyError:
            return np.nan

    def lookup_var(self, table, var, on):
        """
        Lookup the probability of a variable

        table
            table to look into
        var
            variable to look for
        on
            column to look for
        """
        try:
            return self._tables[table].xs(var, level = on)
        except KeyError, AttributeError:
            return np.nan

    def nlookup_var(self, table, var, on):
        """
        Lookup the probability of a variable and return normalized values
        """
        return normalize(self.lookup_var(table, var, on))

    def pmf(self, table):
        """
        Plot the pmf for the table
        """
        self._tables[table].plot(kind = "bar")

    def cdf(self, table):
        """
        Plot the CDF for the table
        """
        self._tables[table].cumsum().plot()

    def hist(self, table):
        """
        Plot the histogram for the table
        """
        self._tables[table].hist()