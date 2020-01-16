"""
Data 시각화 연습

"""

import sqlite3
import pandas as pd

con = sqlite3.connect("C:/Users/S/desktop/바탕화면(임시)/KOSPI/tmp/KOSPI_PriceFinance_DB.db")

df = pd.read_sql("select Date, Close, BPS from A000020",con,index_col=None)
df
df = df.fillna(method="pad")
df = df[~df["BPS"].isna()]


df.insert(len(df.columns), "PBR",df["Close"]/df["BPS"])
df.to_csv("C:/users/S/desktop/dd.csv")
df.plot
df.plot(x ='Date', y=['PBR'])


con.close()

