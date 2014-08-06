from financials.utilities.utilities import profit

# This entire python file is written as a doctest

def test_profit():
    """
    The profit function calculates the percentage of profit on a trade given
    OHLC and Buy and Sell triggers. The basic assumption is that once a trade
    is entered into, the position is closed. All orders are considered as
    LIMIT Orders. The first four arguments to the function are the
    Open, High, Low and Close prices for the stock.
    Percentage arguments must be relative to the Open Price.
    Market and Limit order conditions

    A simple example
    Buy a stock and sell it at the end of the period
    >>> profit(100, 104, 97, 102)
    0.02

    Buy when the stock increases by 1%
    >>> profit(100, 104, 97, 102, BuyAt = 0.01)
    0.0099

    Buy when stock increases by 1% and sell when it increases to 3%
    >>> profit(100, 104, 97, 102, BuyAt = 0.01, SellAt = 0.03)
    0.0198

    All percentages must be relative to the Open Price. In the above case,
    if you want to calculate the profit when the price increases to 2%
    after you buy, then the relative increase from the open price must be
    the value to the SellAt argument. This would be
    >>> profit(100, 104, 97, 102, BuyAt = 0.01, SellAt = 0.0302)
    0.02

    Buy when stock increases by 1% and sell when it increases to 5%
    >>> profit(100, 104, 97, 102, BuyAt = 0.01, SellAt = 0.05)
    0.0099

    Since the period is closed, and a position is entered into the stock
    is sold at current price

    Buy when stock increases by 5% and sell when it increases to 10%
    >>> profit(100, 104, 97, 102, BuyAt = 0.05, SellAt = 0.10)
    0.0

    No trade is possible as both the BuyAt and SellAt percentages
    fall outside the range of OHLC

    You could also use negative percentages
    >>> profit(100, 104, 97, 102, BuyAt = -0.01)
    0.0303

    >>> profit(100, 104, 97, 102, BuyAt = -0.01, SellAt = -0.03)
    -0.0202

    >>> profit(100, 104, 97, 102, BuyAt = 0.01, SellAt = -0.02)
    -0.0297

    If you aren't comfortable with percentages, you can enter price directly
    >>> profit(100, 104, 97, 102, BuyAt = 101, SellAt = 105)
    0.0099

    The function does infer percentages and values by following a simple rule;
    If the value of BuyAt and SellAt is less than 1, then it is a percentage.

    You can also mix percentages and values
    >>> profit(100, 104, 97, 102, BuyAt = 101, SellAt = 0.05)
    0.0099

    >>> profit(100, 104, 97, 102, BuyAt = 0.01, SellAt = 105)
    0.0099

    However this fails in the following case,
    >>> profit(0.1, 0.112, 0.085, 0.105, BuyAt = 0.08, SellAt = 0.15)
    -0.0278

    Since both Buy and Sell are considered as percentages
    To distinguish between prices and percentages explicitly, use
    **percent = True ** for using percentage and **percent = False** for prices.
    Following the above example,
    >>> profit(0.1, 0.112, 0.085, 0.105, BuyAt = 0.08, SellAt = 0.15, percent = False)
    0.0

    Since no trade is possible within the given limits

    The function determines entry, exit, buy and sell based on the following
    criteria

    * If BuyAt and SellAt are both 0, then it is a market order for Buy and the
    entry is the Open Price and exit is the close price
    * If BuyAt is 0 and SellAt is some price, then it is a limit order for Sell
    and the entry is the SellAt Price and exit is the Close Price
    * If Sell At is 0 and BuyAt is some price, then it is a limit order for Buy
    and the entry is the BuyAt Price and the exit is the Close Price
    * If both BuyAt and SellAt has some price, then

        * If both the prices fall outside the range of OHLC, then no trade is
        possible and hence the return is zero
        * If one of the prices fall within the range, then trade is entered
        into at that price and position and exited at the close price
        * If both of the prices fall within the range, then the corresponding
        entry and exit positions are taken and profit is calculated. *There is a gotcha here*

    If you want to enter into a particular position, use the argument **Entry**
    **entry = B** for a buy position and **entry = S** for a sell position.

    Lets see a few examples. Instead of Buy and Sell, we would use Long and
    Short positions to indicate the entry position.

    Open a short position at market price
    >>> profit(100, 104, 97, 102, entry = "S")
    -0.02

    Without the entry argument, the result would be 0.02 as in the very
    first example

    Open a long position when market moves by 1%
    >>> profit(100, 104, 98, 102, BuyAt = 0.01, entry = "B")
    0.0099

    Open a short position at market price and exit at 101
    >>> profit(100, 104, 98, 102, BuyAt = 101, entry = "S")
    -0.01

    Open a long position at 99 and exit at 101
    >>> profit(100, 104, 97, 102, BuyAt = 99, SellAt = 101, entry = "B")
    0.0202

    Open a short position at 101 and exit at 99
    >>> profit(100, 104, 97, 102, BuyAt = 99, SellAt = 101, entry = "S")
    0.0198

    You could see the difference in returns for the same order but at
    different entry positions. By default, it is always considered a long
    position. This is the gotcha.

    If you aren't sure about the entry and exit positions and want a rather
    random buy or sell, pass **entry = "R"**

    >>> profit(100, 104, 97, 102, BuyAt = 99, SellAt = 101, entry = "R") #doctest: +SKIP

    This could give either 0.0202 or 0.0198. If you are probabilistic, then
    you could pass a value between 0 to 1 to the Entry argument. 0 means a
    definite buy order and 1 meaning a definite sell order. For the curious,
    this picks a number from the uniform distribution

    Placing stop loss orders is just similar.

    Buy at 100 with a stop loss of 2%.

    >>> profit(100, 104, 97, 102, BuyAt = 100, SellAt = 98)
    -0.02

    >>> profit(100, 104, 97, 102, BuyAt = 100, SellAt = -0.02)
    -0.02

    Both the above orders are same. But there is a caveat. If you place both
    a Buy order and a Stop Loss order and when the price never reaches the
    Buy price but hits the Stop Loss price, the stop loss would be executed
    first as a Sell Order. This is because all orders are considered as
    Limit Orders and a limit order gets executed as soon as it hits the
    trigger price. An example for clarity

    >>> profit(100, 101, 96, 97, BuyAt = 102, SellAt = 98)
    0.0102

    >>> profit(100, 101, 96, 99, BuyAt = 102, SellAt = 98)
    -0.0102

    In both the cases, the range never hit the buy price but the order would
    still get executed at 98 and closed at 97 in the first case and 99 in
    the second case. This is because the function considers both the order as
    Limit orders and executes them when the order is in the given range.

    If the open price is equal to the high or low price during the entire
    period, then it is unlikely your order gets executed at the open price
    since the time you place the order must be before the time the market opens.
    So if you see a OHLC price of (100, 108, 100, 105), it is unlikely your
    order gets executed at 100 since the market might have moved up as soon
    as it opens. In such cases, a buy order at 100 and a Sell at 98 is never
    going to be executed and it must give a return of zero. To deal with such
    cases, pass the **OPEN** argument with the value *True*

    >>> profit(100, 108, 100, 105, BuyAt = 100) # doctest: +SKIP
    0.05 #Highly unlikely the order gets executed

    >>> profit(100, 108, 100, 105, BuyAt = 100, OPEN = True)
    0

    >>> profit(100, 108, 99, 105, BuyAt = 100, OPEN = True)
    0.05

    >>> profit(100, 108, 100, 105, BuyAt = 100, OPEN = True, entry = "S")
    -0.05

    In the second case, the order would get executed since the price has
    fallen and retraced back to 100

    >>> profit(100, 100, 95, 96, SellAt = 100, OPEN = True)
    0

    More examples for the above type

    Quirky order
    >>> profit(100, 104, 97, 102, BuyAt = 105, SellAt = 103) #doctest: +SKIP



    RoundOff
    --------
    By default the function rounds off to 4 decimal places. Use the **digits**
    argument to specify the number of digits in the output

    FAQ
    ---
    What if my position is open?
    What if in case of trailing stop loss orders?
    What if in case of Bracket Orders?
    What if in case of Market Orders?

    Tick size
    Corner case for BuyAt = 1
    """
    pass