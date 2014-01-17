# -*- coding: utf-8 -*-
"""
Created on Fri Dec 27 19:18:16 2013

@author: Administrator
"""

from financials.parser.parse import SimpleParser, parse
from pandas import DataFrame
from pandas.io.parsers import read_csv, ExcelFile
from numpy import array
import unittest


df = DataFrame([[1,'X',10,1.2,'foo'],
                [2,'Y',18,2.4,'bar'],
                [3,'X',9,0.8,'foo'],
                [4,'Z',16,0.38,'qux'],
                [5,'Y',13,0.15,'foo']
                ], columns = ['first', 'second', 'third', 'fourth', 'fifth'])


class TestTokenize(unittest.TestCase):
    p = SimpleParser(df)
    t = p.tokenize
    # More complex expressions are welcome
    expressions_dict = {
                        "a+b": ['a', '+', 'b'],
                        "a==b": ['a', '==', 'b'],
                        "first>=second": ['first', '>=', 'second'],
                        "a*1.05+b*1e4": ['a', '*', '1.05', '+', 'b', '*', '1e4']
                        }
    
    def test_tokenize(self):
        for k,v in self.expressions_dict.items():
            self.assertEqual(self.t(k), v)
            
class TestEvaluate(unittest.TestCase):
    # Each solution corresponds to a sheet in the solutions.xls file
    expressions = {
                "S1": 'first+third',
                "S2": 'first+third*fourth',
                "S3": 'fifth == foo',
                "S4": 'third > 10 + first * fourth',
                "S5": 'first >=3'
                }
                
    solutions = {
                "S1": df['first'] + df['third'],
                "S2": (df['first'] + df['third']) * df['fourth'],
                "S3": df[df['fifth'] == 'foo']['fifth'],
                "S4": (df[df['third'] > 10]['third'] + df['first']) * df['fourth'],
                "S5": df[df['first'] >= 3]['first']
                }
                
    def test_evaluate(self):
        for (k,v) in self.expressions.items():
            self.assertEqual(all(parse(df,v).dropna() == self.solutions[k].dropna()), True, k)
            # Index and na to be tested
