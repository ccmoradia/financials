# General utilities

def charges(basic = 1, *args, **kwargs):
    """
    Calculate charges based on the given structure

    args: Cost structure in the given format

    kwargs:
    =======

    percent: Boolean/default True
        If False, numbers aren't converted to percentages


    Format
    ======
    Cost
    Case insensitive

    Lets start with a straight forward case
    >>> charges(100, ['tax', 'basic', 10])
    110.0

    >>> charges(100, ['tax1', 'basic', 10], ['tax2', 'basic', 15])
    125.0

    If you want to subtract something, precede it with a negative sign
    >>> charges(100, ['discount', 'basic', -15])
    85.0

    For charges to accumulate all previous values,
    use acc as the second argument

    >>> charges(100, ['tax1', 'basic', 10], ['tax2', 'acc', 15])
    126.5

    charges is case insensitive as all keys are converted to lower case
    >>> charges(100, ['TAX', 'Basic', 10])
    110.0

    charges accumulates values if the first argument is repeated

    >>> charges(100, ['tax', 'basic', 10], ['commission', 'basic', 20], ['tax', 'acc', 5])
    136.5
    """

    p = 0.01
    result = {}
    result['basic'] = basic
    for (a,b,c) in args:

        if b == 'acc':
            if result.get(a.lower()):
                result[a.lower()] = result[a.lower()] + sum(result.values()) * c * p
            else:
                result[a.lower()] = sum(result.values()) * c * p
        else:
            if result.get(a.lower()):
                result[a.lower()] = result[a.lower()] + result[b.lower()] * c * p
            else:
                result[a.lower()] = result[b.lower()] * c * p
    return sum(result.values())


def profit(O,H,L,C, BuyAt = 0., SellAt = 0., percent = "infer",
           entry = "infer", OPEN = False, digits = 4):
    """
    Calculate the profit of a trade based on OHLC Prices
    O
        Open price of the stock
    H
        High price of the stock
    L
        Low price of the stock
    C
        Close price of the stock
    BuyAt
        Price to BuyAt as a percentage from Open Price or the price
    SellAt
        Price to SellAt as a percentage from Open Price or the price
    percent
        Whether to consider the BuyAt and SellAt as percentages
        True to consider all values as strict percentages
        False to consider all values as strict prices
    entry
        The entry position of the trade
        Allowed values
        "B" = Buy
        "S" - Sell
        "R" - A random buy or sell
        a number between 0 and 1 - to select buy or sell probabilistically
    OPEN
        whether to include or discard trades when High or Low margins
        equal the open price
    digits
        precision of the result in number of digits
    >>> profit(100, 103, 98, 102)
    0.02
    >>> profit(100, 103, 98, 102, BuyAt = 0.04)
    0.0
    >>> profit(100, 103, 98, 102, BuyAt = 0.01, SellAt = 0.03)
    0.0198
    >>> profit(100, 103, 98, 102, SellAt = 0.04)
    0.0
    >>> profit(100, 103, 98, 102, BuyAt = 0.01, SellAt = 0.04)
    0.0099
    >>> profit(100, 103, 98, 102, BuyAt = -0.01)
    0.0303
    """
    import random
    E = entry
    if E == "infer":
        if BuyAt != 0:
            E = "B"
        elif SellAt != 0:
            E = "S"
        else:
            E = "B"
    if E == "R":
        E = random.choice(("B", "S"))
    elif isinstance(E, (int, float)):
        E = "B" if random.random() > E else "S"
    else:
        pass

    inrange = lambda x: True if x <= H and x >=L and not \
    (True if (x == H or x == L) and OPEN else False) else False

    if E == "B":
        BUY = BuyAt if percent is False or BuyAt > 1 else O * (1 + BuyAt)
    else:
        if BuyAt == 0:
            BUY = C
        else:
            BUY = BuyAt if percent is False or BuyAt > 1 else O * (1 + BuyAt)

    if E == "S":
        SELL = SellAt if percent is False or SellAt > 1 else O * (1 + SellAt)
    else:
        if SellAt == 0:
            SELL = C
        else:
            SELL = SellAt if percent is False or SellAt > 1 else O * (1 + SellAt)


    if inrange(BUY) and inrange(SELL):
        P = SELL - BUY + 0.0
    elif inrange(BUY) and not inrange(SELL):
        P = C - BUY + 0.0
        E = "B"
    elif not inrange(BUY) and inrange(SELL):
        P = SELL - C + 0.0
        E = "S"
    else:
        P = 0.0
    # print BUY,SELL,P,E
    return round(P/BUY, digits) if E == "B" else round(P/SELL, digits)

def build_index(from_date, to_date, constituents, include, exclude):
    """
    Build an index from the list of constituents

    from_date
        Start date of the index
    to_date
        End date of the index
    constituents
        Constituents of the index to begin with
    include
        constituents to be included as a dataframe with datetime index
    exclude
        constituents to be removed as a dataframe with datetime index
    >>> from pandas import DataFrame, DatetimeIndex, Series
    >>> from datetime import datetime
    >>> BI = build_index("2014-01-01", "2014-01-03", ["A", "B"], \
        include = DataFrame(["C"], index = DatetimeIndex(["2014-01-02"])),\
        exclude = DataFrame(["A"], index = DatetimeIndex(["2014-01-02"])))
    >>> all(BI == Series(data = ['A', 'B', 'C', 'B', 'C', 'B'], \
        index = [datetime(2014,1,1), datetime(2014,1,1), datetime(2014,1,2), \
        datetime(2014,1,2), datetime(2014,1,3), datetime(2014,1,3)]))
    True
    """
    from itertools import repeat, chain
    from numpy import array
    from pandas import date_range, Series
    index = {}
    dates = date_range(from_date, to_date)
    constituents = set(constituents)
    for d in dates:
        if d in include.index:
            for i in include.ix[d].values.ravel():
                constituents.add(i)
        if d in exclude.index:
            for i in exclude.ix[d].values.ravel():
                constituents.remove(i)
        index[d] = list(constituents)
    a = [zip(repeat(k, len(v)), v) for k,v in index.iteritems()]
    b = array(list(chain(*a)))
    return Series(data = b[:,1], index = b[:, 0]).sort_index()