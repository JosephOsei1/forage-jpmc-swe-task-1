################################################################################
#
#  Permission is hereby granted, free of charge, to any person obtaining a
#  copy of this software and associated documentation files (the "Software"),
#  to deal in the Software without restriction, including without limitation
#  the rights to use, copy, modify, merge, publish, distribute, sublicense,
#  and/or sell copies of the Software, and to permit persons to whom the
#  Software is furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in
#  all copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
#  OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
#  FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
#  DEALINGS IN THE SOFTWARE.

import json
import random
import urllib.request


# Server API URLs
QUERY = "http://localhost:8080/query?id={}"

# 500 server request
N = 500


def getDataPoint(quote):
    """
    Produce all the needed values to generate a datapoint.

    Args:
        quote (dict): A dictionary containing the stock symbol, top bid price, and top ask price.

    Returns:
        tuple: A tuple containing the stock symbol, bid price, ask price, and average price.

    Example:
        quote = {
            'stock': 'AAPL',
            'top_bid': {'price': '150.00'},
            'top_ask': {'price': '152.00'}
        }
        stock, bid_price, ask_price, price = getDataPoint(quote)
        print(stock)  # Output: AAPL
        print(bid_price)  # Output: 150.0
        print(ask_price)  # Output: 152.0
        print(price)  # Output: 151.0
    """
    stock = quote['stock']
    bid_price = float(quote['top_bid']['price'])
    ask_price = float(quote['top_ask']['price'])
    price = (bid_price + ask_price) / 2
    return stock, bid_price, ask_price, price

def getRatio(price_a, price_b):
    """
    Get the ratio of two given numbers.

    Parameters:
    price_a (float): The numerator of the ratio.
    price_b (float): The denominator of the ratio.

    Returns:
    float or None: The calculated ratio of price_a and price_b. If price_b is zero, returns None to avoid division by zero.
    """

    if price_b == 0:
        # Avoid division by zero
        return None
    return price_a / price_b

# Main
if __name__ == "__main__":
    # Query the price once every N seconds.
    prices = {}  # Dictionary to store stock prices
    for _ in iter(range(N)):
        try:
            quotes = json.loads(urllib.request.urlopen(QUERY.format(random.random())).read())
        except urllib.error.URLError as e:
            print(f"Error fetching data from the server: {e}")
            continue  # Skip this iteration and try again

        # Update to get the ratio
        for quote in quotes:
            stock, bid_price, ask_price, price = getDataPoint(quote)
            prices[stock] = price  # Store the price in the dictionary
            print("Quoted %s at (bid:%s, ask:%s, price:%s)" % (stock, bid_price, ask_price, price))

        # Calculate and print the ratio
        stock_a = "houses"  # Replace with the actual stock names you want to compare
        stock_b = "cars"
        if stock_a in prices and stock_b in prices:
            ratio = getRatio(prices[stock_a], prices[stock_b])
            if ratio is not None:
                print("Ratio %s" % ratio)

