import tables as table
import numpy as np
import os.path as path
import requests
          
data_type = np.dtype([
            ("SYMBOL", "S20"),
            ("SERIES", "S4"),
            ("OPEN", np.float32),
            ("HIGH", np.float32),
            ("LOW", np.float32),
            ("CLOSE", np.float32),
            ("LAST", np.float32),
            ("PREV", np.float32),
            ("QTY", np.int64),
            ("VOL", np.float64),
            ("TS", "S16"),
            ("TRADES", np.int64),
            ("ISIN", "S20")
            ])
            
class BootStrapNSE(object):
    """
    Bootstrap for NSE
    """
    def __init__(self, filename, url):
        self.filename = filename
        self.url = url
        
    def _isfileExists(self):
        try:
            with open(self.filename) as f:
                pass
            return True
        except IOError:
            return False
         
    def _download(self, url):
        pass
        
    def bootstrap(self):
        pass
        
    def update(self):
        pass
