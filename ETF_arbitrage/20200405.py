import pandas as pd
import numpy as np
import sqlite3
import os
os.getcwd()
os.chdir("c:/Users/S/Desktop/바탕화면(임시)/ETF/tmp/")


df_ETF_index = pd.read_excel("C:/Users/S/Desktop/ETF기초지수.xlsx")

def fine_ETFindex_code_multiple(df_ETF_index, index_name) :
    df1 = df_ETF_index[df_ETF_index["추적지수명"] == "%s" % index_name].iloc[:,[0,3]]
    return df1

baseindex = "F-KOSPI200"
df_index = fine_ETFindex_code_multiple(df_ETF_index,baseindex)
code1 = df_index.iloc[0,0]

con = sqlite3.connect("ETF.db")
df = pd.read_sql("select * from %s" %code1, con, index_col=None)
df.columns



# 이동평균선
df["ma5"] = df["Close"].rolling(window=5).mean()
diff = np.log(df["ma5"]) - np.log(df["ma5"]).shift(1)
df["diff"] = diff
df["diff"].plot()




con.close()