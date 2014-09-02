class Metrics(self, portfolio):
    """
    Metrics package for a portfolio
    """
    self._pf = portfolio

    def mtm(self, price):
        """
        Calculate the mark to market of the portfolio
        """
        return (self._pf.summary + self._pf.valuation(price))["V"].sum()

    def realized_profit(self):
        """
        Calculated the realized profit
        """
        return self.unrealized_profit + self.mtm

    def unrealized_profit(self, price):
        """
        Calculate the unrealized profit
        price
            A dataframe containing the present prices
        """
        return pf.valuation.V.sum()

    def profit(self):
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

    def mean(self, by = "TS"):
        """
        Calculate the mean return
        by
            Metric by which the return is to be calculated

        """
        pass

    def std(self, by = "TS"):
        """
        Calculate the standard deviation
        """
        pass

    def sharpe(self, by = "TS"):
        """
        Calculate the Sharpe Ratio
        """
        return self.mean(by = by)/self.std(by = by)

    def ROC(self):
        """
        Calculate the Return on Capital
        """
        df = self._pf.cash_ledger()
        capital = df[df.I == "Capital"].A.sum() + 0.0
        return self.profit/capital