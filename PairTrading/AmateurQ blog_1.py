import pandas as pd
import numpy as np
import sqlite3 as sql
import os
import matplotlib.pyplot as plt

os.chdir("C:/Users/S/Desktop/바탕화면(임시)/ETF/")
df_ETF_index = pd.read_excel("C:/Users/S/Desktop/ETF기초지수.xlsx")
df_ETF_index_code = list(df_ETF_index["종목코드"])


code1 = df_ETF_index[df_ETF_index["종목명"] == "KODEX 200"]["종목코드"].iloc[0]
code2 = df_ETF_index[df_ETF_index["종목명"] == "KODEX 레버리지"]["종목코드"].iloc[0]

con = sql.connect("ETF.db")

# KODEX200, KODEX 레버리지 데이터 이용
df_200 = pd.read_sql("Select * from %s" %code1, con, index_col=None)
df_lev = pd.read_sql("Select * from %s" %code2, con, index_col=None)

con.close()

Date = pd.date_range("20100601","20120201")
df_merg1 = pd.DataFrame(data= Date, columns=["Date"])

def to_Datetime(df) :
    df["Date"] = df["Date"].astype(str)
    df["Date"] = pd.to_datetime(df["Date"])
    return df
df_200 = to_Datetime(df_200)
df_lev = to_Datetime(df_lev)

df_merg1 = df_merg1.merge(df_200, on="Date")
df_merg1 = df_merg1.merge(df_lev, on="Date")
df_merg1= df_merg1.iloc[:,[0,1,3]]
df_merg1.columns = ["Date", "200_C", "lev_C"]
df_merg1


# 시각화
fig = plt.figure(figsize=(15,5))
ax = plt.subplot()
ax.plot(df_merg1["Date"], df_merg1["200_C"])
ax2 = ax.twinx() # diff scale , twin axis
ax2.plot(df_merg1["Date"], df_merg1["lev_C"], color="red")

# 로그 스케일 누적 return으로 비교
df_merg1["log_200"] = np.log(df_merg1["200_C"])
df_merg1["log_lev"] = np.log(df_merg1["lev_C"])

df_merg1["dif_log_200"] = df_merg1["log_200"] - df_merg1["log_200"].shift(1)+1
df_merg1["dif_log_lev"] = df_merg1["log_lev"] - df_merg1["log_lev"].shift(1)+1
df_merg1= df_merg1.fillna(1)
df_merg1["r_log_200"] = df_merg1["dif_log_200"].cumprod()
df_merg1["r_log_lev"] = df_merg1["dif_log_lev"].cumprod()
df_merg1["r_log_200"] = df_merg1["r_log_200"]-1
df_merg1["r_log_lev"] = df_merg1["r_log_lev"]-1



# normalized price
avg_200 = df_merg1["200_C"].mean()
avg_lev = df_merg1["lev_C"].mean()
std_200 = df_merg1["200_C"].std(ddof=1)
std_lev = df_merg1["lev_C"].std(ddof=1)

df_merg1["n_200_c"] = (df_merg1["200_C"] - avg_200)/std_200
df_merg1["n_lev_c"] = (df_merg1["lev_C"] - avg_lev)/std_lev


# 시각화
fig = plt.figure(figsize=(15,5))
fig.suptitle('log_r vs normalized') # 제목

ax = plt.subplot(1,2,1)
ax.plot(df_merg1["Date"], df_merg1["r_log_200"]*2)
ax.plot(df_merg1["Date"], df_merg1["r_log_lev"])

ax = plt.subplot(1,2,2)
ax.plot(df_merg1["Date"], df_merg1["n_200_c"])
ax.plot(df_merg1["Date"], df_merg1["n_lev_c"])

# spread 비교
df_merg1["sp_log_r"] = df_merg1["r_log_200"] - df_merg1["r_log_lev"]
df_merg1["sp_n"] = df_merg1["n_200_c"] - df_merg1["n_lev_c"]

fig = plt.figure(figsize=(15,5))
fig.suptitle('log_r vs normalized') # 제목

ax = plt.subplot(1,2,1)
ax.plot(df_merg1["Date"], df_merg1["sp_log_r"])

ax = plt.subplot(1,2,2)
ax.plot(df_merg1["Date"], df_merg1["sp_n"])


# normalized spread 구해보기
import pandas as pd
import numpy as np
import sqlite3 as sql
import os
import matplotlib.pyplot as plt

os.chdir("C:/Users/S/Desktop/바탕화면(임시)/ETF/")
df_ETF_index = pd.read_excel("C:/Users/S/Desktop/ETF기초지수.xlsx")
df_ETF_index_code = list(df_ETF_index["종목코드"])


