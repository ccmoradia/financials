class Metrics(self, portfolio):
    """
    Metrics package for a portfolio
    """
    self._pf = portfolio

    def mean(self, f = None):
        pass

    def std(self):
        pass

    def sharpe(self):
        return self.mean()/self.std()