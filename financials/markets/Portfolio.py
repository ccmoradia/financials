from numpy import iterable


class Portfolio(object):
    """
    Portfolio class
    """

    def __init__(self):
        self._funds = []      
   
    def add_funds(self,amount):
        """
        Add funds to this portfolio
        
        Parameters
        ----------
        amount : int/float/tuple
            amount to be funded
        
        If date is required, pass it as a 2-tuple. There can be more values
        in the tuple but only the first and last value is considered, the
        first being the date and the last being the amount.
        """
        if iterable(amount):
            a = list(amount)
            a[-1] = abs(a[-1]) # Force the value to be positive
            self._funds.append(a)
        else:
            self._funds.append(abs(amount))

                
    def withdraw_funds(self,amount):
        """
        withdraw funds to this portfolio
        
        Parameters
        ----------
        amount : int/float/tuple
            amount to be withdrawn
        
        If date is required, pass it as a 2-tuple. There can be more values
        in the tuple but only the first and last value is considered, the
        first being the date and the last being the amount.
        """
        if iterable(amount):
            a = list(amount)
            a[-1] = -abs(a[-1]) # Force the value to be negative
            self._funds.append(a)
        else:
            self._funds.append(-abs(amount))
        
    def balance(self):
        """
        Gets the current funds position
        """  
        return sum([x[-1] if iterable(x) else x for x in self._funds])
        
    def add_trades(self):
        """
        Add trades in the given format        
        """
    
    
        
