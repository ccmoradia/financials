import sys
import unittest
from financials.accounting.cash import Cash

def test_initialize():
    cash = Cash()
    assert cash.balance == 0
    cash = Cash(10000)
    assert cash.balance == 10000    

def test_transactions():
    cash = Cash(10000)
    cash.add(10000)
    cash.add(-2000) # The negative sign has no effect
    assert cash.balance == 22000
    cash.wd(5000)
    cash.wd(-5000) # Again, this has no effect
    assert cash.balance == 12000
    
class TestCash(unittest.TestCase):
    cash = Cash(10000, TS = "2014-01-01")
    assert cash.balance == 10000
        
    def add_cash(self):
        receipts = [
                    (5000, "2014-01-01", "Salary"),
                    (6000, "2014-02-06", "Lottery"),
                    (5000, "2014-02-10", "Salary"),
                    (5000, "2014-04-10", "Salary"),
                    (3000, "2014-05-06", "Debt")
                    ]
        [self.cash.add(A = a, TS = t, I = i) for (a,t,i) in receipts]
        
    def withdraw_cash(self):
        payments = [
                    (1000, "2014-01-10", "Grocery"),
                    (1000, "2014-01-17", "Party"),
                    (5000, "2014-01-20", "Rent"),
                    (1200, "2014-02-10", "Party"),
                    (850, "2014-02-17", "Grocery"),
                    (3100, "2014-03-01", "Medicine"),
                    (600, "2014-03-10", "Grocery"),
                    (600, "2014-03-18", "Party"),
                    (3000, "2014-04-01", "Medicine"),
                    (5000, "2014-04-10", "Rent"),
                    (1000,"2014-04-25", "Grocery"),
                    (800, "2014-04-10", "Grocery")
                    ]
        [self.cash.wd(A = a, TS = t, I = i) for (a,t,i) in payments]
        assert self.cash.balance == 7850  
