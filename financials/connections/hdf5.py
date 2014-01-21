# Connect from and to HDF5 class

import h5py

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
        f = h5py.File(filename, **options)

