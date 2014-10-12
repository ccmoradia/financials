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
from financials.utilities.decorators import *

def CLV(S, **kwargs):
    """
    Calculates the Close Location Value
    """
    return ((S.C - S.L) - (S.H - S.C))/(S.H - S.L)

def TR(S, **kwargs):
    """
    Calculate the True Range
    """
    return DataFrame([S.H - S.L, S.H - S.C.shift(1), S.C.shift(1) - S.L]).T.max(axis = 1)

@period
@frequency
def AD(S, **kwargs):
    """
    Calculates the Accumulation/Distribution line
    """
    return (S.V * CLV(S)).cumsum()

@period
@frequency
def ADX(S, n = 14, **kwargs):
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
    adx = (DX.shift * (n-1) + DX) / n
    return adx

@period
@frequency
def ATR(S, n = 14):
    """
    Calculate the Average True Range
    """
    TrueRange = TR(S)
    return ((TrueRange.shift(1) * (n-1)) + TrueRange) / n

@period
@frequency
def SMA(S, n = 7, **kwargs):
    """
    Calculates the simple moving average
    """
    return rolling_mean(S.C, n)

@period
@frequency
def EMA(S, n = 7, **kwargs):
    """
    Calculates the exponential moving average
    """
    alpha = 2.0 / (n+1)
    return S.C * alpha + (S.C.shift(1) * (1 - alpha))

@period
@frequency
def BB(S, k = 2, n = 14, **kwargs):
    """
    Calcuate the bollinger bands
    """
    sigma = rolling_std(S.C, n)
    central_band = MA(n)
    upper_band = central_band + (k * sigma)
    lower_band = central_band - (k * sigma)
    return DataFrame([central_band, upper_band, lower_band]).T


@period
@frequency
def FS(S, n1 = 7, n2 = 5, n3 = 5, **kwargs):
    """
    Calculate the Full Stochastic momentum indicator
    """
    S['MinLow'] = rolling_min(S.L, n1)
    S['MaxHigh'] = rolling_max(S.L, n1)
    K_fast = ((S.C - S.MinLow) / (S.MaxHigh - S.MinLow)) * 100
    K_full = MA(K_fast, n2)
    D_full = MA(K_full, n3)
    return DataFrame([K_full, D_full]).T

@period
@frequency
def MACD(S, n1 = 12, n2 = 26, n3 = 9, **kwargs):
    """
    Calculate the Moving Average Convergence Divergence
    """
    macd = EMA(S, n1) - EMA(S, n2)
    signal_line = EMA(macd, 9)
    histogram = macd - signal_line
    return DataFrame([macd, signal_line, histogram]).T

@period
@frequency
def OBV(S, **kwargs):
    """
    Calculate the On Balance Volume
    """
    S['Indicate'] = S.C - S.C.shift(1)
    S['OBV'] = [V if P > 0 else -V for (P,V) in zip(S.Indicate, S.V)]
    return S.OBV.cumsum()


@period
@frequency
def RSI(S, n = 7, **kwargs):
    """
    Calculate the Relative Strength Index
    """
    gain = []
    loss = []
    for (a,b) in zip(S.C, S.C.shift(1)):
        if a > b:
            gain.append(a - b)
            loss.append(0)
        else:
            loss.append(b - a)
            gain.append(0)
    S['Gain'] = gain
    S['Loss'] = loss
    intial_gain = MA(S.Gain, n)
    average_gain = ((initial_gain.shift(1) * (n - 1)) / initial_gain) / n
    initial_loss = MA(S.Loss, n)
    average_loss = ((initial_loss.shift(1) * (n -1)) / initial_loss) / n
    RS = average_gain / average_loss
    rsi = 100 - (100 / (1 + RS))
    return rsi

@period
@frequency
def SR(S, **kwargs):
    """
    Returns the support resistance levels
    """
    pass
