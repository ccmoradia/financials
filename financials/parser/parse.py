import pandas as pd
from operator import add,sub,mul,pow,div,floordiv
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
            return [r]
        except ValueError:
            return df[string]
    else:
        return string  
        
def _is_reduced(sequence):
    # Check whether non-single expression is reduced to a series
    for s in sequence:
        if len(s) > 1:
            if type(s) != pd.core.series.Series:
                return False
    return True
        

class Parser(object):
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
        self._chars = ["+", "-", "*", "/", ">", "<", "=", "&", "|"]
        self._d = {'+': add, '-': sub, '*': mul, '**': pow, '/': div,
                   '//': floordiv, '<': lt, '<=': le, '==': eq, '!=': ne,
                   '>': gt, '>=': ge, '&': and_, '|': or_}
                   
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


    def split_tokens(self,expression = None):
        # Split the tokens for evaluation  
        expression = self._get_expression(expression)
        tokens = self.tokenize(expression) 
        parsed = []
        temp = []
        for tok in tokens:
            if len(temp) == 3:
                parsed.append(temp)
                temp = []
                temp.append(tok)
            elif len(temp) == 1 and temp[0] in self._d.keys():
                parsed.append(temp)
                temp = []
                temp.append(tok)
            else:
                temp.append(tok)
        parsed.append(temp)        
        return parsed
            
  
    def evaluate(self,expression = None):
        # evaluate the expression        
        expression = self._get_expression(expression)
        tokens = self.split_tokens(self.tokenize(expression))
        
        def evl(x):
            if len(x) == 3:
                a = _convert(self._df, x[0])
                b = _convert(self._df, x[2])
                return self._d[x[1]](a,b)
            elif len(x) == 1 and x[0] in self._d.keys():
                return x
            else:
                return _convert(self._df,x[0])
                
        parsed_tokens = tokens[:]
                
        from time import time
        TIME = time()
        
        while _is_reduced(parsed_tokens) == False:
            parsed_tokens = [evl(t) for t in parsed_tokens][:]
            if time() > TIME + 10:
                print "Timeout error - Too much involved in the program"
                break
                 
        for (i,tok) in enumerate(parsed_tokens):
            if type(tok) == list:
                tok = tok[0]
                parsed_tokens[i] = tok                   
                if tok in self._d.keys():
                    a = self._d[tok](parsed_tokens[i-1], parsed_tokens[i+1])
                    parsed_tokens[i+1] = a           
                    
        return parsed_tokens
