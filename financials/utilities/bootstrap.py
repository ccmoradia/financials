"""
Bootstrap to get started
"""
import os
import zipfile
import requests
from tables import open_file, IsDescription, StringCol, BoolCol
from pandas import read_csv, read_json

run = lambda obj: obj() if hasattr(obj, "__call__") else obj



class BootStrap(object):
    def __init__(self, filename, repository, schema = {}):
        """
        Bootstrap with a HDF5 database
        filename
            name of the HDF5 file
            If the file doesn't exist, use createDB to create the file
        repository
            the directory that holds the files
        schemas
            schema as dict/json file
        """
        self._DB = filename
        self._repository = repository
        self._schema = schema
        self._log = []

    def _download(self, url):
        """
        Download the url
        Returns the request content
        else returns False
        """
        url = run(url)
        try:
            req = requests.get(url)
            if req.status_code == 200:
                return req
            else:
                req.close()
                self._log.append(("_download", url, req.status_code))
                return False
        except Exception as E:
            self._log.append(("_download", url, E.message))
            return False

    def _write_to_repository(self, req, path, filename = None):
        """
        Write the content to repository
        returns the filename if file succesfully written
        else false
        req
            A url request object from the _download function
        path
            repository path
        """
        try:
            if req:
                if filename is None:
                    filename = req.url.split("/")[-1]
                elif hasattr(filename, "__call__"):
                    filename = filename()
                else:
                    filename

                pth = os.path.join(path, filename)
                if os.path.exists(pth):
                    self._log.append(("_write_to_repository", path, "File already exists"))
                    return False
                else:
                    with open(pth, "wb") as f:
                        f.write(req.content)
                        req.close()
                        return pth
            else:
                return False
        except Exception as E:
            self._log.append(("_write_to_repository", path, E.message))

    def _upload_to_DB(self, filename, name, n_check = 10, **kwargs):
        """
        Uploads a file to DB
        filename
            filename to upload
        name
            The name of the schema
        n_check
            The number of last files to check whether
            they are already uploaded to DB
        """
        with open_file(self._DB, "r+") as h5file:
            desc = self.get_schema(name)
            sync = h5file.get_node(h5file.root._SYNC, desc["path"]) \
                   [-n_check:]["filename"]
        if filename.split("/")[-1] in sync:
            self._log.append(("_upload_to_DB", filename, "File already uploaded to DB"))
            return False

        if self.get_schema(name)["upload"] is None:
            _,ext = os.path.splitext(filename)
            if ext in [".gzip", ".bz2"]:
                df = read_csv(filename, compression = ext)
            elif ext == ".zip":
                z = zipfile.ZipFile(filename)
                df = read_csv(z.open(z.namelist()[0]))
            else:
                pass
            self.default_upload(df, name)
        else:
            self.get_schema(name)["upload"](filename = filename, **kwargs)

        with open_file(self._DB, "r+") as h5file:
            desc = self.get_schema(name)
            sync_table = h5file.get_node(h5file.root._SYNC, desc["path"])
            it = sync_table.row
            for i in range(2):
                it["filename"] = filename.split("/")[-1]
                it["flag"] = True
            it.append()
            sync_table.flush()
        return True

    def _run_before(self, before, schema, **kwargs):
        """
        function to run before an action
        before
            string. any of url, filename, upload, sync
        schema
            schema as dict
        """
        if schema.get("before") is not None:
            for a,func in schema.get("before"):
                if a == before:
                    func(**kwargs)

    def _run_after(self, after, schema, **kwargs):
        """
        function to run after an action
        after
            string. any of url, filename, upload, sync
        schema
            schema as dict
        """
        if schema.get("after") is not None:
            for a,func in schema.get("after"):
                if a == after:
                    func(**kwargs)

    @property
    def log(self):
        return self._log

    @property
    def repository(self):
        return self._repository

    @property
    def db_name(self):
        return self._DB

    def createDB(self, create_tables = False, force_overwrite = False):
        """
        create the HDF5 file if it doesn't exist
        create_tables
            If True all tables are created with parent nodes
        force_overwrite
            Overwrite an existing file with this file
            default: False
        """
        if os.path.exists(self._DB):
            if force_overwrite:
                h5file = open_file(self._DB, "w")
            else:
                return "File already exists"
        if create_tables:
            DATA = h5file.create_group("/", "_DATA")
            SYNC = h5file.create_group("/", "_SYNC")
            class Sync(IsDescription):
                filename = StringCol(60)
                flag = BoolCol()
            for k,v in self._schema.iteritems():
                h5file.create_table(where = DATA, name = v["path"], description = v["schema"])
                h5file.create_table(where = SYNC, name = v["path"], description = Sync)
        h5file.close()


    def add_path(self, path, name = None):
        """
        Add path to the existing HDF5 file
        This adds a node to the HDF5 file
        path
            HDF5 path. String
        name
            A custom name/description for the path
            Don't use / in your name
        """
        if name is None:
            name = path.split("/")[-1]
        self._schema[name] = {}
        self._schema[name]["path"] = path

    def add_schema(self, name, schema, url, filename = None, upload = None,
                   sync = None, before = None, after = None):
        """
        The schema for the specified path. All arguments are functions except name
        name
            name/path of the node. If there is a / in the argument, it
            is considered a path otherwise a node. The node must exist
        schema
            A description of the data in an accepted PyTables format.
            Any valid description that support the create_table method in
            PyTables
        url
            A function, probably the build_url, that returns a url as a string
        filename
            Filename to be saved in the local repository.
            If None, the last string from the url is used as the filename
        upload
            function to upload the data from the repository to the HDF5 file.
            By default, the file is read line by line and appended to the HDF5 file.
            It is assumed that the file is in csv format
        sync
            A function to synchronize the data in the repository and the HDF5 file
            By default, it is assumed that all data is written to the HDF5 file
            immediately after a file is downloaded and saved in the repository
        before
            Functions to be run before any of url,filename,transform or sync
            A list of 2-tuples with the first being a string with one of the values
            url, filename, transform or sync and the second being the function
            to run
        after
            Similar to before but run after any of url,filename,transform or sync
            is executed
        Notes
        =====
        The functions before and after are run in the following order.
        For url, it is run before the url request is sent and after the url
        request is received
        For filename, before the file is downloaded from the url and after the
        url is downloaded
        For upload, before the file is read and any transformation is made and
        after the file is uploaded to the HDF5 database.
        For sync, before and after the sync function is run.
        """
        if "/" in name:
            for k,v in self._schema.items():
                if v[path] == name:
                    name = k
                    break

        desc = self._schema[name]
        desc["schema"] = schema
        desc["url"] = url
        desc["filename"] = filename
        desc["upload"] = upload
        desc["sync"] = sync
        desc["before"] = before
        desc["after"] = after


    def default_upload(self, dataframe, name):
        """
        The default upload method
        Given a dataframe and a schema name, uploads data to DB
        for columns found in both dataframe and schmea
        """
        with open_file(self._DB, "r+") as h5file:
            desc = self.get_schema(name)
            data_table = h5file.get_node(h5file.root._DATA, desc["path"])
            it = data_table.row
            for i in range(len(dataframe)):
                for col in data_table.colnames:
                    it[col] = dataframe.at[i,col]
                it.append()
            data_table.flush()

    def load_schema(self, schema):
        """
        Load schema from a dictionary or a json file
        Overwrites the existing schema
        """
        if type(schema) == dict:
            self._schema = schema
        else:
            import json
            with open(schema, "r") as f:
                self._schema = json.load(f)

    def get_schema(self, name = None):
        """
        returns the existing schema
        name
            name of the the schema
        """
        return self._schema if name is None else self._schema.get(name)

    def build_url(self, domain, *args):
        """
        Build an url to download data
        domain
            the domain of the website
        args
            keyword args that specify different parts of the url
            If the args is a function it must return a value
        """
        params = "/".join([str(x) for x in args])
        return domain + "/" + params

    def update_repository(self, *args):
        """
        Download the files from the url and save them in the repository
        By default, all urls are downloaded
        To download only specific urls, pass the names as arguments
        """
        if len(args) == 0:
            args = self._schema.keys()
        for k in args:
            v = self._schema.get(k)
            self._run_before("url", v)
            req = self._download(v["url"])
            self._run_after("url", v)

            self._run_before("filename", v)
            self._write_to_repository(req, os.path.join(self._repository, v["path"]), v["filename"])
            self._run_after("filename", v)

    def update(self, *args):
        """
        Download the files from the url, save them in the repository and
        upload to the HDF5 file
        By default, all urls are downloaded
        To upload only specific files, pass the names as arguments
        """
        if len(args) == 0:
            args = self._schema.keys()
        for k in args:
            v = self.get_schema(k)
            self._run_before("url", v)
            req = self._download(v["url"])
            self._run_after("url", v)

            path = os.path.join(self._repository, v["path"])
            self._run_before("filename", v)
            filename = self._write_to_repository(req, path, v["filename"])
            self._run_after("filename", v)

            if filename:
                self._run_before("upload", v)
                self._upload_to_DB(os.path.join(path, filename), k)
                self._run_after("upload", v)
            else:
                self._log.append(("update", filename, "File not uploaded"))

    def syncDB(self, *args):
        """
        Synchronize the repository with the HDF5 file
        This function iterates the repository and uploads file to the DB
        that are earlier not uploaded. This ischs useful when downloads are done
        at one time and uploads at another time
        Names as args
        """
        if len(args) == 0:
            args = self._schema.keys()
        for k in args:
            v = self._schema.get(k)
            self._run_before("sync", v)
            if v["sync"] is None:
                with open_file(self._DB, "r+") as h5file:
                    path = os.path.join(self._repository, v["path"])
                    for dirpath, dirnames, filenames in os.walk(path):
                        filelist = h5file.get_node(h5file.root._SYNC, v["path"]).read(field = "filename")
                        for f in filenames:
                            if f not in filelist:
                                self._upload_to_DB(os.path.join(path, f), k)
            else:
                v["sync"]()
                self._run_after("sync", v)
