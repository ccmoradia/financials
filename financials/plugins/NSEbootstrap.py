import tables as table
import numpy as np
import os
import requests
import datetime
from pandas import bdate_range
          
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
            
patt = cm01APR2011bhav.csv.zip
%d%b%Y
     
class BootStrapNSE(object):
    """
    Bootstrap for NSE
    """
    def __init__(self, filename, repository, schema = data_type, url = None):
        self._filename = filename
        self._repository = repository
        self._schema = data_type
        self._url = url
        sel._log= []
         
    def _download(self, url):
        base_url = ""
        url = base_url + url
        try:
            requests.get(url)
            # save this file locally
        except Exception as E:
            self._log.append((url, E.message))
            
    def _update_database(self):
        """
        update the HDF5 database
        """
        if os.path.exists(self._filename):
            dbase = tables.open_file(self._filename, "w")
            table = dbase.root.RAW.bhavcopy
            dbase.close()
        else:
            return "File not found"
        
    def bootstrap(self):
        if os.path.exists(self._filename):
            pass
        else:
            dbase = tables.open_file(self._filename, "w")
            root = dbase.root
            group = dbase.create_group(root, "RAW")
            table = dbase.create_table(group, "bhavcopy", self._schema, "NSE Daily Bhav copy of equities market")
            dbase.close()            
        
    def update(self, from_date = "2011-01-01"):
        if os.path.exists(self._filename):
            dates = bdate_range(from_date, datetime.date.today())
            for t in dates:
                fn = os.path.join(self._repository, "cm" + t.strftime("%d%b%Y").upper() + "bhav.csv.zip")
                if os.path.exists(fn):
                    pass
                else:
                    self._download()               
        else:
            return "File not found"
