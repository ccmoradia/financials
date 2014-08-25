def rank_it(df, col, on, by, name = "name", **options):
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
    df = df.set_index([on, by])
    df2 = df.unstack(level = on)
    df[name] = df2.xs(col, axis = 1, level = 0).rank(**options).unstack(by)
    return df.reset_index()

def lag_it(df, col, on, by, lag):
    """
    Adds a time lag to the data

    col: column for which lag is to be added

    lag: int
        Time lag to add
    """
    df = df.set_index([on, by])
    df2 = df.unstack(level = on)
    df[name] = df2.xs(col, axis = 1, level = 0).shift(lag).unstack(by)
    return df.reset_index()