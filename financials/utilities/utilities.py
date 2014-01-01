# -*- coding: utf-8 -*-
"""
Created on Tue Nov 26 11:29:08 2013

@author: Administrator
"""
from pandas import DataFrame

def dict_to_list(listdict, keys = None, is_JSON = False, as_dataframe = False):
    """
    Given a list of dict and keys, return the value of keys as a list
    
    listdict : list of dictionaries
        In case the object is a JSON string, pass True to the is_JSON argument           
    keys : list
        keys for which data is to be extracted
        If None, keys in the first item of the list if picked by default
    is_JSON: boolean, default False
        True if the input is a JSON string    
    as_dataframe : boolean, default False
        if True, a pandas dataframe is returned with keys as headers
        
    >>> list_of_dicts = [{"A": 4, "B": 5}, {"A": 40, "B": 50}]
    >>> R = [[4,5],[40,50]]
    >>> R == dict_to_list(list_of_dicts)
    True
    >>> import json
    >>> s = json.dumps(list_of_dicts)
    >>> R == dict_to_list(s, is_JSON = True)
    True
    >>> R = [[4],[40]]
    >>> R == dict_to_list(list_of_dicts, keys = ["A"])
    True
    >>> from pandas import DataFrame
    >>> df = DataFrame(list_of_dicts)
    >>> all(df == dict_to_list(list_of_dicts,as_dataframe = True))
    True
    >>> D = dict_to_list(s, keys = ["B"], is_JSON = True, as_dataframe = True)
    >>> del df["A"]
    >>> all (df == D)
    True
    
    TO DO
        Deal with missing keys
        Deal with missing values
        Deal with error on more than one key
    """
    
    if is_JSON:
        import json
        listdict = json.loads(listdict)
       
    keys = listdict[0].keys() if keys == None else keys 
    result = [[k.get(v) for v in keys] for k in listdict]
    
    if as_dataframe:
        return DataFrame(result, columns = keys)
    else:
        return result
        
        
def aggregate_data(path, **kwargs):
    """
    Given a directory path, aggregate data from csv files into a dataframe 
    
    Data is assumed to be fine. Only csv files are searched
        
    path: string 
        Directory path. Only searches the present directory
        
    **kwargs: Could pass all options to the read_csv function
    """
    import os
    options = kwargs
    data = {}    
    for root,dirs,files in os.walk(path):
        for f in files:
            if f[-3:] == "csv":
                read_csv(os.path.join(root,f), **options)
        break
    return DataFrame(data)    
 
    
def convert_to_number(data):
    """
    convert string to number by removing data
    """
    return [float(x.replace(",", "")) for x in data]
    
def correlation_coef(df,x,y):
    # Correlation co-efficient
    x1 = df[x]
    y1 = df[y]
    from sklearn import linear_model
    x1 = x1[:, newaxis]
    y1 = y1[:, newaxis]
    regr = linear_model.LinearRegression()
    regr.fit(x1,y1)
    return x, y, regr.coef_, regr.intercept_