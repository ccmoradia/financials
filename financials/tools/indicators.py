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

from pandas import DataFrame, rolling_mean, rolling_std, rolling_max, rolling_min, rolling_max


def CLV(S):
    """
    Calculates the Close Location Value
    """
    return ((S.C - S.L) - (S.H - S.C))/(S.H - S.L)
    
def AD(S):
    """
    Calculates the Accumulation/Distribution line
    """
    return (S.V * CLV(S)).cumsum()
    
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
    adx = (DX.shift * (n-1) + DX) / n
    return adx
    
def ATR(S, n = 14):
    """
    Calculate the Average True Range
    """
    TrueRange = TR(S)
    return ((TrueRange.shift(1) * (n-1)) + TrueRange) / n
    
def TR(S):
    """
    Calculate the True Range
    """
    return DataFrame([S.H - S.L, S.H - S.C.shift(1), S.C.shift(1) - S.L]).T.max(axis = 1)
    
def MA(S, n = 7):
    """
    Calculates the simple moving average
    """
    return rolling_mean(S.C, n)
    
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
    return AD(S)/S.V.cumsum()
    
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
    
def DPO(S, n = 7):
    """
    Calculate the Detrended Price Oscillator
    """
    X = int(n/2) + 1
    moving_average = MA(S, n)
    return moving_average - moving_average.shift(X)
    
def EMV(S):
    """
    Calculate the ease of movement
    """
    A = (S.H + S.L) / 2
    B = S.V / (S.H + S.L)
    return (A - A.shift(1)) / B
    
def FS(S, n1 = 7, n2 = 5, n3 = 5):
    """
    Calculate the Full Stochastic momentum indicator
    """
    S['MinLow'] = rolling_min(S.L, n1)
    S['MaxHigh'] = rolling_max(S.L, n1)
    K_fast = ((S.C - S.MinLow) / (S.MaxHigh - S.MinLow)) * 100
    K_full = MA(K_fast, n2)
    D_full = MA(K_full, n3)
    return DataFrame([K_full, D_full]).T
    
def MFI(S, n = 7):
    """
    Calculate the Money Flow Index
    """
    typical_price = TP(S)
    S['PMF'] = 0
    S['NMF'] = 0
    S['Indicate'] = typical_price > typical_price.shift(1)
    S[S.Indicate == True]['PMF'] = typical_price * S.V
    S[S.Indicate == False]['NMF'] = typical_price * S.V
    money_ratio = rolling_mean(S.PMF, n) / rolling_mean(S.NMF, n)
    mfi = 100 - ((100/ 1 + money_ratio))
    return mfi

def MACD(S, n1 = 12, n2 = 26, n3 = 9):
    """
    Calculate the Moving Average Convergence Divergence
    """
    macd = EMA(S, n1) - EMA(S, n2)
    signal_line = EMA(macd, 9)
    histogram = macd - signal_line
    return DataFrame([macd, signal_line, histogram]).T
    
def OBV(S):
    """
    Calculate the On Balance Volume
    """
    S['Indicate'] = S.C - S.C.shift(1)
    S['OBV'] = [V if P > 0 else -V for (P,V) in zip(S.Indicate, S.V)]
    return S.OBV.cumsum()
    
def PP(S):
    """
    Calculate the Pivot Points
    """
    pp = TP(S)
    s1 = (2 * pp) - S.H
    s2 = pp - S.H - S.L
    s3 = S.L - (2* (S.H - pp))
    r1 = (2 * pp) - S.L
    r2 = pp + S.H + S.L
    r3 = S.H + 2* (pp - S.L)
    return DataFrame([pp, s1, s2, s3, r1, r2, r3]).T
    
def PO(S, n1 = 5, n2 = 10):
    """
    Calculate the Price Oscillator
    """
    return ((EMA(S, n1) - EMA(S, n2)) / EMA(S, n2)) * 100
    
def ROC(S, n = 7):
    """
    Calculate the Rate of Change
    """
    return (S.C - S.C.shift(n)) / S.C.shift(n)
    
def RSI(S, n = 7):
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
   
def VWMA(S, n = 7):
    """
    Calculate the Volume Weighted Moving Average
    """
    S['VWMA'] = S.V * S.P
    S['CUMVOL'] = rolling_sum(S.V, n)
    return S['VWMA'] / S['CUMVOL']
    
def WR(S, n = 7):
    """
    Calculate the Williams % R
    """
    S['MaxHigh'] = rolling_max(S.C, n)
    S['MinLow'] = rolling_min(S.C, n)
    return ((S.MaxHigh - S.C) / (s.MaxHigh - S.MinLow)) * -100
