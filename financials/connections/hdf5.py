# Connect from and to HDF5 class

from tables import open_file

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
