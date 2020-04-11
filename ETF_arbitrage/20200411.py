import pandas as pd
import sqlite3 as sql
import numpy as np
import statsmodels.api as stm
import os
import matplotlib.pyplot as plt

# trend를 제거한 log diff close의 corr 값은 유효한가 ?
# 동일한 기초자산을 추종하는 ETF 데이터로 확인 해보자

os.chdir("c:/Users/S/Desktop/바탕화면(임시)/ETF/")
df_ETF_index = pd.read_excel("C:/Users/S/Desktop/ETF기초지수.xlsx")
df_ETF_index_code = list(df_ETF_index["종목코드"])

con = sql.connect("ETF.db")

# 동일 기초자산, 인버스와 비교
code = df_ETF_index_code[0]
code2 = df_ETF_index_code[1]
df_ETF_index[df_ETF_index["종목코드"] == df_ETF_index_code[0]]
df_ETF_index[df_ETF_index["종목코드"] == df_ETF_index_code[1]]

df = pd.read_sql("Select * from %s" %code, con, index_col= None)
df2 = pd.read_sql("Select * from %s" %code2, con, index_col= None)

con.close()

df_pair = pd.DataFrame()
df_pair["Date"] = df["Date"]
df_pair["p1_C"] = df["Close"]
df_pair = df_pair.merge(df2[["Date","Close"]], on="Date")
df_pair = df_pair.dropna()
df_pair.columns = ['Date', 'p1_C', 'p2_C']

df_pair["log_p1"] = np.log(df_pair["p1_C"])
df_pair["log_p2"] = np.log(df_pair["p2_C"])
df_pair["diff_p1"] = df_pair["log_p1"] - df_pair["log_p1"].shift(1)
df_pair["diff_p2"] = df_pair["log_p2"] - df_pair["log_p2"].shift(1)
df_pair = df_pair.dropna()
df_corr = df_pair.corr()

# 결과적으로 추세를 제거한 것이 더 상관관계를 잘 보여주는 것으로 보임
df_corr.loc["log_p1","log_p2"]
df_corr.loc["diff_p1","diff_p2"] # 추세 제거

# pair 스프레드 확인
m = stm.formula.ols("diff_p2~diff_p1", data=df_pair)
r = m.fit()
r.summary() # 유의미한 coefficient
df_pair["diff_p2_hat"] = r.predict()

df_pair["Sp"] = df_pair["diff_p2"] - df_pair["diff_p2_hat"]
df_pair["Sp"].plot()
df_pair["Sp"].hist(bins=200)

df_pair[df_pair["Sp"]==df_pair["Sp"].max()]
df_pair.loc[143:144,:]
df_pair[df_pair["Sp"]==df_pair["Sp"].min()]
df_pair.loc[1557:1558,:]


((54125+52400)/(54715+51970)-1)*100
((71920+45285)/(72280+45030)-1)*100

stm.stats.jarque_bera(df_pair["Sp"])
stm.stats.jarque_bera(np.random.normal(0,1,10000))


# 동일 기초자산 비교
con = sql.connect("ETF.db")
code = df_ETF_index_code[74]
code2 = df_ETF_index_code[75]
df_ETF_index[df_ETF_index["추적지수명"]=="KOSPI200"]
df_ETF_index[df_ETF_index["종목코드"] == df_ETF_index_code[0]]
df_ETF_index[df_ETF_index["종목코드"] == df_ETF_index_code[1]]

df = pd.read_sql("Select * from %s" %code, con, index_col= None)
df2 = pd.read_sql("Select * from %s" %code2, con, index_col= None)

con.close()








# 직접 data generating 해서 결과 확인

# random walk
data1 = [1000]
for i in range(1,10000):
    data1.append(data1[i-1] + np.random.normal(0, 5, 1)[0])

data2 = [10000]
for i in range(1, 10000):
    data2.append(data2[i - 1] + np.random.normal(0, 30, 1)[0])


df_pair2 = pd.DataFrame({"data1" : data1,
                         "data2" : data2})


df_pair2["log_p1"] = np.log(df_pair2["data1"])
df_pair2["log_p2"] = np.log(df_pair2["data2"])
df_pair2["diff_p1"] = df_pair2["log_p1"] - df_pair2["log_p1"].shift(1)
df_pair2["diff_p2"] = df_pair2["log_p2"] - df_pair2["log_p2"].shift(1)
df_pair2= df_pair2.dropna()
df_pair2.corr()

# 우연히 trend로 인해 corr이 높게 나올 수 있는 문제 diff로 해결
df_corr2 = df_pair2.corr()
df_corr2.loc["log_p1","log_p2"]
df_corr2.loc["diff_p1","diff_p2"] # 추세 제거

# pair 스프레드 확인
m = stm.formula.ols("log_p2~log_p1", data=df_pair2)
r = m.fit()
r.summary()
df_pair2["log_p2_hat"] = r.predict()

df_pair2["Sp"] = df_pair2["log_p2"] - df_pair2["log_p2_hat"]
df_pair2["Sp"].plot() # 우연히 corr이 높은 경우 스프레드는 발산하는 모습
df_pair2["Sp"].hist(bins=200) # spread는 정규분포를 따르지 않음



# 추세가 있는 random walk
data1 = [1000]
for i in range(1,10000):
    data1.append(data1[i-1] + np.random.normal(0, 5, 1)[0]+1)

data2 = [10000]
for i in range(1, 10000):
    data2.append(data2[i - 1] + np.random.normal(0, 30, 1)[0]+12)


df_pair2 = pd.DataFrame({"data1" : data1,
                         "data2" : data2})


df_pair2["log_p1"] = np.log(df_pair2["data1"])
df_pair2["log_p2"] = np.log(df_pair2["data2"])
df_pair2["diff_p1"] = df_pair2["log_p1"] - df_pair2["log_p1"].shift(1)
df_pair2["diff_p2"] = df_pair2["log_p2"] - df_pair2["log_p2"].shift(1)
df_pair2= df_pair2.dropna()
df_pair2.corr()

# 우연히 trend로 인해 corr이 높게 나올 수 있는 문제 diff로 해결
df_corr2 = df_pair2.corr()
df_corr2.loc["log_p1","log_p2"] # trend로 인한 corr 높게나타남
df_corr2.loc["diff_p1","diff_p2"] # 추세 제거

# pair 스프레드 확인
m = stm.formula.ols("log_p2~log_p1", data=df_pair2)
r = m.fit()
r.summary()
df_pair2["log_p2_hat"] = r.predict()

df_pair2["Sp"] = df_pair2["log_p2"] - df_pair2["log_p2_hat"]
df_pair2["Sp"].plot() # 추세로 인해 corr이 높은 경우 스프레드는 발산하는 모습
df_pair2["Sp"].hist(bins=200) # spread는 정규분포를 따르지 않음







