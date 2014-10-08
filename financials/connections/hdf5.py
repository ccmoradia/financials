# Connect from and to HDF5 class

from collections import Iterable
from tables import open_file, NodeError
from pandas import DataFrame
from pandas.tslib import Timestamp

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
        self._f = open_file(filename, **options)

    def __del__(self):
        # Close the HDF5 file
        self._f.close()

    @property
    def f(self):
        """
        Return the HDF5 file handle
        """
        return self._f

    def _build_condition(self, condition, linker = "&"):
        """
        Given a dictionary, convert it to the pytables condition format
        condition
            a dictionary with keys as column names and values as 2 tuples
            with the first element being the operator and the second element
            being a list of values to be found in the column
        linker
            link expression that matches all the conditions. usually | or &
            In case of different linkers for each functions, pass a list
            of size that is 1 less than dict
        """
        expr = []
        for k,v in condition.iteritems():
            a,b = v
            b = b if isinstance(b, Iterable) else [b]
            b = ["'" + str(x) + "'" if not isinstance(x, (int, float))
                 else x for x in b]
            expr.append("(" + '|'.join(["(" + k + a + str(x) + ")" for x in b]) + ")")
        builder = expr[0]
        if len(linker) > 1:
            if len(linker) != (len(condition) - 1):
                raise ValueError("Length of linker must be 1 less than \
length of condition")
            else:
                for string, link in zip(expr[1:], linker):
                    builder = builder + link + string
        else:
            for string in expr[1:]:
                builder = builder + linker + string
        return builder


    def search_cols(self, column, path = "/", find_all = False, \
    case_insensitive = False):
        """
        Search a column among all datasets
        column
            column to search
        path
            path to search for
        find_all
            If True searches the whole object tree and returns all occurences
            If False returns the first occurence
        case_insensitive
            If True, a case insensitive search is made
        """
        result = []
        for node in self._f.walk_nodes(path):
            try:
                if case_insensitive:
                    column = column.lower()
                    column_names = [x.lower() for x in node.colnames]
                else:
                    column_names = node.colnames
                if column in column_names:
                    result.append(node._v_pathname)
                    if find_all is not True:
                        break
            except:
                pass
        return result

    def search_attrs(self, attr, path = "/", find_all = True, \
    case_insensitive = False):
        """
        Search attributes for a name
        returns a dict with path as keys and attribute names as values
        """
        result = {}
        for node in self._f.walk_nodes(path):
            for attrs in self._f.get_node(node)._v_attrs._f_list("all"):
                if case_insensitive:
                    attr = attr.lower()
                    myattr = str(self._f.get_node_attr(node, attrs)).lower()
                else:
                    myattr = self._f.get_node_attr(node, attrs)
                if attr == myattr:
                    result[node._v_pathname] = attrs
            if (find_all is not True) and len(result) > 0:
                return result
        return result

    def extract_data(self, path, condition, cols = None, ts_col = None, \
    from_date = None, to_date = None):
        """
        Extract data from a compound datatype
        path
            path to the data
        condition
            condition to search for
        cols
            columns to return
        ts_col
            column containing datetime
        from_date

        """
        data = self._f.get_node(path)
        cond = self._build_condition(condition = condition)
        if ts_col is not None:
            if (from_date is None) or (to_date is None):
                raise ValueError("Dates not matching")
            f,t = Timestamp(from_date).value, Timestamp(to_date).value
            cond = cond + "&" + self._build_condition({ts_col: (">=", f)})
            cond = cond + "&" + self._build_condition({ts_col: ("<=", t)})
        if cols is None:
            cols = data.colnames
        df = [[x[col] for col in cols] for x in data.where(cond)]
        return DataFrame(df, columns = cols)

    def split(self, path, newpath, name, column, condition = None, \
    values = None, overwrite_tables = False):
        """
        Split data based on a column
        path
            existing path to data
        newpath
            path to create data
        name
            name of the group
        condition
            condition to filter other columns
        column
            column by which data is to be split
        values
            values for which data is to be split
            If None all values are split
        overwrite_tables
            If True already existing table is overwritten

        Split works only with the equality operator. So it can work only
        with discrete values
        """
        data = self._f.get_node(path)
        description = data.coldescrs
        cond = self._build_condition(condition)
        try:
            group = self._f.create_group(newpath, name = name)
        except NodeError:
            group = self._f.get_node(newpath)

        if values is None:
            values = unique(data.read(field = column)) # This could be horribly slow
        for val in values:
            d = data.where(cond)
            try:
                d = self._f.create_table(group, name = val, description = description)
            except NodeError:
                if overwrite_tables:
                    self._f.remove_node(group, name = val)
                    d = self._f.create_table(group, name = val, description = description)
                else:
                    raise NodeError("Table seem to exist. Try overwriting them \
with the overwrite_tables option")
            c = cond + " &" + self._build_condition({column: ("==", [val])})
            data.append_where(d, condition = c)
            self._f.flush()

    def merge(self, src, dst, on = None, src_condition = None, \
    dst_condition = None, **kwargs):
        """
        merge two tables based on common columns
        src
            source table
        dst
            destination table
        on
            columns to merge on
        src_condition
            condition to be applied on source table
        dst_condition
            condition to be applied on destination table
        kwargs
            kwargs to pandas merge function
        """
        if src_condition is None:
            df1 = DataFrame(self._f.get_node(src).read())
        else:
            df1 = self.extract_data(src, condition = src_condition)

        if dst_condition is None:
            df2 = DataFrame(self._f.get_node(dest).read())
        else:
            df2 = self.extract_data(dst, condition = dst_condition)

        return merge(df1, df2, on = on, **kwargs)