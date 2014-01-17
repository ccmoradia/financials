import pandas as pd
from operator import add,sub,mul,pow,div,floordiv,mod
from operator import lt,le,eq,ne,gt,ge,and_,or_

def _check_char(string, chars):
    for s in string:
        if s in chars:
            return True
    return False   

def _check_type(string):
    # check whether the character could be converted into float
    # return True if it could be converted and False otherwise
    try:
        float(string)
        return True
    except ValueError:
        return False
        
def _convert(df, string):
    if type(string) in (str,float,int):
        try:
            r = float(string)
            return r
        except ValueError:
            return df[string] if string in df.columns else string
    else:
        return string  
        
def _is_reduced(sequence):
    # Check whether non-single expression is reduced to a series
    for s in sequence:
        if len(s) > 1:
            if type(s) != pd.core.series.Series:
                return False
    return True
        

class SimpleParser(object):
    """
    A Simple Parser class for doing operations on
    dataframes
    """
    def __init__(self,dataframe = pd.DataFrame(), expression=None):
        """
        dataframe - a pandas DataFrame
        expression - an expression string without brackets
        """
        self._df = dataframe
        self._expression = expression
        self._chars = ["+", "-", "*", "/", ">", "<", "=", "&", "|", "%"]
        self._d = {'+': add, '-': sub, '*': mul, '**': pow, '/': div,
                   '//': floordiv, '<': lt, '<=': le, '==': eq, '!=': ne,
                   '>': gt, '>=': ge, '&': and_, '|': or_, '%': mod}
                   
    def _get_expression(self, expression = None):
        # Assign the default expression if there is None
        if expression is None:
            return self._expression
        else:
            return expression               
        
        
    def dataframe(self, dataframe):
        """
        Add/replace a dataframe
        """
        self._df = dataframe

    def tokenize(self, expression = None):
        # Split the expression into tokens
        expression = self._get_expression(expression)        
        tokens = []
        buffers = '' 
        for s in expression:
            if s in self._chars:
                if buffers == '':
                    buffers = s
                elif _check_char(buffers, self._chars) is True:
                    buffers = buffers + s
                else:
                    tokens.append(buffers)
                    buffers = s
            else:
                if buffers == '':
                    buffers = s
                elif _check_char(buffers, self._chars) is True:
                    tokens.append(buffers)
                    buffers = s
                else:
                    buffers = buffers + s
        tokens.append(buffers)
        return [t.strip() for t in tokens]  
  
    def evaluate(self,expression = None):
        # evaluate the expression        
        expression = self._get_expression(expression)
        tokens = self.tokenize(expression)
        result = self._df[tokens[0]]
        
        for (i,op) in enumerate(tokens[1::2]):
            c = _convert(self._df, tokens[(i+1)*2])
            if op in ['<', '>', '<=', '>=', '==', '!=']:
                result = result[self._d[op](result,c)]
            else:
                result = self._d[op](result,c)
        return result
        
def parse(df, expression = None):
    # Helper function for the Parser Class
    p = SimpleParser(df, expression)
    return p.evaluate()
