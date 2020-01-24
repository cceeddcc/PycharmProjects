"""
PBR데이터에 대한 분석

"""
import sqlite3
import pandas as pd
import numpy as np
import time
import matplotlib.pyplot as plt


# 종목명, 코드 불러오기
with open("C:\\Users\\S\\Desktop\\바탕화면(임시)\\KOSPI\\KOSPI_codelist.txt", "r") as f :
    code_list = [line.split("\n")[0] for line in f.readlines()]

# 데이터 불러오기 및 정제
con = sqlite3.connect("C:/Users/S/desktop/바탕화면(임시)/KOSPI/tmp/KOSPI_PriceFinance_DB.db")
df = pd.read_sql("select Date, Close, BPS from A000020",con,index_col=None)
df = df.fillna(method="pad")
df = df[~df["BPS"].isna()]
df.insert(len(df.columns), "PBR", df["Close"] / df["BPS"])

df.index = range(len(df["Date"]))

for i in range(len(df["Date"])) :
    df["Date"][i] = df["Date"][i].split("-")[0]

Year_index = df.groupby("Date").mean().index

# 알고리즘 조건 적용
buy_price = []
sell_price = []
Trade = {}
for Year in Year_index :
    Year = "2017" #tmp
    mean1 = "{0:.4f}".format(df.groupby('Date').mean()["PBR"]["%s" %Year] )
    std1 = "{0:.4f}".format(df.groupby('Date').std()["PBR"]["%s" %Year] )
    con_high = float(mean1) + 2* float(std1)
    con_low = float(mean1) - 2* float(std1)

    a = df[df["Date"]=="%s" %str(int(Year)+1)]
    buy_index = list(a[a["PBR"] < con_low].index)
    sell_index = list(a[a["PBR"] > con_high].index)

    #############################################################################

    buy_index = [1,2,3,7,8,9] #tmp
    sell_index = [4,5,10,11] #tmp

    a3 = []
    for a1 in buy_index :
        for a2 in sell_index:
            if a1<a2 :
                a3.append(a1)
            else: continue

        sell_index[sell_index>a1]
        print(a1)

    buy_index = pd.Series(a[a["PBR"] < con_low].index)
    sell_index = pd.Series(a[a["PBR"] > con_high].index)



    buyone, sellone = min(buy_index), min(sell_index)
    if min(buy_index) < min(sell_index) :
        Trade["%s" % Year] = (buyone,sellone)
    else :
        buyone,sellone = min(buy_index),min(sell_index)
        Trade["%s" %Year] = buyone
        Trade["%s" %str(int(Year)-1)] = sellone



    for con1 in buy_index :
        try :
            buy_price.append(a["Close"][con1])
            sell_price.append(a["Close"][sell_index[sell_index > 328].iloc[0]])
        except : continue





    sell_index[]

if a[a["PBR"]<con_low].index < a[a["PBR"]>con_high].index[0] :
    buy_price = a["Close"][a[a["PBR"] < con_low].index]  # 매수
    sell_price = a["Close"][a[a["PBR"] > con_high].index[0]]  # 매도
else :

((sell_price/buy_price)-1)*100 # 수익률



type(df["Date"][0])

df
df.groupby()
df["Date"]


df = pd.DataFrame({'A': ['foo', 'bar', 'foo', 'bar', 'foo', 'bar', 'foo', 'foo'],
                   'B': ['one', 'one', 'two', 'three', 'two', 'two', 'one', 'three'],
                   'C': np.random.randn(8),
                   'D': np.random.randn(8)})
df
df.groupby('A').sum() # A열의 데이터를 기준으로 묶어서 각각 계산수행
df.groupby(['A', 'B']).sum() # 기준을 여러개 지정 가능

con.close()
















for code in code_list :
    try :
            print(i, "/", len(code_list))
            i += 1
            df = pd.read_sql("select Date, Close, BPS from %s" %code,con,index_col=None)
            df = df.fillna(method="pad")
            df = df[~df["BPS"].isna()]
            df.insert(len(df.columns), "%s PBR" %code, df["Close"] / df["BPS"])
            df_concat = pd.concat(df_concat,df["%s PBR"] %code, axis=1)



            #
            # df = df[df["PBR"]>0]
            # df = df[df["PBR"]<20]
            # PBR_dict["%s" %code] = ["{0:.3f}".format(min(df["PBR"])),
            #                        "{0:.3f}".format(np.mean(df["PBR"])),
            #                        "{0:.3f}".format(max(df["PBR"]))]
            #
            # fig, ax = plt.subplots()
            # ax.plot(df["PBR"], color="red", lw=1)
            # fig.tight_layout()

            # time.sleep(60)

    except : continue



con.close()


min_PBR = [values[0] for values in PBR_dict.values()]
avg_PBR = [values[1] for values in PBR_dict.values()]
max_PBR = [values[2] for values in PBR_dict.values()]

df1 = pd.DataFrame({"min_PBR" : min_PBR,
              "avg_PBR" : avg_PBR,
              "max_PBR" : max_PBR})

df1 = df1.sort_values(by="avg_PBR")
index = range(len(df1.index))
df1.index = index
df1.to_csv("C:\\Users\\S\\Desktop\\pbr.csv")
fig, ax = plt.subplots()
ax.plot(df1["min_PBR"], color="blue", lw=1)
ax.plot(df1["avg_PBR"], color="black", lw=1)
ax.plot(df1["max_PBR"], color="red", lw=1)
fig.tight_layout()

plt.show()