import unittest
import datetime

from financials.markets.Portfolio import Portfolio
from pandas.io.parsers import read_csv

class TestPortfolio(unittest.TestCase):

    pf = Portfolio()

    def test_funds(self):
        # test addition and withdrawal of funds
        self.pf.add_funds(2000)
        self.pf.add_funds(3000)
        self.assertEqual(self.pf.cash_balance, 5000)
        self.pf.add_funds(-1000)
        self.assertEqual(self.pf.cash_balance, 6000)
        self.pf.withdraw_funds(1000)
        self.pf.withdraw_funds(1500)
        self.assertEqual(self.pf.cash_balance, 3500)
        self.pf.add_funds(2000, TS = '2014-01-02')
        self.pf.withdraw_funds(5500, TS = '2014-01-03')
        self.assertEqual(self.pf.cash_balance,0)
