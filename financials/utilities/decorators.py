# All decorator functions go here

from functools import wraps

def period(function):
    """
    Given a Series/DataFrame with a datetime index and the arguments f,t
    selects the data between the period f and t including f and t
    f
        from period - valid datetime
    t
        to period - valid datetime

    Notes
    -----
    DataFrame/Series must have a Datetime Index
    """
    @wraps(function)
    def wrapped(df, *args, **kwargs):
        try:
            df2 = df.loc[kwargs.get("f"): kwargs.get("t")]
        except KeyError:
            raise TypeError("Index not a valid datetime object")
        kwargs.pop("f", None)
        kwargs.pop("t", None)
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