# All decorator functions go here

from functools import wraps
from pandas import DataFrame, Series, DatetimeIndex

def clean_up(function):
    """
    Checks for Series/DataFrame types and adds other goodies
    set_index
        set the index to the specified column
        name of the column. applies only to datafrme
    convert_to_datetimeindex
        convert the columns to Datetimeindex
    d
        attribute referring to the dataframe or series in the class
    """
    @wraps(function)
    def wrapped(df, set_index = None, convert_to_datetimeindex = None, \
    d = None, *args, **kwargs):
        if not isinstance(df, (DataFrame, Series)):
            if hasattr(df, "d"):
                df = df.d
            elif d is not None:
                df = getattr(df, d)
            else:
                raise AttributeError("Thisclass has no attribute d")

        if convert_to_datetimeindex is True:
            df[set_index] = DatetimeIndex(df[set_index])

        if set_index is not None:
            df.set_index(set_index, inplace = True)

        return function(df, *args, **kwargs)
    return wrapped


def period(function):
    """
    Given a Series/DataFrame with a datetime index and the arguments f,t
    selects the data between the period f and t including f and t
    If the
    f
        from period - valid datetime
    t
        to period - valid datetime, freq = "M")
    index_column
        column to set as index

    Notes
    -----
    DataFrame/Series must have a Datetime Index
    """
    @wraps(function)
    def wrapped(df, index_column = None, *args, **kwargs):
        try:
            df2 = df.loc[kwargs.get("f"): kwargs.get("t")]
        except KeyError:
            raise TypeError("Index not a valid datetime object")
        [kwargs.pop(prop, None) for prop in ["f", "t", "index_column"]]
        return function(df2, *args, **kwargs)
    return wrapped

def frequency(function):
    """
    Groups data by the given frequency
    freq
        A valid pandas DateOffset object or string

    Notes
    -----
    Uses the ffill method to fill nans

    TO DO: add arguments to decorators
    """
    @wraps(function)
    def wrapped(df, *args, **kwargs):
        if kwargs.get("freq") is not None:
            df2 = df.asfreq(kwargs.get("freq"), method = "ffill")
        else:
            df2 = df
        kwargs.pop("freq", None)
        return function(df2, *args, **kwargs)
    return wrapped