code1 = df_ETF_index[df_ETF_index["종목명"] == "KODEX 200"]["종목코드"].iloc[0]
code2 = df_ETF_index[df_ETF_index["종목명"] == "KODEX 레버리지"]["종목코드"].iloc[0]

con = sql.connect("ETF.db")

# KODEX200, KODEX 레버리지 데이터 이용
df_200 = pd.read_sql("Select * from %s" %code1, con, index_col=None)
df_lev = pd.read_sql("Select * from %s" %code2, con, index_col=None)

con.close()

Date = pd.date_range("20010101","20200201")
df_merg1 = pd.DataFrame(data= Date, columns=["Date"])

def to_Datetime(df) :
    df["Date"] = df["Date"].astype(str)
    df["Date"] = pd.to_datetime(df["Date"])
    return df
df_200 = to_Datetime(df_200)
df_lev = to_Datetime(df_lev)

df_merg1 = df_merg1.merge(df_200, on="Date")
df_merg1 = df_merg1.merge(df_lev, on="Date")
df_merg1= df_merg1.iloc[:,[0,1,3]]
df_merg1.columns = ["Date", "200_C", "lev_C"]
df_merg1

# normalized price
avg_200 = df_merg1["200_C"].mean()
avg_lev = df_merg1["lev_C"].mean()
std_200 = df_merg1["200_C"].std(ddof=1)
std_lev = df_merg1["lev_C"].std(ddof=1)

df_merg1["n_200_c"] = (df_merg1["200_C"] - avg_200)/std_200
df_merg1["n_lev_c"] = (df_merg1["lev_C"] - avg_lev)/std_lev


# 시각화
def show_plt(df1) :
    fig = plt.figure(figsize=(15,5))
    ax = plt.subplot()
    ax.plot(df1["Date"], df1["n_200_c"])
    ax.plot(df1["Date"], df1["n_lev_c"])
    return True

show_plt(df_merg1)

# normalized spread price
df_merg1["sp_n"] = df_merg1["n_200_c"] - df_merg1["n_lev_c"]
df_merg1["sp_n"].plot()


# 비율 spread 구해보기
import pandas as pd
import numpy as np
import sqlite3 as sql
import os
import matplotlib.pyplot as plt

os.chdir("C:/Users/S/Desktop/바탕화면(임시)/ETF/")
df_ETF_index = pd.read_excel("C:/Users/S/Desktop/ETF기초지수.xlsx")
df_ETF_index_code = list(df_ETF_index["종목코드"])


code1 = df_ETF_index[df_ETF_index["종목명"] == "KODEX 200"]["종목코드"].iloc[0]
code2 = df_ETF_index[df_ETF_index["종목명"] == "KODEX 레버리지"]["종목코드"].iloc[0]

con = sql.connect("ETF.db")

# KODEX200, KODEX 레버리지 데이터 이용
df_200 = pd.read_sql("Select * from %s" %code1, con, index_col=None)
df_lev = pd.read_sql("Select * from %s" %code2, con, index_col=None)

con.close()

Date = pd.date_range("20010101","20200201")
df_merg1 = pd.DataFrame(data= Date, columns=["Date"])

def to_Datetime(df) :
    df["Date"] = df["Date"].astype(str)
    df["Date"] = pd.to_datetime(df["Date"])
    return df
df_200 = to_Datetime(df_200)
df_lev = to_Datetime(df_lev)

df_merg1 = df_merg1.merge(df_200, on="Date")
df_merg1 = df_merg1.merge(df_lev, on="Date")
df_merg1= df_merg1.iloc[:,[0,1,3]]
df_merg1.columns = ["Date", "200_C", "lev_C"]
df_merg1["r-sp"] = df_merg1["200_C"]/df_merg1["lev_C"]
df_merg1["r-sp"].plot()

df_merg1["log_200"] = np.log(df_merg1["200_C"])
df_merg1["log_lev"] = np.log(df_merg1["lev_C"])
df_merg1["log_sp"] = df_merg1["log_200"]- df_merg1["log_lev"]
df_merg1["log_sp"].plot()

# cointegration coefficient 구해서 로그스프레드 구하기
import statsmodels.api as stm
m = stm.formula.ols(formula="log_200~log_lev", data=df_merg1)
r = m.fit()
df_merg1["hat_log_200"] = r.fittedvalues
df_merg1["log_sp2"] = df_merg1["log_200"]- df_merg1["hat_log_200"]

df_merg1["hat_log_200"].plot()
df_merg1["log_200"].plot()

plt.plot(df_merg1["log_200"],df_merg1["log_lev"], "bo")


# SK에너지 , LG화학 페어 분석해보기
import pandas as pd
import numpy as np
import sqlite3 as sql
import os
import matplotlib.pyplot as plt
import statsmodels.api as stm

