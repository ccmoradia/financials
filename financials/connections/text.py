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
        
    def decompress(self, archive_name):
        """
        Extract file from archive
        
        archive_name: string
            path to the archive
        """
        import zipfile
        archive = zipfile.Zipfile(archive_name)
        for f in archive.namelist()[1:]:
            yield (archive.open(f))       
    
        
    def aggregate_data(self, fns = False, fnf = None, handle_compression = True, **kwargs):
        """
        Given a directory path, aggregate data from csv files into a dataframe 
        
        fns (filename as symbol): Boolean/ default False
            adds the filename as the symbol column in the dataframe
            
        fnf (filename filter): Boolean function
            filter to be applied to a filename for further processing
            If filter is True, the file is processed else its not processed.
            The default filter is to process files that end with .csv extension.
            
        handle_compression: Boolean/ default True
            automatically extracts zip,gz,bz2 files
            In case of zip archive with multiple files, extracts all files
            with the csv extension
        
        kwargs: Could pass all options to the pandas read_csv function
        """
        df = DataFrame()
        if fnf == None:
            fnf = lambda x: True if '.csv' in x else False 
            
        def read_file(file_to_read, **kwargs):
            # TO DO: Move this code outside this function
            if fnf(fn):
                d = read_csv(file_to_read, **kwargs)
                if fns:
                    d['SYMBOL'] = file_to_read[:-4]
            return d        
                           
        
        for root,dirs,files in os.walk(self._dir):
            for f in files:
                fp = os.path.join(root, f)
                _, ext = os.path.splitext(fp)
                # TO DO: Move this code to the decompress function
                if handle_compression:
                    if ext == '.zip':
                        filelist = self.decompress(fp)
                        for fl in  filelist:
                            df = concat([df, read_file(fl, **kwargs)])
                    elif ext == '.gz':
                        kwargs['compression'] = '.gz'
                        df = concat([df, read_file(fp, **kwargs)])                        
                    elif ext == '.bz2'
                        df = concat([df, read_file(fp, **kwargs)])
                    else:
                        pass
        self._df  = df                
         
    def get_data(self, symbols, **kwargs):
        """
        Get data for the required symbols
        
        symbols: string/list
            list of symbols
            TO DO: list of symbols to be implemented
        """
        df = self._df
        return df[df['SYMBOL'] == symbols]
