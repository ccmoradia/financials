from financials.markets.Portfolio import Portfolio
import unittest

class TestPortfolio(unittest.TestCase):

    pf = Portfolio()
       
    def test_funds(self):
        # test addition and withdrawal of funds
        self.pf.add_funds(2000)
        self.pf.add_funds(3000)
        self.assertEqual(self.pf.balance(), 5000)
        self.pf.add_funds(-1000)
        self.assertEqual(self.pf.balance(), 6000)
        self.pf.withdraw_funds(1000)
        self.pf.withdraw_funds(1500)
        self.assertEqual(self.pf.balance(), 3500)
        self.pf.add_funds(['2014-01-02',2000])
        self.pf.withdraw_funds(['2014-01-03', 5500])
        self.assertEqual(self.pf.balance(),0)
        self.pf.add_funds(['2014', 1, 10000]) # Test for irregular array shapes
        self.pf.withdraw_funds(['2014', '01', '10', 5000])
        self.assertEqual(self.pf.balance(), 5000)
