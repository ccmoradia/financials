from financials.tools.indicators import *
from pandas.io.excel import ExcelFile

xls = ExcelFile("indicators.xls")
data = xls.parse("Indicators", skiprows = 1, index_col = 0, parse_dates = True)
df = data[["O", "H", "L", "C", "V"]]

assert 10 == 4+6