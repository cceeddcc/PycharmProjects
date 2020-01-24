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

# 일별 PBR 데이터 만들어 넣기
df.insert(len(df.columns), "PBR",df["Close"]/df["BPS"])
# df.to_csv("C:/users/S/desktop/dd.csv")

con.close()

# 시각화
import matplotlib.pyplot as plt
import matplotlib


data1 = df["Close"]
data2 = df["PBR"]

fig, ax1 = plt.subplots()

color = 'tab:red'
ax1.set_xlabel('time') # x축 label 설정
ax1.set_ylabel('Close', color=color) # y축 label 설정
ax1.plot(data1, color=color)
ax1.tick_params(axis='y', labelcolor=color) # y축 label 색 지정

ax2 = ax1.twinx()  # x축 공유하는 새로운 y축 추가

color = 'tab:blue'
ax2.set_ylabel('PBR', color=color)  # we already handled the x-label with ax1
ax2.plot(data2, color=color)
ax2.tick_params(axis='y', labelcolor=color) # y축 label 색 지정

fig.tight_layout()  # 화면 레이아웃 맞추기
plt.show()

# 100일 평균 PBR 그리기
rollingdata= df["PBR"].rolling(window=100).mean()
fig, ax1 = plt.subplots()
ax1.plot(rollingdata)
ax1.plot(df["PBR"], color = "blue")
dir(ax1)
fig.tight_layout()

# 알고리즘
df.insert(len(df.columns),"PBR_100MA", rollingdata)
df = df[~df["PBR_100MA"].isna()]
df.insert(len(df.columns),"test", df["PBR_100MA"]-df["PBR"])
# a = [df["Close"] for test in list(df["test"]) if test > 0]

a = df["Close"][df["test"] >0]
fig, ax1 = plt.subplots()
matplotlib.markers = "."

ax1.plot(a, color = "green")
ax1.plot(df["Close"],color ="red")
plt.show()


import numpy as np
import matplotlib.pyplot as plt

y = np.array([np.NAN, 45, 23, np.NAN, 5, 14, 22, np.NAN, np.NAN, 18, 23])
x = np.arange(0, len(y))
mask = np.isfinite(y)

fig, ax = plt.subplots()
line, = ax.plot(x[mask],y[mask], ls="--",lw=1)
ax.plot(x,y, color=line.get_color(), lw=1.5)

plt.show()

df["test"]>0
df["Date"]
from datetime import datetime
df["Date"]= pd.to_datetime(df["Date"])
df.iloc[:,0:2]


index = df.index
df2 = df
df2 = df[df["test"]>0]
df2 = df2.reindex(index)
fig, ax1 = plt.subplots()
ax1.plot(df2["Close"])

fig, ax1 = plt.subplots()
line = ax1.plot(df2["Close"], ls="--",lw=1)
ax1.plot(df["Close"], color=line.get_color(), lw=1.5)


ax.plot(x,y, color=line.get_color(), lw=1.5)

import numpy as np
import matplotlib.pyplot as plt

y = np.array([np.NAN, 45, 23, np.NAN, 5, 14, 22, np.NAN, np.NAN, 18, 23])
x = np.arange(0, len(y))
mask = np.isfinite(y)

fig, ax = plt.subplots()
line, = ax.plot(x[mask],y[mask], ls="--",lw=1)
ax.plot(x,y, color="red", lw=1.5)

plt.show()

import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
con = sqlite3.connect("C:/Users/S/desktop/바탕화면(임시)/KOSPI/tmp/KOSPI_PriceFinance_DB.db")
df = pd.read_sql("select Date, Close, BPS from A000020",con,index_col=None)
df = df.fillna(method="pad")
df = df[~df["BPS"].isna()]
df.insert(len(df.columns), "PBR",df["Close"]/df["BPS"])
# 100일 평균 PBR 그리기
rollingdata= df["PBR"].rolling(window=100).mean()
# 알고리즘
df.insert(len(df.columns),"PBR_100MA", rollingdata)
df = df[~df["PBR_100MA"].isna()]
df.insert(len(df.columns),"test", df["PBR_100MA"]-df["PBR"])

df
df2 = df[df["test"]>0]
df2 = df2[df2["PBR"]<0.7]
df3 = df[df["test"]<0]
newindex = df.index
df2 = df2.reindex(newindex)
df3 = df3.reindex(newindex)


fig, ax = plt.subplots()
line, = ax.plot(df2["Close"], lw=1.5, color = "red")
ax.plot(df3["Close"], color="blue", lw=1.5)
fig.tight_layout()

plt.show()

con.close()





