import os
import datetime
import json
import sys
if "/home/ubermensch/financials" not in sys.path:
    sys.path.append("/home/ubermensch/financials")
from pandas import DataFrame
from financials.utilities.bootstrap import BootStrap
from tables import IsDescription, StringCol, Float16Col, Float32Col,\
                   Float64Col, Int32Col

class Equity(IsDescription):
    SYMBOL = StringCol(50)
    SERIES = StringCol(2)
    OPEN = Float32Col()
    HIGH = Float32Col()
    LOW = Float32Col()
    CLOSE = Float32Col()
    LAST = Float32Col()
    PREVCLOSE = Float32Col()
    TOTTRDQTY = Int32Col()
    TOTTRDVAL = Float64Col()
    TIMESTAMP = StringCol(12)
    TOTALTRADES = Int32Col()
    ISIN = StringCol(12)

class Preopen(IsDescription):
    symbol = StringCol(50)
    xDt = StringCol(50)
    caAct = StringCol(50)
    iep = Float32Col()
    chn = Float16Col()
    perChn = Float16Col()
    pCls = Float32Col()
    trdQnty = Int32Col()
    iVal = Float16Col()
    sumVal = Float32Col()
    sumQnty = Int32Col()
    finQnty = Int32Col()
    sumfinQnty = Int32Col()

class Derivative(IsDescription):
    INSTRUMENT = StringCol(6)
    SYMBOL = StringCol(50)
    EXPIRY_DT = StringCol(11)
    STRIKE_PR = Int32Col()
    OPTION_TYP = StringCol(2)
    OPEN = Float32Col()
    HIGH = Float32Col()
    LOW = Float32Col()
    CLOSE = Float32Col()
    SETTLE_PR = Float32Col()
    CONTRACTS = Int32Col()
    VAL_INLAKH = Float64Col()
    OPEN_INT = Int32Col()
    CHG_IN_OI = Int32Col()
    TIMESTAMP = StringCol(11)


class NSEBootStrap(BootStrap):
    """
    BootStrap for NSE
    """
    def url_equity(self, day = datetime.date.today()):
        """
        Get the url for equity
        """
        domain = "http://nseindia.com/content/historical/EQUITIES"
        return self.build_url(domain, day.strftime("%Y"), day.strftime("%b").upper(),
                              "cm" + day.strftime("%d%b%Y").upper() + "bhav.csv.zip")
    def url_preopen(self):
        return "http://nseindia.com/live_market/dynaContent/live_analysis/pre_open/nifty.json"

    def filename_preopen(self):
        return datetime.date.today().strftime("%Y-%m-%d") + ".json"

    def upload_preopen(self, filename):
        with open(filename, "r") as f:
            df = DataFrame(json.load(f)["data"])
        df = df.replace(",", "", regex = True)
        self.default_upload(df, "preopen")

    def url_derivative(self, day = datetime.date.today()):
        domain = "http://nseindia.com/content/historical/DERIVATIVES"
        return self.build_url(domain, day.strftime("%Y"), day.strftime("%b").upper(),
                              "fo" + day.strftime("%d%b%Y").upper() + "bhav.csv.zip")


if __name__ == "__main__":
    rep = "/home/ubermensch/NSE/data"
    db = "/home/ubermensch/NSE/test.h5"
    bt = NSEBootStrap(db, rep)
    bt.add_path("preopen", "preopen")
    bt.add_path("bhavcopy", "equity")
    bt.add_path("fo", "derivative")
    bt.add_schema("preopen", schema = Preopen, url = bt.url_preopen,
                filename = bt.filename_preopen, upload = bt.upload_preopen)
    bt.add_schema("equity", schema = Equity, url = bt.url_equity)
    bt.add_schema("derivative", schema = Derivative, url = bt.url_derivative)
    bt.update("equity", "preopen")
    print bt.log