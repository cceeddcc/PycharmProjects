import pandas as pd
import pandas_datareader as dr
import numpy as np
import sqlite3 as sql
import statsmodels.api as sm
import matplotlib.pyplot as plt
import os
import scipy.stats as stats

os.getcwd()
os.chdir("C:/Users/S/Desktop/바탕화면(임시)/ETF/")

# MA(30), MA(60) 골든크로스 매매에 대한 수익률 backtest
df_ETF_index = pd.read_excel("C:/Users/S/Desktop/ETF기초지수.xlsx")
df_ETF_index_code = list(df_ETF_index["종목코드"])
con = sql.connect("ETF.db")
df_ETF_goldencross = pd.DataFrame()
MDD_list = []
risk_adj_return_list = []
t = 0
for code in df_ETF_index_code[0:100] :
    t += 1
    print(t, " / ", len(df_ETF_index_code))

    # code = df_ETF_index_code[0] # tmp
    ETF_df = pd.read_sql("Select * from %s" %code, con, index_col=None)

    # Trading signal initialization
    ETF_df["MA30"] = ETF_df["Close"].rolling(window=30).mean()
    ETF_df["MA60"] = ETF_df["Close"].rolling(window=60).mean()
    ETF_df["signal"] = [1 if ETF_df.loc[i,"MA30"] > ETF_df.loc[i,"MA60"] else 0
                        for i in ETF_df.index]
    ETF_df["Close1"] = ETF_df["Close"].shift(-1)
    ETF_df["daily_return"] = [ETF_df.loc[i, "Close1"] / ETF_df.loc[i, "Close"] if ETF_df.loc[i, "signal"] == 1 else 1
                              for i in ETF_df.index]
    ETF_df["cum_return"] = ETF_df["daily_return"].cumprod()

    MDD_list.append((ETF_df["cum_return"]/ETF_df["cum_return"].cummax()-1).min())
    daily_return = (ETF_df["cum_return"].iloc[-2] - 1) / len(ETF_df.index)
    risk_adj_return_list.append(daily_return / (ETF_df["Close1"] / ETF_df["Close"]).std())

    ETF_df = ETF_df.dropna()
    ETF_df.index = [i for i in range(0,len(ETF_df.index))]
    df_ETF_goldencross["cum_return_%s" %code] = ETF_df["cum_return"]

con.close()

df_ETF_goldencross.loc["MDD"] = MDD_list
df_ETF_goldencross.loc["risk_adj_return"] = risk_adj_return_list
df_ETF_goldencross.to_excel("C:/Users/S/Desktop/goldencross.xlsx")



con = sql.connect("ETF.db")
ETF_df = pd.read_sql("Select * from %s" % "A139220", con, index_col=None)
ETF_df["MA30"] = ETF_df["Close"].rolling(window=30).mean()
ETF_df["MA60"] = ETF_df["Close"].rolling(window=60).mean()

con.close()
ETF_df["Close"].plot()
ETF_df["MA30"].plot()
ETF_df["MA60"].plot()



# MA(30)의 변화율이 Gaussian WN process를 따를까?
# MA(30)의 변화율이 Gaussian을 따를 때, Pair trading 가능 ?

