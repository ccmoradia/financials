# A backtesting framework

from collections import namedtuple

_getarg = lambda x,y: x if x is not None else y

class Strategy(object):
    """
    Implementation of a trading strategy
    """
    def __init__(self, data):
        """
        data: data on which the strategy is to be tested
        """
        self._data = data
        
    def add_entry(self, func):
        """
        Add entry signal
        """
        pass
    
class BackTest(object):
    """
    The Backtesting framework
    """
    def __init__(self, data, from_period, to_period, **kwargs):
        """
        data: data to run the backtest
        
        from_period: start period of the backtest
        
        to_period: end period of the backtest
        
        kwargs
        ======
        Symbol: Symbol column in the dataframe
                str/ default: "Symbol" 
        TS: Timestamp column in the dataframe
                str/default: "TS"
        
        """
        self._data = data
        self._fromperiod = from_period
        self._toperiod = to_period
        self._groups = {}
        self._strategy = {}
        self.symbol = _getarg(kwargs.get("symbol"), "Symbol")
        self.TS = _getarg(kwargs.get("TS"), "TS")
        self.capital = kwargs.get("capital")
        constraints = namedtuple("constraints",
                                [
                                "max_allocation_size", "initial_allocation_size",
                                "reimplement_time", "rebalance_on"
                                ])
        
    def __repr__(self):
        """
        A string representation of the object
        """
        pass
        
    @property
    def d(self):
        """
        Get the data
        """
        return self._data
        
    def set_period(self, from_period = None, to_period = None):
        """
        Set the backtesting period
        """
        self._fromperiod = _getarg(fromperiod, self._fromperiod)
        self._toperiod = _getarg(toperiod, self._toperiod)
        
    def add_group(self, name, items):
        """
        Add a group of stocks
        
        items: list/tuple containing stock symbols
        
        Create groups to test strategies. The symbols in the group
        must be available in the dataframe and must not be the
        same as any of the symbols. These groups are independent
        from strategies
        """
        self._groups[name] = items
        
    def remove_group(self,name):
        """
        Removes a group
        """
        return self._groups.pop(name)
        
    def get_group(self, name):
        """
        Get a group by name
        
        name: name of the group
        """
        return self._groups[name]
        
    @property
    def get_all_groups(self):
        """
        Get all groups
        """
        self._groups
        
        
    def add_strategy(self, name, entry, exit, group = None):
        """
        Add a strategy to the backtest
        
        name: name of the strategy
        
        entry: an entry signal for the strategy / function
        
        exit: exit signal for the strategy / function
        
        group: group to apply the strategy
        """
        group = _getarg(group, "all")
        self._strategy[name] = (entry, exit, group)        
    
    
    def run_backtest(self, from_period, to_period, strategy, group = None, **kwargs):
        """
        Run backtest based on given parameters
            
        from_period: start period of the backtest
        
        to_period: end period of the backtest
        
        strategy: name of the strategy
        
        group: group on which the strategy is to be executed
            list/tuple of stocks or stock groups or a combination of both
        """
        df = self._data.set_index(self.TS).loc[from_period:to_period]
        if group is not None:
            df = df[df[self.Symbol].isin(self.get_group(group))]
        entry, exit, _ = self._strategy[strategy]
        positions = []        
        for symbol in unique(df[self.Symbol]):
            positions.append(entry(df, **kwargs))
            positions.append(exit(df, **kwargs))
        trades = concat(positions, axis = 1)
