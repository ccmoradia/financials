# -*- coding: utf-8 -*-
"""
Created on Thu Oct 24 06:53:55 2013

@author: Ubermensch

General helper functions
"""

from pandas import *
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

