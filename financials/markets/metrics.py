class Metrics(object):
    """
    Metrics package for a portfolio
    """
    def __init__(self, portfolio):
        """
        Initialize metrics with a portfolio
        """
        self._pf = portfolio

    def mtm(self, price, **kwargs):
        """
        Calculate the mark to market of the portfolio
        """
        return self._pf.valuation(price).V.sum() + self._pf.summary.V.sum()

    def realized_profit(self, **kwargs):
        """
        Calculated the realized profit
        """
        sale_qty = self._pf.trades.groupby(["S", "M"]).Q.sum().xs("SELL", level = "M")
        price_diff = self._pf.price().SELL - self._pf.price().BUY
        return (price_diff * -sale_qty).sum()

    def unrealized_profit(self, price, **kwargs):
        """
        Calculate the unrealized profit
        price
            A dataframe containing the present prices
        """
        return self.mtm(price) - self.realized_profit()

    def profit(self, **kwargs):
        """
        Calculate the profit of the portfolio
        mode:
        'realized' - calculate only on completed trades
        'unrealized' - calculate only on holdings
        'indicative' - calculate both realized and unrealized
        """
        df = self._pf.cash_ledger()
        expenses = df[df.I == "Expense"].A.sum()
        return self.mtm + expenses

    def mean(self, by = "TS", **kwargs):
        """
        Calculate the mean return
        by
            Metric by which the return is to be calculated

        """
        pass

    def std(self, by = "TS", **kwargs):
        """
        Calculate the standard deviation
        """
        pass

    def sharpe(self, by = "TS", **kwargs):
        """
        Calculate the Sharpe Ratio
        """
        return self.mean(by = by)/self.std(by = by)

    def ROC(self, **kwargs):
        """
        Calculate the Return on Capital
        """
        df = self._pf.cash_ledger()
        capital = df[df.I == "Capital"].A.sum() + 0.0
        return self.profit/capital