# Load files into HDF5 archive
from pandas import *
import zipfile


columns = ["SYMBOL", "SERIES", "OPEN", "HIGH", "LOW", "CLOSE",
           "LAST", "PREVCLOSE", "TOTTRDQTY", "TOTTRDVAL",
           "TIMESTAMP", "TOTALTRADES", "ISIN"]
           
dtypes = [("SYMBOL", "S50"), ("SERIES", "S6"), ("OPEN", "f8"),
          ("HIGH", "f8"), ("LOW", "f8"), ("CLOSE", "f8"),
          ("LAST", "f8"), ("PREVCLOSE", "f8"), ("TOTTRDQTY", "f8"),
          ("TOTTRDVAL", "f8"), ("TIMESTAMP", "S15"),
          ("TOTALTRADES", "f8"), ("ISIN", "S20")]


def zip_to_dataframe(path, filename, headers = columns):
    # path must include the final slash /
    # convert a csv file in zip archive to dataframe
    # headers - default headers to create a dataframe
    with zipfile.ZipFile(path + filename) as z:        
        df = read_csv(z.open(filename[:-4])).drop_duplicates()
        df = df.drop(df[df.SYMBOL == "SYMBOL"].index).iloc[:,:-1]
        return concat([DataFrame(columns = headers), df])

def concat_dataframes(path, files, headers = columns):
    # unzips files, reads csv and joins them into a single dataframe
    # headers - default headers to create a dataframe    
    df = DataFrame(columns = headers) # Empty dataframe with required columns
    return concat([df, concat([zip_to_dataframe(path, f) for f in files])])
    
def convert_dataframe_to_recarray(dataframe):
    # helper functions to convert dataframe to recarray
    # main function is to convert objects into strings
    rec = dataframe.to_records(index = False)
    return rec.astype(dtype = dtypes)

def write_recarray_to_hdf5(recarray, filename, key = "RAW"):
    # write recarray to a HDF5 file. Uses vanilla h5py
    # writes data straight under root
    import h5py
    f = h5py.File(filename)
    if f.get(key):
        dset = f[key]
        # print 'Existing dset shape - ', dset.shape
        l, = recarray.shape
        d, = dset.shape
        dset.resize((l+d,))
        dset[d:] = recarray
        # print 'New dset shape - ', dset.shape        
    else:
        dset = f.create_dataset(key, data = recarray,maxshape = (1000000000,))
    f.close()
    
def run_bootstrap():
    # Bootstrap to load initial data - crappy code
    filelist = read_csv('filelist_2011.csv').values
    filelist = filelist.ravel()
    path = "G:/Projects/finance/NSE/"
    for (y,x) in enumerate(filelist):
        try:
            df = zip_to_dataframe(path, x)
            rec = convert_dataframe_to_recarray(df)
            write_recarray_to_hdf5(rec, 'data.h5','FROM2011')
            # print "Success ", x
        except Exception as inst:
            print y, type(inst), x
            
if __name__ == "__main__":
    run_bootstrap()