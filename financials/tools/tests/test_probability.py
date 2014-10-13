import unittest
from itertools import cycle
from financials.tools.probabilities import *
from pandas import DataFrame

df = DataFrame([(a,b,c) for a,b,c in zip(cycle("ABCD"), cycle("XYZ"),
                range(12))], columns = list("ABC"))


class TestFrequencyTable(unittest.TestCase):
    def test_frequency_table_one(self):
        ft = frequency_table(df, on = "A", by = "B")
        assert all(ft.values.ravel() == [4,4,4])
        assert all(ft.index == list("XYZ"))
        assert all(ft.columns == ["A"])

    def test_frequency_table_two(self):
        ft = frequency_table(df, on = "B", by = "A")
        assert all(ft.values.ravel() == [3,3,3,3])
        assert all(ft.index == list("ABCD"))
        assert all(ft.columns == ["B"])

    def test_agg(self):
        ft = frequency_table(df, on = "C", by = "B", agg = sum)
        assert all(ft.values.ravel() == [18,22,26])


class TestProbability(unittest.TestCase):
    def setUp(self):
        self.prob = Probability(df)
        self.prob.add_table(on = "C", by = "B", name = "table")

    def test_add_table(self):
        print self.prob._tables["table"]
        assert all(self.prob._tables["table"].values.ravel() == [1/3.0]*3)