os.chdir("C:/Users/S/Desktop/바탕화면(임시)/KOSPI/tmp/")
con = sql.connect("KOSPI_Price_DB_merge_final.db")
df_sk = pd.read_sql("Select Date, Close from A096770", con, index_col=None)
df_lg = pd.read_sql("Select Date, Close from A051910", con, index_col=None)

con.close()

date = pd.date_range("20080101","20130101")
df_tmp = pd.DataFrame({"Date":date})
df_sk["Date"] = pd.to_datetime(df_sk["Date"])
df_lg["Date"] = pd.to_datetime(df_lg["Date"])

df_merg1 = pd.merge(df_tmp,df_sk, on="Date", how="left")
df_merg1 = pd.merge(df_merg1,df_lg, on="Date", how="left")
df_merg1 = df_merg1.dropna()
df_merg1["log_sk"] = np.log(df_merg1.iloc[:,1])
df_merg1["log_lg"] = np.log(df_merg1.iloc[:,2])
m = stm.formula.ols("log_lg~log_sk", data=df_merg1)
r = m.fit()
r.summary()
df_merg1.corr()
plt.plot(df_merg1["log_sk"],df_merg1["log_lg"], "bo")

df_merg1["hat_log_lg"] = r.params["log_sk"]*df_merg1["log_sk"]
df_merg1["sp"] = df_merg1["log_lg"] - df_merg1["hat_log_lg"]
df_merg1["hat_log_lg"].plot()
df_merg1["log_lg"].plot()
plt.plot(df_merg1["sp"])



# 현대백화점, 롯데쇼핑 페어 분석해보기
import pandas as pd
import numpy as np
import sqlite3 as sql
import os
import matplotlib.pyplot as plt
import statsmodels.api as stm

os.chdir("C:/Users/S/Desktop/바탕화면(임시)/KOSPI/tmp/")
con = sql.connect("KOSPI_Price_DB_merge_final.db")
df_hyun = pd.read_sql("Select Date, Close from A069960", con, index_col=None)
df_lotte = pd.read_sql("Select Date, Close from A023530", con, index_col=None)

con.close()

date = pd.date_range("20090901", "20120222")
df_tmp = pd.DataFrame({"Date":date})
df_hyun["Date"] = pd.to_datetime(df_hyun["Date"])
df_lotte["Date"] = pd.to_datetime(df_lotte["Date"])

df_merg1 = pd.merge(df_tmp,df_hyun, on="Date", how="left")
df_merg1 = pd.merge(df_merg1,df_lotte, on="Date", how="left")
df_merg1 = df_merg1.dropna()
df_merg1["log_hyun"] = np.log(df_merg1.iloc[:,1])
df_merg1["log_lotte"] = np.log(df_merg1.iloc[:,2])
m = stm.formula.ols("log_lotte~log_hyun", data=df_merg1)
r = m.fit()
r.summary()
df_merg1.corr()

df_merg1["hat_log_lotte"] = r.fittedvalues
df_merg1["sp"] = df_merg1["log_lotte"] - df_merg1["hat_log_lotte"]
df_merg1["hat_log_lotte"].plot()
df_merg1["log_lotte"].plot()
plt.plot(df_merg1["sp"])
plt.hist(df_merg1["sp"],bins=200)


# 스프레드 정규성 검정해보기
# 삼성전자, 삼성전자(우) 페어

import pandas as pd
import numpy as np
import sqlite3 as sql
import os
import matplotlib.pyplot as plt
import statsmodels.api as stm
import pandas_datareader.data as web

start = '2009-09-29'
end = '2012-02-28'
df_sam = web.DataReader("005930.KS", "yahoo", start, end) # 날짜 지정안하면 최근 5개년치 데이터 불러옴
df_samwoo = web.DataReader("005935.KS", "yahoo", start, end) # 날짜 지정안하면 최근 5개년치 데이터 불러옴
df_sam = pd.DataFrame({"Date":df_sam.index,
                       "Close" : df_sam["Close"]})
df_samwoo = pd.DataFrame({"Date":df_samwoo.index,
                       "Close" : df_samwoo["Close"]})

df_sam.index = [i for i in range(0,len(df_sam))]
df_samwoo.index = [i for i in range(0,len(df_sam))]

df_merg1 = pd.merge(df_sam, df_samwoo, on="Date",how="left")
df_merg1.columns = ["Date", "C_sam", "C_samwoo"]
df_merg1["log_sam"] = np.log(df_merg1["C_sam"])
df_merg1["log_samwoo"] = np.log(df_merg1["C_samwoo"])

m = stm.formula.ols("log_sam~log_samwoo", data=df_merg1)
r = m.fit()
r.summary()
df_merg1["hat_log_sam"] = r.fittedvalues
df_merg1["sp"] = df_merg1["hat_log_sam"]-df_merg1["log_sam"]
df_merg1["sp"].plot()


