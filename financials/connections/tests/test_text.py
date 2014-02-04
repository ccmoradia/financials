import os
from pandas import DataFrame
from pandas.io.parsers import read_csv
import unittest
from financials.connections.text import TextConnection

import os
tp = 'financials/connections/tests'
rp = 'financials/connections/tests/result'


class TestTextConnection(unittest.TestCase):

    def test_aggregate_data(self):
        pth = os.path.join(os.path.curdir, tp, 'data6')
        res = os.path.join(os.path.curdir, rp, 'result_eod.csv')
        t = TextConnection(pth)
        t.aggregate_data()
        print t._df, pth
        df = read_csv(res)
        self.assertEqual(all(df.sort_index(axis = 1) == t._df.sort_index(axis = 1)), True) 
        
    def test_zip(self):
        pth = os.path.join(os.path.curdir, tp, 'data3')
        res = os.path.join(os.path.curdir, rp, 'result_all.csv')
        t = TextConnection(pth)
        t.aggregate_data(fns = True)
        df = read_csv(res)
        self.assertEqual(all(df.sort_index(axis = 1) == t._df.sort_index(axis = 1)), True) 
        
    def test_compression(self):
        pth = os.path.join(os.path.curdir, tp, 'data5')
        res = os.path.join(os.path.curdir, rp, 'result_all.csv')
        t = TextConnection(pth)
        t.aggregate_data(fns = True)
        df = read_csv(res)
        self.assertEqual(all(df.sort_index(axis = 1) == t._df.sort_index(axis = 1)), True)        
 
    def test_fnf(self):
        pth = os.path.join(os.path.curdir, tp, 'data1')
        res = os.path.join(os.path.curdir, rp, 'result_filter.csv')
        flt = lambda x: True if x[:-4] in ['AAPL', 'ARIA', 'LMT', 'MDLZ'] else False
        t = TextConnection(pth)
        t.aggregate_data(fns = True, fnf = flt)
        df = read_csv(res)
        self.assertEqual(all(df.sort_index(axis = 1) == t._df.sort_index(axis = 1)), True) 
        
    def test_after_read(self):
        pth = os.path.join(os.path.curdir, tp, 'data5')
        res = os.path.join(os.path.curdir, rp, 'result_all.csv')
        df = read_csv(res)
        df['add_col'] = df['high'] + df['low']
        def f(x):
            x['add_col'] = x['high'] + x['low']
            return x
        t = TextConnection(pth)
        t.aggregate_data(fns = True, after_read = f)
        self.assertEqual(all(df.sort_index(axis = 1) == t._df.sort_index(axis = 1)), True)
        
    def other_test(self):
        # TO DO: test for no compression
        # TO DO: test for reset_index
        pass
                
