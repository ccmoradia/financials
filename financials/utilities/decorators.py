# All decorator functions go here

from functools import wraps

def select_period(function):
    """
    Given a Series/DataFrame and the arguments f,t selects the data between
    the period f and t.
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
        df2 = df.loc[kwargs.get("f"): kwargs.get("t")]
        return func(df2, *args, **kwargs)
    return wrapped

def frequency(function):
    """
    Groups data by the given frequency
    freq
        frequency
    """
    @wraps(function)
    def wrapped(df, *args, **kwargs):
        freq = kwargs.get("freq")
        result = func(df2, *args, **kwargs)
        return result.groupby(freq)
    return wrapped