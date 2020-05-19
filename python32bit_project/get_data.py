from CP import Cybos_mod as cm
import pandas as pd
import sqlite3 as sql
import os

# os.chdir("C:/Users/S/Desktop/바탕화면(임시)/KOSPI/")
# con = sql.connect("kospi_price.db")
kospi1 = cm.CP_KOSPI()
# kospi1.login_CP()
# kospi1.CP_login_status()
# help(kospi1)

# codelist = kospi1.Get_code_by_seckind("주권")
# codename = kospi1.Get_name_by_seckind("주권")

# code = codelist[0]
Sdate = 20011201
Edate = 20200301

df1 = kospi1.Get_Data(code = "U001", Sdate= 20011201, Edate= 20080811)
df2 = kospi1.Get_Data(code = "U001", Sdate= 20080812, Edate= 20100112)
df3 = kospi1.Get_Data(code = "U001", Sdate= Sdate, Edate= Edate)
df4 = pd.concat([df1,df2,df3])
df4 = df4.sort_values(by="Date")
df4.index = [i for i in range(len(df4.index))]
df4["Date"][0].year
df4["Date"][0].month
df4["Date"][0].day
df4["index"] = [df4["Date"][i].day for i in range(len(df4["Date"]))]
df4 = df4[df4["index"]>=20]
df4["index2"] = [str(df4["Date"].iloc[i].year) + "-" + str(df4["Date"].iloc[i].month) for i in range(len(df4["Date"]))]
df4.groupby()
dir(df4)
help(df4.groupby["index2"].mean())
df_last = df4.groupby(["index2"]).mean()
df_last.columns
df_last["Mcap"]
df_money = pd.read_csv("C:/Users/S/Desktop/BOK_Data.csv", encoding="euc-kr")
df_last
df_last["Date"] = df_last.index
df_last.index = [i for i in range(len(df_last.index))]
df_money
df_merge = pd.concat([df_last[["Mcap","Date"]],df_money[["Date","M2"]]], axis=1)


df_merge = df_merge.iloc[:,[0,2,3]]
df_merge

import matplotlib.pyplot as plt
plt.subplot(1,2,1)
plt.plot(df_merge.iloc[:,0])
plt.subplot(1,2,2)
plt.plot(df_merge.iloc[:,2])

df_merge["bubble"] = df_merge["Mcap"]/df_merge["M2"]
plt.plot(df_merge["bubble"])
plt.plot(df_merge["bubble"])
plt.plot(df_merge.iloc[:,2])
df_last["Close"]

fig = plt.figure(figsize=(15,5))
ax = plt.subplot()
ax.plot(df_merge["bubble"])
ax2 = ax.twinx() # diff scale , twin axis
ax2.plot(df_last["Close"], color="red")
df_last["Close"]
df_my = pd.concat([df_last["Close"],df_merge["bubble"]], axis=1)
df_my["index"] = [df_my.iloc[i,0] if df_my["bubble"].iloc[i] < 0.0025 else 0 for i in range(len(df_my.index))]
df_my["index2"] = [df_my.iloc[i,0] if df_my["bubble"].iloc[i] > 0.005 else 0 for i in range(len(df_my.index))]
df_my


df_my["Close"].plot(color="black")
df_my["index"].plot(color="red")
df_my["index2"].plot(color="blue")
fb["Profit"] = [(fb.loc[i,"Price1"]/fb.loc[i, "Adj Close"]) if fb.loc[i,"Shares"] == 1 else 1
                for i in fb.index]