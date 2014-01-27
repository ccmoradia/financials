# Create in memory dataframes for csv, txt files

import os
from pandas.io.parsers import read_csv
from pandas import DataFrame, Panel, concat

class TextConnection(object):
    """
    Text Connection object
    """
    
    def __init__(self, directory):
        """
        Directory where file exists
        
        options - keyword arguments to be passed to read_csv function
        """
        self._dir = directory
        
    def _decompress(self, archive_name):
        """
        Extract file from archive
        Return a 2-tuple containing the file name and the file object
                
        archive_name: string
            path to the archive
        """
        import zipfile
        archive = zipfile.ZipFile(archive_name)
        for f in archive.infolist():
            yield (f.filename, archive.open(f.filename))  
    
        
    def aggregate_data(self, fns = False, fnf = None, after_read = None, handle_compression = True, **kwargs):
        """
        Given a directory path, aggregate data from csv files into a dataframe 
        
        fns (filename as symbol): Boolean/ default False
            adds the filename as the symbol column in the dataframe
            
        fnf (filename filter): Boolean function
            filter to be applied to a filename for further processing
            If filter is True, the file is processed else its not processed.
            The function must result a Boolean value.
            The default filter is to process files that end with .csv extension.
            
        after_read: function/ default None
            function to run after the file is read
            
        handle_compression: Boolean/ default True
            automatically extracts zip,gz,bz2 files
            gz and bz2 files are assumed to contain csv files.
            In case of zip archive with multiple files, extracts all files
            with the csv extension
        
        kwargs: Could pass all options to the pandas read_csv function
        """
        df = DataFrame()
        if fnf == None:
            fnf = lambda x: True if ('.csv' in x) or ('.gz' in x) or ('bz2' in x) else False 
            
        def read_file(file_to_read, symbol, **kwargs):
            # TO DO: Move this code outside this function
            d = DataFrame()
            print file_to_read, symbol
            if fnf(symbol):
                d = read_csv(file_to_read, **kwargs)
                if after_read is None:
                    pass
                else:
                    d = after_read(d)
                if fns:
                    d['SYMBOL'] = symbol[:-4]
            return d       
                           
        
        for root,dirs,files in os.walk(self._dir):
            for f in files:
                fp = os.path.join(root, f)
                _, ext = os.path.splitext(fp)
                # TO DO: Move this code to the decompress function
                if handle_compression:
                    if ext == '.zip':
                        filelist = self._decompress(fp)
                        for (a,fl) in filelist:
                            df = concat([df, read_file(fl, a, **kwargs)])  
                    elif ext == '.gz':
                        options = kwargs.copy()
                        options['compression'] = 'gzip'
                        df = concat([df, read_file(fp, f, **options)])                        
                    elif ext == '.bz2':
                        options = kwargs.copy()
                        options['compression'] = 'bz2'
                        df = concat([df, read_file(fp, f, **options)])
                    elif ext == '.csv':
                        df = concat([df, read_file(fp, f, **kwargs)])
                    else:
                        pass
                else:
                    df = concat([df, read_file(fp, f, **kwargs)])
                       
        self._df  = df.reset_index(drop = True)               
         
    def get_data(self, symbols, **kwargs):
        """
        Get data for the required symbols
        
        symbols: string/list
            list of symbols
            TO DO: list of symbols to be implemented
        """
        df = self._df
        return df[df['SYMBOL'] == symbols]
