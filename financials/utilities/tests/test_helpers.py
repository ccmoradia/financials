from financials.utilities.helpers import *  
from pandas import DataFrame
from numpy import *
import unittest
 

def isDataFramesEqual(*args):
    # compare whether dataframes are identical
    for (i,df) in enumerate(args[1:]):
        df1 = df.sort_index(axis = 1)
        # FIX ME: quick fix to replace nan with values
        for col in df1.columns:
            if str(df1[col].dtype).startswith("int") or str(df1[col].dtype).startswith("float"):
                df1[col] = nan_to_num(df1[col])
        df2 = args[i].sort_index(axis = 1)
        for col in df2.columns:
            if str(df2[col].dtype).startswith("int") or str(df2[col].dtype).startswith("float"):
                df2[col] = nan_to_num(df2[col])
        try:
            if not all(df1 == df2):
                return False
        except:
            return False
    return True
  
class test_utilties(unittest.TestCase):
    def test_DictToDataFrame(self):
        dct = {'A':range(5), 'B':10, 'C':'Q', 'D': [10,20], 'E': [24,31,42]}
        # Initialize data
        df = DataFrame(range(5), columns = ["A"])
        df['B'] = 10
        df['C'] = "Q"
        df['D'] = Series([10,20])
        df['E'] = Series([24,31,42])
        
        # Run tests     
        assert isDataFramesEqual(df[:2], dict_to_dataframe(dct))
        assert isDataFramesEqual(df, dict_to_dataframe(dct, rows = "H"))
        assert isDataFramesEqual(df[:4], dict_to_dataframe(dct, rows = 4))
        df.loc[[2,3,4],'D'] = [[10,20,10]] # Change data to test cycle
        df.loc[[3,4], 'E'] = [[24,31]]
        assert isDataFramesEqual(df[:2], dict_to_dataframe(dct, cycle = True))
        assert isDataFramesEqual(df, dict_to_dataframe(dct, rows = "H", cycle = True))
        assert isDataFramesEqual(df[:4], dict_to_dataframe(dct, rows = 4, cycle = True))
        # TO DO: Test for all as arrays and all input as scalars, rows integer equal to minimum length
    


