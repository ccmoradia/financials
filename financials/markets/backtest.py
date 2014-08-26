from financials.markets.Portfolio import Portfolio

class BackTest(object):
    """
    A modular backtesting framework
    """
    def __init__(self, source):
        """
        source:
            A valid source
        """
        self._source = source

    def universe(self, func, *args, **kwargs):
        """
        Create a stock universe
        func
            A function to select stocks
        """
        self._data = func(self._source, *args, **kwargs)

    def ordering(self, func, *args, **kwargs):
        """
        An algorithm to rank stocks
        func
            A function to order stocks
        """
        return func(self._data)

    def select(self, func, *args, **kwargs):
        """
        An algorithm to select stocks
        func
            A function to select stocks
        """
        return func(self.ordering())

    def generate_trades(self, positions):
        """
        Create trades based on entry, exit positions
        """
        pass

    def generate_portfolio(self):
        """
        Evaluate the portfolio
        """
        pass

    def run(self, func_list = []):
        """
        Runs the entire backtest in a single step
        func_list
            A list of 3-tuples for each of the 4 functions
            with function name as the first element, arguments as the second
            element and kwargs as the third element
        """
        for func, args, kwargs in func_list:
            func(*args, **kwargs)