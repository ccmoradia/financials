from pandas import *
from numpy import array, zeros
def stoploss(data,percentage,price_column,order_column,**kwargs):
    """
    Given order data and a percentage, create a stop loss order
    
    data - DataFrame containing order information
    
    percentage - the percentage of stop loss. Provide a list in case of different
    percentages for different orders. Given a numpy array, the length of the list
    must match with the number of orders. Also, the list must be sorted to
    match the orders
    
    price_column - column that contains price on which the stop loss percentage
    is calculated
    
    order_column - column that contains the order type BUY/SELL. If orders have
    different codes other than BUY/SELL, use kwargs    
    
    
    **kwargs**    
    
    Pair - list - keyword for BUY,SELL
    
    ORDERCODE_COL - string - column that contains the order code
    
    STOPLOSS_CODE - string - code for the Stop Loss order to be filled up
                             in ORDERTYPE_COL
     
    Notes:
    Any value that matches a DataFrame Column can be given as an argument to
    kwargs. Given a column name as key and a matching value, the default
    behavior of this function is to replace the entire column with the given
    value.    
    
    StopLoss calculation
     * Long orders = price * (1 + percentage)
     * Short orders = price * (1 - percentage)
    
    >>> df = DataFrame([list("ABCD"), list("WXYZ"),range(1,5),["BUY","SELL","BUY","SELL"]]).transpose()
    >>> df.columns = ["Symbol", "Remarks", "Price", "OrderType"]
    >>> df2 = df.copy()
    >>> df2['Price'] = [0.99,2.02,0.97,4.04]
    >>> df2['OrderType'] = ["SELL", "BUY", "SELL", "BUY"]
    >>> all(df2 == stoploss(df,1,"Price","OrderType"))
    True
    >>> all(df2 == stoploss(df,array([1,1,1,1]),"Price","OrderType"))
    True
    >>> df["OrderType"] = ["B", "S", "B", "S"]
    >>> df2["OrderType"] = ["S", "B", "S", "B"]
    >>> all(df2 == stoploss(df,1,"Price","OrderType", Pair = ["B", "S"]))
    True
    
    """
    if kwargs.get("Pair"):
        Pair = kwargs["Pair"]
        s = Series({Pair[0]:Pair[1], Pair[1]:Pair[0]})
    else:
        s = Series({"BUY": "SELL", "SELL": "BUY"})     
    p = percentage * 0.01
    SL = [price *(1-p) if x==s[1] else price*(1+p) for (price,x) in zip(data[price_column], data[order_column])]
    df = data.copy()
    df[price_column] = SL
    df[order_column] = df[order_column].map(s)
    return df