df_ETF_index = pd.read_excel("C:/Users/S/Desktop/ETF기초지수.xlsx")
df_ETF_index_code = list(df_ETF_index["종목코드"])
con = sql.connect("ETF.db")
t = 0
for code in df_ETF_index_code[0:10] :
    t += 1
    print(t, " / ", len(df_ETF_index_code))

    code = df_ETF_index_code[0] # tmp
    code2 = df_ETF_index_code[10] # tmp
    ETF_df_p1 = pd.read_sql("Select * from %s" %code, con, index_col=None)
    ETF_df_p2 = pd.read_sql("Select * from %s" %code2, con, index_col=None)

    ETF_df_p1["Date"] = ETF_df_p1["Date"].astype(str)
    ETF_df_p1["Date"] = pd.to_datetime(ETF_df_p1["Date"])
    ETF_df_p2["Date"] = ETF_df_p2["Date"].astype(str)
    ETF_df_p2["Date"] = pd.to_datetime(ETF_df_p2["Date"])

    df_pairs = pd.DataFrame({"Date": ETF_df_p1["Date"]})

    # Trading signal initialization
    ETF_df_p1["MA30"] = np.log(ETF_df_p1["Close"].rolling(window=30).mean())
    ETF_df_p2["MA30"] = np.log(ETF_df_p2["Close"].rolling(window=30).mean())
    ETF_df_p1["diff.MA30"] = ETF_df_p1["MA30"] - ETF_df_p1["MA30"].shift(1)
    ETF_df_p2["diff.MA30"] = ETF_df_p2["MA30"] - ETF_df_p2["MA30"].shift(1)

    # pair
    df_pairs = df_pairs.merge(ETF_df_p1[["Date","Close","diff.MA30"]], on="Date")
    df_pairs = df_pairs.merge(ETF_df_p2[["Date","Close","diff.MA30"]], on="Date")
    df_pairs = df_pairs.dropna()
    # df_pairs.iloc[:,2].plot()
    # df_pairs.iloc[:,4].plot()

    # QQ plot 보면 diff.MA30은 WN처럼 보임
    # stats.probplot(ETF_df_p1["diff.MA30"], dist="norm", plot=plt)
    # stats.probplot(ETF_df_p2["diff.MA30"], dist="norm", plot=plt)

    # histogram
    # stats.probplot(df_pairs.iloc[:,2], dist="norm", plot=plt)
    # stats.probplot(df_pairs.iloc[:,4], dist="norm", plot=plt)

    # df_pairs.iloc[:, 2].hist(bins=100)
    # df_pairs.iloc[:, 4].hist(bins=100)
    #
    # # 검정결과 정규분포는 아님
    # stats.jarque_bera(df_pairs.iloc[:, 2])
    # stats.jarque_bera(df_pairs.iloc[:, 4])

    # 표준화
    df_pairs["p1_standard"] = (df_pairs["diff.MA30_x"]-df_pairs["diff.MA30_x"].mean())/df_pairs["diff.MA30_x"].std(ddof=1)
    df_pairs["p2_standard"] = (df_pairs["diff.MA30_y"]-df_pairs["diff.MA30_y"].mean())/df_pairs["diff.MA30_y"].std(ddof=1)

    # Index
    # 고 Index : short p1, long p2
    # 저 Index : short p2, long p1
    df_pairs["Index"] = df_pairs["p1_standard"] - df_pairs["p2_standard"]
    upper = df_pairs["Index"].mean() + df_pairs["Index"].std(ddof=1)*1.96
    lower = df_pairs["Index"].mean() - df_pairs["Index"].std(ddof=1)*1.96

    signal = []
    for i in df_pairs.index :
        if df_pairs.loc[i,"Index"] > upper :
            signal.append(1)
        elif df_pairs.loc[i,"Index"] < lower :
            signal.append(-1)
        else : signal.append(0)
    df_pairs["signal"] = signal

    # signal 1 : short p1, long p2
    df_pairs["Close_x1"] = df_pairs["Close_x"].shift(-1)
    df_pairs["Close_y1"] = df_pairs["Close_y"].shift(-1)
    df_pairs["return_p1"] = df_pairs["Close_x1"]/df_pairs["Close_x"]
    df_pairs["return_p2"] = df_pairs["Close_y1"]/df_pairs["Close_y"]

    return_pair = []
    for i in df_pairs.index:
        if df_pairs.loc[i, "signal"] == 1:
            return_pair.append((-df_pairs.loc[i,"return_p1"]+df_pairs.loc[i,"return_p2"])+1)
        elif df_pairs.loc[i, "signal"] == -1:
            return_pair.append((df_pairs.loc[i,"return_p1"]-df_pairs.loc[i,"return_p2"])+1)
        else:
            return_pair.append(1)

    df_pairs["return"] = return_pair
    df_pairs["cum_return"] = df_pairs["return"].cumprod()
    df_pairs["cum_return"].plot()
    # 수익성 없어보임

    # index가 거의 정규분포에 근접
    # stats.probplot(df_pairs["Index"], dist="norm", plot=plt)


    df_pairs.to_excel("C:/Users/S/Desktop/ma.xlsx")



con.close()