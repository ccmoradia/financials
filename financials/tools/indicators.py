"""
A library of functions containing common technical indicators
All functions take the stock details as the first parameter.
Stock must be a dataframe with date as index and the following columns
 * O - Open
 * H - High
 * L - Low
 * C - Close
 * V - Volume 
"""

from pandas import DataFrame, rolling_mean, rolling_std, rolling_max, rolling_min


def CLV(df):
    """
    Calculates the Close Location Value
    """
    return ((C-L) - (H-C))/(H-L)
    
def AD(df):
    """
    Calculates the Accumulation/Distribution line
    """
    return (V * CLV(df)).cumsum()
    
def ADX(S, n = 14):
    """
    Calculates the Average Directional Movement Index
    """
    plus_DM = S.H - S.H.shift(1)
    minus_DM = S.L.shift(1) - S.L
    TrueRange = TR(S)
    plus_DM_n = ((plus_DM.shift(1) * (n-1)) + plus_DM) / n
    minus_DM_n = ((minus_DM.shift(1) * (n-1)) + minus_DM) / n
    TrueRangen_n = ((TrueRange.shift(1) * (n-1)) + TrueRange) / n
    plus_DI_n = plus_DM_n / TrueRange_n
    minus_DI_n = minus_DM_n / TrueRange_n
    DI = abs(plus_DI_n - minus_DI_n)
    DX = DI / DataFrame([plus_DI_n, minus_DI_n]).T.sum(axis = 1)
    ADX = (DX.shift * (n-1) + DX) / n
    return ADX
    
def ATR(S, n = 14):
    """
    Calculate the Average True Range
    """
    TrueRange = TR(S)
    ATR = ((TrueRange.shift(1) * (n-1)) + TrueRange) / n
    return ATR
    
def TR(S):
    """
    Calculate the True Range
    """
    return DataFrame([S.H - S.L, S.H - S.C.shift(1), S.C.shift(1) - S.L]).T.max(axis = 1)
    
def MA(S, n = 7):
    """
    Calculates the simple moving average
    """
    return rolling_mean(S, n)
    
def EMA(S, n = 7):
    """
    Calculates the exponential moving average
    """
    alpha = 2.0 / (n+1)
    return S.C * alpha + (S.C.shift(1) * (1 - alpha))

def BB(S, k = 2, n = 14):
    """
    Calcuate the bollinger bands
    """
    sigma = rolling_std(S.C, n)
    central_band = MA(n)
    upper_band = central_band + (k * sigma)
    lower_band = central_band - (k * sigma)
    return DataFrame([central_band, upper_band, lower_band]).T
    
def CMF(S, n = 21):
    """
    Calculate the Chaikin Money Flow
    """
    return AD/S.V.cumsum()
    
def CV(S, n = 10):
    """
    Calculate the Chaikin volatility
    """
    H = rolling_max(S.H, n)
    L = rolling_min(S.L, n)
    C = H - L
    EMA_1 = EMA(DataFrame([H,L,C]).T, n)
    C = S.H - S.L.shift(n)
    EMA_2 = EMA(DataFrame([H,L,C]).T, n)
    return ((EMA_1 - EMA_2) / EMA_2) * 100
    
def TP(S):
    """
    Calculate the typical price of a stock
    """
    return (S.H + S.L + S.C) / 3

def CCI(S, n = 20, c = 0.15):
    """
    Calculate the Commodity Channel Index
    """
    typical_price = TP(S)
    moving_average = MA(TP, 20)
    mean_deviation = (abs(typical_price - moving_average)).mad()
    return (typical_price - moving_average) / (c * mean_deviation)
    
    
