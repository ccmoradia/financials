import numpy as np
from pandas import DataFrame
from collections import Iterable

def frequency_table(dataframe, on, by, agg = 'size', stackby = None, fillNaN = True, fillvalue = 0, aggfunc = {}):
    """
    Calculate a frequency distribution table for a discrete distribution
    
    dataframe:
        a pandas dataframe object
    
    on: column for which frequency distribution table is to be calculated
    
    by: columns by which the table is to be aggregated
    
    agg: {'size', 'sum'}
        aggregation function to used
        size: counts the number of occurences
        sum: sums the number of occurences
        
    stackby:
        colums by which the results are to be stacked
        
    fillNaN:
        fill Nan values. Default True
        
    fillvalue:
        value to fill for Nan values
        
    aggfunc:
        list of function for each of the on variables    
    """
    grouped = dataframe.groupby(by, sort = False)
    func_dict = {k: aggfunc[k] if aggfunc.get(k) is not None else agg for k in on}
    grp = grouped.aggregate(func_dict)
    
    if stackby is not None:
        grp = grp.unstack(stackby)
        if fillNaN:
            grp.fillna(fillvalue, inplace = True)
            
    return grp
