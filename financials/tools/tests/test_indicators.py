from financials.tools.indicators import *
from pandas.io.excel import ExcelFile
import os

filename = os.path.join(os.getcwd(), "financials", "tools", "tests", "indicators.xls")

xls = ExcelFile(filename)
data = xls.parse("Indicators", skiprows = 1, index_col = 0, parse_dates = True)
df = data[["O", "H", "L", "C", "V"]]

# This is a dictionary. Keys are the function names as string while the values
# are 2-tuples with first element being the actual function and the second
# element is the list of column names in the Excel File. The dictionary is
# iterated and each function result is compared to the actual result in the
# Excel File

result = {
"AD": (AD, ("AD")),
"ATR": (ATR, ("ATR")),
"SMA": (SMA, ("SMA")),
"EMA": (EMA, ("EMA")),
"BB": (BB, ("CentralBand", "UpperBand", "LowerBand")),
"FS": (FS, ("K_full", "D_full")),
"MACD": (MACD, ("MACD", "SignalLine", "Hist")),
"OBV": (OBV, ("OBV")),
"RSI": (RSI, ("RSI")),
"SR": (SR, ("Support", "Resistance"))
}

def checkAlmostEqual(one, two, precision = 10):
    """
    Checks whether the values in one and two are equal to the given precision
    """
    collect = []
    for a,b in zip(one.dropna().values, two.dropna().values):
        collect.append(a - b < 1/1e-10)
    return all(collect)

def test_indicators():
    for indicator, cols in result.values():
        assert checkAlmostEqual(indicator(df), data.ix[:, cols])
