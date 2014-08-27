from functools import partial
from pandas import read_csv
from financials.markets.backtest import BackTest
from financials.tools.AdvancedGroup import AdvancedGroup



class HerdInstinct(BackTest):
    """
    The Herd Instinct Portfolio
    """
    def universe(self, symbols, col = "S", **kwargs):
        """
        Read the csv file and select symbols

        col: col to apply filter
        kwargs
        ------
        kwargs to the read_csv function
        """
        df = read_csv(self._source, **kwargs)
        df = df[df.SERIES == "EQ"]
        self._data = df[df[col].isin(symbols)].reset_index()

    def ordering(self):
        """
        Add ordering information to data
        """
        df = self._data
        df["RET"] = df.CLOSE/df.PREVCLOSE
        df["IDRET"] = df.CLOSE/df.OPEN

    def select(self):
        """
        Rank based on Return
        """
        AG = AdvancedGroup(self._data, TS = "TIMESTAMP", S = "SYMBOL")
        self._data = AG.add_feature(AG.d, "rank_it", col = "RET", on = "TIMESTAMP",
                                    by = "SYMBOL", name = "Rank", method = 'first', ascending = False, axis = 0)

    def generate_trades(self):
        """
        Generate trades
        """
        df = self._data


    @property
    def d(self):
        return self._data


