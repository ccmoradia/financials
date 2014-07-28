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


def profit(O,H,L,C, BuyAt = 0., SellAt = 0., OrderType = "M"):
    """
    Calculate the profit of a trade
    Open
        Open price of the stock
    High
        High price of the stock
    Low
        Low price of the stock
    Close
        Close price of the stock
    BuyAt
        Price to BuyAt as a percentage from Open Price
    SellAt
        Price to SellAt as a percentage from Open Price
    OrderType
        "M" for market and "L" for Limit
    >>> profit(100, 103, 98, 102)
    0.02
    >>> profit(100, 103, 98, 102, BuyAt = 0.04)
    -0.02
    >>> profit(100, 103, 98, 102, BuyAt = 0.01, SellAt = 0.03)
    0.0198
    >>> profit(100, 103, 98, 102, SellAt = 0.04)
    0.02
    >>> profit(100, 103, 98, 102, BuyAt = 0.01, SellAt = 0.04)
    0.0099
    >>> profit(100, 103, 98, 102, BuyAt = -0.01)
    0.01
    >>> profit(100, 103, 98, 102, BuyAt = -0.01, SellAt = 0.02)
    0.0303
    """
    B = O * (1 + BuyAt)
    S = O * (1 + SellAt)
    R = lambda x,y = 4: round(x,y)
    in_range = lambda x: True if x >=L and x<=H else False
    if BuyAt == 0 and SellAt == 0:
        return R((C - B)/B)
    elif BuyAt == 0:
        if in_range(S):
            return R((S - B)/B)
        else:
            return (R(C - B)/B)
    elif SellAt == 0:
        if in_range(B):
            return R((S - B)/S)
        else:
            return R((S - C)/S)
    else:
        if in_range(B) and in_range(S):
            return R((S - B)/B)
        elif in_range(B):
            return R((C - B)/B)
        elif in_range(S):
            return(R(S - C)/S)
        else:
            return 0
profit(100, 103, 98, 102, BuyAt = -0.01)
