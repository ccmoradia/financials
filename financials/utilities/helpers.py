# -*- coding: utf-8 -*-
"""
Created on Thu Oct 24 06:53:55 2013

@author: Ubermensch

General helper functions
"""

from pandas import DataFrame, Series
from numpy import array, zeros

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

