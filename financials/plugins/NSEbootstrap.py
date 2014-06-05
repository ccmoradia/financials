import os
import datetime
import zipfile
import tables
import requests
import numpy as np
from pandas import bdate_range, read_csv
          
data_type = np.dtype([
            ("SYMBOL", "S20"),
            ("SERIES", "S4"),
            ("OPEN", np.float64),
            ("HIGH", np.float64),
            ("LOW", np.float64),
            ("CLOSE", np.float64),
            ("LAST", np.float64),
            ("PREV", np.float64),
            ("QTY", np.float64),
            ("VOL", np.float64),
            ("TS", "S16"),
            ("TRADES", np.float64),
            ("ISIN", "S20")
            ])            
   
class BootStrapNSE(object):
    """
    Bootstrap for NSE
    """
    def __init__(self, filename, repository = None, schema = data_type, url = None):
        """
        Initialize the HDF5 database
        
        filename: name of the HDF5 file
        repository: repository to look for zip files
        schema: underlying schema of the data
        url: url to download new data
        """
        self._filename = filename
        self._repository = repository
        self._schema = data_type
        self._url = url
        self._log = []
         
    def _download(self, url):
        """
        Download the specified url
        url: the url to download
        returns True if the url is successfully downloaded 
        otherwise False
        """
        base_url = "http://nseindia.com/content/historical/EQUITIES/"        
        url = base_url + url
        try:
            req = requests.get(url)
            if req.status_code == 200:
                with open(os.path.join(self._repository, url.split("/")[-1]), "wb") as f:
                    f.write(req.content)
                    req.close()
                    return True
            else:
                req.close()
                return False
        except Exception as E:
            self._log.append(("download", url, E.message))
            return False
            
    def _update_database(self, filename):
        """
        update the HDF5 database
        """
        if os.path.exists(self._filename):
            archive = zipfile.ZipFile(filename)
            fn = archive.namelist()[0] # Reads only the first file from archive
            df = read_csv(archive.open(fn))
            # For legacy purpose
            if len(df.columns) < len(self._schema):
                for n in range(len(self._schema) - len(df.columns)):
                    df[str(n)] = np.nan
            dbase = tables.open_file(self._filename, "a")
            table = dbase.root.RAW.bhavcopy # This is hardcoded
            try:
                table.append(df.values[:,:13].tolist()) 
                table.flush()
                dbase.close()
            except Exception as E:
                self._log.append(("_update_database", fn, E.message))
                dbase.close()
        else:
            return "File not found"
        
    def bootstrap(self, build = False):
        """
        Bootstrap with a new HDF5 file
        
        build: Boolean
        If build is True and repository is not None, builds
        the new database from data in the repository
        default: False
        """
        if os.path.exists(self._filename):
            return "File already exists"
        else:
            dbase = tables.open_file(self._filename, "w")
            root = dbase.root
            group = dbase.create_group(root, "RAW")
            table = dbase.create_table(group, "bhavcopy", self._schema, "NSE Daily Bhav copy of equities market")
            dbase.close()
        if build:
            for root,directory,files in os.walk(self._repository):
                for f in files:                    
                    try:
                        self._update_database(os.path.join(root,f))
                    except Exception as E:
                        self._log.append(("bootstrap", f, E.message))
       
    def update(self, from_date = "2011-01-01", updateDB = True):
        """
        Downloads data, saves in the repository and updates the HDF5 database
        
        from_date: date from which update is to be considered
        updateDB: Boolean
           If True, update the HDF5 database
        """
        if os.path.exists(self._filename):
            dates = bdate_range(from_date, datetime.date.today())
            for t in dates:
                fn = os.path.join(self._repository, "cm" + t.strftime("%d%b%Y").upper() + "bhav.csv.zip")
                if os.path.exists(fn):
                    pass
                else:
                    status = self._download(t.strftime("%Y/%b/").upper() + "cm" + t.strftime("%d%b%Y").upper() + "bhav.csv.zip")
                    if updateDB:
                        if status:
                            self._update_database(fn)        
        else:
            return "File not found"            
            
     @property
     def get_log(self):
        """
        Get the error log
        """
        return self._log
