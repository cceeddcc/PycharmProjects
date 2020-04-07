import pandas as pd
import numpy as np
import pandas_datareader.data as web


fb = web.DataReader("FB", "yahoo")
fb.shape
fb.columns
fb["diff"] = fb["Adj Close"] - fb["Adj Close"].shift(-1)
fb["Directions"] = [1 if fb.loc[er,"diff"] > 0 else -1
                    for er in fb.index]

# moving average
fb["Adj Close"]
fb["MA30"] = fb["Adj Close"].rolling(30).mean()
fb["MA60"] = fb["Adj Close"].rolling(60).mean()
fb["Adj Close"].plot()
fb["MA30"].plot()
fb["MA60"].plot()

# Trading strategies
# long or not
fb.head()
fb["Shares"] = [1 if fb.loc[i,"MA30"] > fb.loc[i,"MA60"] else 0
                for i in fb.index]

# fb["Shares"] = 0
# fb["Shares"][fb["MA30"] > fb["MA60"]] = 1

# Daily Profit
fb["Price1"] = fb["Adj Close"].shift(-1)
fb["Profit"] = [(fb.loc[i,"Price1"]/fb.loc[i, "Adj Close"]) if fb.loc[i,"Shares"] == 1 else 1
                for i in fb.index]
fb["Profit"].plot()
# cumulative wealth
fb["Wealth"] = fb["Profit"].cumprod()
fb["Wealth"].plot()

# fb.to_excel("C:/Users/S/Desktop/wow.xlsx")

