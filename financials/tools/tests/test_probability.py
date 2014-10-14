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
        self.prob.add_table(on = "C", by = "B", name = "table", agg = sum)

    def test_add_and_remove_table(self):
        self.prob.add_table(on = "A", by = "B", name = "table2")
        self.prob.add_table(on = "B", by = "A", name = "table3")
        self.assertEqual(sorted(self.prob.get_tables), ["table", "table2", "table3"])
        self.prob.remove_table("table2")
        self.assertEqual(sorted(self.prob.get_tables), ["table", "table3"])
        self.prob.remove_all_tables()
        self.assertEqual(self.prob.get_tables, [])

    def test_values(self):
        print self.prob.add_table(on = "C", by = "B", name = "table")
        assert all(self.prob._tables["table"].values.ravel() == [1/3.0]*3)

    def test_lookup(self):
        result = [x/66.0 for x in [18, 22, 26]]
        assert all(self.prob._tables["table"].values.ravel() == result)
        assert self.prob.lookup("table", "Y").values == 1/3.0
        self.prob.add_table(on = "C", by = ["A", "B"], name = "table2", agg = sum)
        assert self.prob.lookup("table2", ("B", "Y")).values == 1/66.0
        result2 = [x/66.0 for x in [0,4,8]]
        assert all(self.prob.lookup("table2", "A").values.ravel() == result2)