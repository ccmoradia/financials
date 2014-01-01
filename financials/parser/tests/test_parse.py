# -*- coding: utf-8 -*-
"""
Created on Fri Dec 27 19:18:16 2013

@author: Administrator
"""

from parse import Parser
from pandas.io.parsers import read_csv
import unittest

df = read_csv('test_parse.csv')
p = Parser(df)

class TestTokenize(unittest.TestCase):
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

class TestTokenSplit(unittest.TestCase):
    t = p.split_tokens
    # More complex expressions are welcome
    expressions_dict = {
                        "a+b": [['a', '+', 'b']],
                        "a+b>b+c": [['a', '+', 'b'], ['>'], ['b', '+ ', 'c']]
                        }

class TestParser(unittest.TestCase):
    pass

    