import pandas as pd
import numpy as np
import sqlite3 as sql
import os
import statsmodels.api as stm

# popular corr = sample corr ??
os.getcwd()
os.chdir("C:/Users/S/Desktop/바탕화면(임시)/ETF/")
con = sql.connect("ETF.db")

df_ETF_index = pd.read_excel("C:/Users/S/Desktop/ETF기초지수.xlsx")
df_ETF_index_code = list(df_ETF_index["종목코드"])
code = df_ETF_index_code[0]
code2 = df_ETF_index_code[55]
df = pd.read_sql("Select * from %s" %code, con, index_col=None)
df2 = pd.read_sql("Select * from %s" %code2, con, index_col=None)
con.close()


# sample corr 직접 계산과정
df_merge = pd.DataFrame()
df_p1 = pd.DataFrame(df.iloc[0:1043,1])
df_p2 = pd.DataFrame(df2.iloc[:,1])
df_p1["s_diff"] = df_p1["Close"] - df_p1["Close"].mean()
df_p2["s_diff"] = df_p2["Close"] - df_p2["Close"].mean()
df_merge["s_diff"] = df_p1["s_diff"]*df_p2["s_diff"]
s_cov = df_merge["s_diff"].sum()/(len(df_merge["s_diff"])-1) # s_cov
s1 = df_p1["Close"].std(ddof=1) # sample_std1
s2 = df_p2["Close"].std(ddof=1) # sample_std2
s_corr = s_cov/(s1*s2) # sample_corr

# popular corr 직접 계산과정
df_merge = pd.DataFrame()
df_p1 = pd.DataFrame(df.iloc[0:1043,1])
df_p2 = pd.DataFrame(df2.iloc[:,1])
df_p1["p_diff"] = df_p1["Close"] - df_p1["Close"].mean()
df_p2["p_diff"] = df_p2["Close"] - df_p2["Close"].mean()
df_merge["p_diff"] = df_p1["p_diff"]*df_p2["p_diff"]
p_cov = df_merge["p_diff"].sum()/(len(df_merge["p_diff"])) # p_cov
s1 = df_p1["Close"].std(ddof=0) # popular_std1
s2 = df_p2["Close"].std(ddof=0) # popular_std2
p_corr = p_cov/(s1*s2) # sample_corr

# 같음 확인
s_corr
p_corr
np.corrcoef(df.iloc[0:1043,1],df2.iloc[:,1])[0][1]


