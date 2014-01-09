# -*- coding: utf-8 -*-
"""
Created on Thu Oct 24 06:53:55 2013

@author: Ubermensch

General helper functions
"""

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
    
def dict_to_dataframe(data, rows = "L", cycle = False):
    """
    Creates a data frame from a dictionary with different array lengths
        
    DataFrame is constructed in the following way
    
    * Keys are considered as columns
    * Values are considered as rows. Values can be either scalars or lists/tuples
    * By default, list with the lowest length is considered the size of the
      array (i.e) number of rows and other lists are trimmed to fit in.
      See the rows option below to override this
    * In case the value is scalar, the entire column is assigned the scalar value
    
     data - data dictionary with column names as key and rows as list or tuples     
     
     rows - string/integer, default "L" 
     
            number of rows to be included in the data frame
            
            "L"- rows equal the list with the lowest length. List with higher
            lengths are trimmed
            
            "H"- size of the list with the highest length. List with lower
            lengths are assigned NA
            
            integer - rows equal the number. If number > max(length of any list),
            rows are filled only to the maximum length of the list.
            If number < min(length of any list), rows are trimmed.   
         
     cycle - boolean, default False 
             cycles values to fill in the rows instead of NA. Values are filled
             by columns. If the rows argument is set to L or less than the length
             of any of the list values, then cycle has no effect.
             

    """
    keys = [k for (k,v) in data.items() if type(v) == list or type(v) == tuple]
    length = [len(v) for (k,v) in data.items() if k in keys]
    max_length, min_length = max(length), min(length)
    rows = min(int(rows), max_length) if type(rows) == int else rows
   
    if rows == "L":
        row_length = min_length
    elif rows == "H":
        row_length = max_length
    else:
        row_length = rows
        
    if row_length <= min_length:
        cycle = False
        
   
    df = DataFrame(zeros((row_length, len(data))), columns = data.keys())

    for (k,v) in data.items():
        if k in keys:
            if cycle:
                df[k] = Series((list(v) * int(row_length / len(v)) + list(v)[:row_length % len(v)]))
            else:
                df[k] = Series(v)
        else:
            df[k] = v  
       
    return df
    

def create_dataframe(data,columns):
    """
    Creates a dataframe from given data and columns tuple
    
    data - dataframe
    
    columns - list of 2-tuples containing column name and default values
    
    Note:
    
    If the columns in tuples are in the dataframe, then it's value is used.
    Else the default tuple value is substituted for the entire column
    The order of the columns is the order of the tuples
    
    >>> from numpy import arange
    >>> x = arange(9).reshape(3,3)
    >>> df = DataFrame(x,columns = list("ABC"))
    >>> assert(all(df == create_dataframe(df, [("A",10), ("B",20),("C",30)])))
    >>> df2 = df.copy()
    >>> df2['D'] = 40
    >>> df2['E'] = 50
    >>> assert(all(df2 == create_dataframe(df, [("A",10), ("B",20),("C",30),("D",40),("E",50)])))
    """
    r,c = data.shape
    c = len(columns)
    df = DataFrame(zeros((r,c)),columns = [a for (a,b) in columns])
    for (col,default) in columns:
        if col in data.columns:
            df[col] = data[col]
        else:
            df[col] = default
    return df    

def append_columns(dataframe,columns):
    """
    Append columns to a dataframe
    
    dataframe - initial dataframe
    
    columns - list of 2 tuples containing column name and values.
    If the values are scalar, they are directly assigned.
    If the values are list, then the length of list must match the dataframe
    """
    df = dataframe.copy()     
    for (i,(x,y)) in enumerate(columns):
        if x not in df.columns:
            df.insert(i,x,y)
    return df 
    
def test(x,y):
    """ 
    This is an example for doctest
    >>> 4+3  
    7
    >>> a=5
    >>> b=6
    >>> a+b
    11
    >>> S = 0
    >>> S
    0
    >>> for i in range(1,5):
    ...  S+=i 
    >>> S
    10
    >>> S = S+"M"
    Traceback (most recent call last):
    ...
    TypeError: unsupported operand type(s) for +: 'int' and 'str'
    >>> 10+15 == test(10,15)
    True
    >>> test(6,7)
    13
    >>> range(3)
    [0, 1, 2]
    """
    return x+y
        
        
def get_url(url):
    import urllib2
    headers = {"User-Agent": "Mozilla/5.0", "Accept": "*/*"}
    request = urllib2.Request(url,headers = headers)
    response = urllib2.urlopen(request)
    return response.read()
    
            
            
            
            
        

        
    
    
