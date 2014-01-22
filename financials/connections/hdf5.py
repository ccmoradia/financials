# Connect from and to HDF5 class

import h5py
from numpy import dtype

class HDF5Connection(object):
    """
    Create a HDF5 connection object    
    """
    pass
    
    def __init__(self, filename, **options):
        """
        Open a connection to the HDF5 file
        Create a file if it doesn't exit
        
        filename: string
        **options
        any keyword arguments that could be passed to h5py.File object
        """
        self._f = h5py.File(filename, **options)
        
    def __del__(self):
        # Close the HDF5 file
        self._f.close()  
 
        
    def add_data(self, data, path = 'DATA', dtypes = None, convert_object = True, **kwargs):
        """
        Add data to an existing HDF5 file. Create the file if it doesn't exist
        Objects are converted into strings. Datasets created are limited to the
        maximum shape of 1 billion rows in case of record arrays. Existing datasets
        are assumed to be flexible so that new data can be added.
                
        data: numpy recarray        
        
        path: string/ default DATA
            HDF5 path to write to
            
        dtypes: numpy dtype
            converted to this dtypes when writing to HDF5 file
            
        convert_object: Boolean/ default True
            convert object into strings of size 100. This overrides the dtype option for objects.
            Pass False to preserve the dtypes
            
        kwargs
        =======
        List of arguments that could be passed to HDF5 file object
        
        maxshape: int/default 1000000000
            maximum rows of the datasets     
        
        """
        if kwargs.get('maxshape') is None:
            maxshape = 1000000000
        else:
            maxshape = kwargs['maxshape']
        
        if convert_object:
            dtypes = [(k, dtype('S100') if v == dtype('O') else v) for (k,(v,v1)) in data.dtype.fields.items()]
        else:
            pass            
            
        if dtypes is None:
            pass
        else:
            data = data.astype(dtypes)
        
        f = self._f
        if f.get(path):
            dset = f[path]
            l,_ = data.shape
            d,_ = dset.shape
            dset.resize((l+d,))
            dset[d:] = data
        else:
            dset = f.create_dataset(path, data = data, maxshape = (maxshape,))
        
    def get_data(self, symbols, path = "DATA", **kwargs):
        """
        Get data from a HDF5 file
        
        symbols: list
            symbols to get data
            
        path: string
            HDF5 path to extract data
            
        kwargs
        ======
         
            
        """
        f = self._f
        dset = f[path]
        return dset[dset['SYMBOL'] == symbols]
        

