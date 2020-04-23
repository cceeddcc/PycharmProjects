import pandas as pd
import numpy as np
import sqlite3 as sql
import statsmodels.api as stm
import matplotlib.pyplot as plt
import os
from statsmodels.tsa.stattools import acf
from scipy import stats, integrate

pd.options.mode.chained_assignment = None

# 종목명, 코드 불러오기
def road_codename():
    """
    종목명, 코드 불러오기 위함
    """
    with open("C:\\Users\\S\\Desktop\\바탕화면(임시)\\KOSPI\\KOSPI_codelist.txt", "r") as f:
        code_list = [line[1:].split("\n")[0] for line in f.readlines()]

    with open("C:\\Users\\S\\Desktop\\바탕화면(임시)\\KOSPI\\KOSPI_namelist.txt", "r") as f:
        name_list = [line.split("\n")[0] for line in f.readlines()]

    code_dict = {}
    for i in range(0, len(code_list)):
        code_dict["%s" % name_list[i]] = code_list[i]

    return code_dict, code_list, name_list
code_dict, code_list, name_list = road_codename()

# 페어 선정하기
# 3년치 데이터
os.chdir("C:/Users/S/Desktop/바탕화면(임시)/KOSPI/")

start = "2012-01-01"
end = "2015-01-01"
date = pd.date_range(start,end)
df_kospi = pd.DataFrame({"Date" : date})
con = sql.connect("KOSPI_Price_DB_merge_final.db")

t = 1
for code in code_list[:200] :
    print(t, " / " , len(code_list))
    code = "A" + code
    df = pd.read_sql("select Date, Close from %s" %code, con, index_col= None)
    df["Date"] = pd.to_datetime(df["Date"])
    df["log_%s" %code] = np.log(df["Close"])
    df = df.iloc[:,[0,2]]
    df = df[df["Date"]>=start]
    df = df[df["Date"]<=end]
    if len(df) < 740 :
        continue
    df_kospi = df_kospi.merge(df, how="left", on="Date")
    df_kospi.dropna()
    t += 1
con.close()

df_kospi = df_kospi.dropna()
df_kospi_test = df_kospi.iloc[:500, :]

# correlation 기준으로 페어 찾기
# 0.7이상
df_p = pd.DataFrame(data=None)
df_corr = df_kospi_test.corr()
for i in range(0,len(df_corr.columns)-1) :
    if abs(df_corr.iloc[i+1,i]) > 0.7 :
        s1 = pd.Series([df_corr.index[i+1],df_corr.columns[i],df_corr.iloc[i+1,i]])
        df_p = df_p.append(s1, ignore_index=True)

columns=["p1","p2","corr"]
df_p.columns = columns


# 공적분 계수 (CC) 찾기
# golden section search algorithm 사용
def find_cc_golden(upper, lower, p_df, error) :
    loop = 1000
    ratio = 0.618033
    ran = upper - lower

    for i in range(0,loop) :
        x1 = lower + ratio * ran
        x2 = upper - ratio * ran
        fx = []

        for x in [x1,x2] :
            # acf coef 계산
            p_df["hat_data"] = x*p_df.iloc[:,1]
            p_df["sp"] = p_df.iloc[:,0] - p_df["hat_data"]
            fx.append(acf(p_df["sp"],fft=False)[1])

        # golden section search algorithm
        if fx[0] > fx[1] : # f(x1) > f(x2)
            upper = x1
            ran = upper - lower
        else :
            lower = x2
            ran = upper - lower

        if ran < error :
            cc = (upper+lower)/ 2
            return cc, acf(p_df["sp"],fft=False)[1]
            break




# 시각화 확인
import math

k = 0
for j in range(0,math.ceil(len(df_p.index)/3)) :
    if j%3 == 0 :
        fig, axes_list = plt.subplots(3, 3, figsize=(20, 20), tight_layout=True)
        k = 0
    for i in range(3*j,3*(j+1)) :
        try :
            df_p_cal = df_kospi_test[[df_p.iloc[i, 0], df_p.iloc[i, 1]]]
            cc = find_cc_golden(10, -10, df_p_cal, 0.0000001)
            df_p_cal["hat_data"] = cc*df_p_cal.iloc[:,1]
            df_p_cal["sp"] = df_p_cal.iloc[:,0] - df_p_cal["hat_data"]
            df_p_cal["n_p1"] = (df_p_cal.iloc[:,0]-df_p_cal.iloc[:,0].mean())/df_p_cal.iloc[:,0].std(ddof=1)
            df_p_cal["n_p2"] = (df_p_cal["hat_data"]-df_p_cal["hat_data"].mean())/df_p_cal["hat_data"].std(ddof=1)
            df_p_cal["sc_sp"] = df_p_cal["sp"]-df_p_cal["sp"].mean()

            kde = stats.gaussian_kde(df_p_cal["sc_sp"])
            # upper 찾기
            xmin, xmax, xtmp = 0, 15, 15
            for t in range(0, 500):
                integral, err = integrate.quad(kde, xmin, xmax)
                if integral >= 0.05:
                    xmin = xmin + (xtmp - xmin) / 2
                elif integral <= 0.048:
                    xtmp = xmin
                    xmin = xmin / 2
                else:
                    upper = xmin
                    break
            # lower 찾기
            xmin, xmax, xtmp = -15, 0, -15
            for t in range(0, 500):
                integral, err = integrate.quad(kde, xmin, xmax)
                if integral >= 0.05:
                    xmax = xmax + (xtmp - xmax) / 2
                elif integral <= 0.048:
                    xtmp = xmax
                    xmax = xmax / 2
                else:
                    lower = xmax
                    break

            # 시각화
            axes_list[k][i-3*j].plot(df_p_cal["sc_sp"], '.-', linewidth = 0.8)
            axes_list[k][i-3*(j+1)].axhline(y=df_p_cal["sc_sp"].mean(), color="red", linestyle="--")
            axes_list[k][i-3*(j+1)].axhline(y=upper, color="blue", linestyle="--")
            axes_list[k][i-3*(j+1)].axhline(y=lower, color="blue", linestyle="--")

        except : continue
    k +=1


# back testing
# upper = 1.5sig, lower = -1.5sig
# spread upper short sp
# spread lower long sp
# 0 청산
# 500개 데이터씩 moving window
df_kospi.index = [i for i in range(0,len(df_kospi.index))]

index_num = []
for i in range(0,len(df_p.index)) :
    df_p_cal = df_kospi[[df_p.iloc[i,0],df_p.iloc[i,1]]]
    cc, acf_1 = find_cc_golden(10,-10,df_p_cal,0.000001)
    if acf_1 < 0.97 :
        index_num.append(i)
index_num
df_p = df_p.loc[index_num]
df_p.index = [i for i in range(0,len(df_p.index))]
df_p

for i in range(0,len(df_p.index)) :
    i = 0
    df_p_cal = df_kospi[[df_p.iloc[i,0],df_p.iloc[i,1]]]
    cc, acf_1 = find_cc_golden(10,-10,df_p_cal,0.000001)
    df_p_cal["hat_data"] = cc * df_p_cal.iloc[:, 1]
    df_p_cal["sp"] = df_p_cal.iloc[:, 0] - df_p_cal["hat_data"]
    df_p_cal["sc_sp"] = df_p_cal["sp"] - df_p_cal["sp"].mean()

df_p_cal["sc_sp"].plot()



for j in range(0,len(df_p.index)) :
    acf_list = []
    cc_list = []
    for i in range(1, 200):
        print(i, " / ", len(range(0, 200)))
        df_p_cal = df_kospi[[df_p.iloc[j,0],df_p.iloc[j,1]]].iloc[i:i + 500, :]
        df_p_cal["hat_data"] = cc * df_p_cal.iloc[:, 1]
        df_p_cal["sp"] = df_p_cal.iloc[:, 0] - df_p_cal["hat_data"]
        df_p_cal["sc_sp"] = df_p_cal["sp"] - df_p_cal["sp"].mean()

        acf_list.append(acf(df_p_cal["sc_sp"], fft=False)[1])
        cc_list.append(cc)
        df_acfcc = pd.DataFrame({"acf": acf_list,
                                 "cc": cc_list})
    df_acfcc.iloc[:,0].plot()

for j in range(0,len(df_p.index)) :
    fig, axes_list = plt.subplots(1, 1, figsize=(10, 8), tight_layout=True)

    df_p_cal = df_kospi_test[[df_p.iloc[j,0],df_p.iloc[j,1]]]
    cc, acf_1 = find_cc_golden(10,-10,df_p_cal,0.000001)
    df_p_cal["hat_data"] = cc * df_p_cal.iloc[:, 1]
    df_p_cal["sp"] = df_p_cal.iloc[:, 0] - df_p_cal["hat_data"]
    df_p_cal["sc_sp"] = df_p_cal["sp"] - df_p_cal["sp"].mean()
    mid = df_p_cal["sc_sp"].mean()
    upper = mid + 1.5*df_p_cal["sc_sp"].std(ddof=1)
    lower = -upper

    df_p_cal = df_kospi[[df_p.iloc[j,0],df_p.iloc[j,1]]]
    # df_p_cal = df_kospi_test[[df_p.iloc[j,0],df_p.iloc[j,1]]]
    df_p_cal["hat_data"] = cc * df_p_cal.iloc[:, 1]
    df_p_cal["sp"] = df_p_cal.iloc[:, 0] - df_p_cal["hat_data"]
    df_p_cal["sc_sp"] = df_p_cal["sp"] - df_p_cal["sp"].mean()

    axes_list.plot(df_p_cal["sc_sp"], ".-")
    axes_list.axhline(y=mid, color="red", linestyle="--")
    axes_list.axhline(y=upper, color="blue", linestyle="--")
    axes_list.axhline(y=lower, color="blue", linestyle="--")




















for k in range(0,math.ceil(len(df_p.index)/3)) :
    if k%3 == 0 :
        fig, axes_list = plt.subplots(3, 3, figsize=(20, 20), tight_layout=True)

    for j in range(k*3,3*(k+1)) :
        df_p_cal = df_kospi[[df_p.iloc[j, :][0], df_p.iloc[j, :][1]]].iloc[0:500, :]
        cc, acf_1 = find_cc_golden(10, -10, df_p_cal, 0.000001)
        acf_list = []
        cc_list = []
        i = 0
        for i in range(1,200) :
            print(i, " / ", len(range(0,200)))
            df_p_cal = df_kospi[[df_p.iloc[j,:][0],df_p.iloc[j,:][1]]].iloc[i:i+500,:]
            df_p_cal["hat_data"] = cc * df_p_cal.iloc[:, 1]
            df_p_cal["sp"] = df_p_cal.iloc[:, 0] - df_p_cal["hat_data"]
            df_p_cal["sc_sp"] = df_p_cal["sp"] - df_p_cal["sp"].mean()

            acf_list.append(acf(df_p_cal["sc_sp"], fft=False)[1])
            cc_list.append(cc)
            #

            #
            # if account == 0 and df_p_cal["sc_sp"].iloc[-1] > upper:
            #     print("sp매도 진입  : ",i)
            #     show_me()
            #     account = df_p_cal["sc_sp"].iloc[-1]
            # elif account == 0 and df_p_cal["sc_sp"].iloc[-1] < lower:
            #     print("sp매수 진입  : ",i)
            #     show_me()
            #     account = df_p_cal["sc_sp"].iloc[-1]
            # elif account > 0 and df_p_cal["sc_sp"].iloc[-1] < df_p_cal["sc_sp"].mean() :
            #     print("sp매도 청산  : ",i, "순이익 : ", df_p_cal["sc_sp"].iloc[-1] - account)
            #     show_me()
            #     profit.append(df_p_cal["sc_sp"].iloc[-1] - account)
            #     account = 0
            # elif account < 0 and df_p_cal["sc_sp"].iloc[-1] > df_p_cal["sc_sp"].mean() :
            #     print("sp매수 청산  : ",i, "순이익 : ", account-df_p_cal["sc_sp"].iloc[-1])
            #     show_me()
            #     profit.append(account-df_p_cal["sc_sp"].iloc[-1])
            #     account = 0
        df_acfcc = pd.DataFrame({"acf" : acf_list,
                                 "cc" : cc_list})

        axes_list[j%3][j-3*k].plot(df_acfcc.iloc[:, 0], '.-', linewidth=0.8)




df_p_cal = df_kospi[[df_p.iloc[1, :][0], df_p.iloc[1, :][1]]]
df_p_cal["hat_data"] = cc * df_p_cal.iloc[:, 1]
df_p_cal["sp"] = df_p_cal.iloc[:, 0] - df_p_cal["hat_data"]
df_p_cal["sc_sp"] = df_p_cal["sp"] - df_p_cal["sp"].mean()


df_acfcc.iloc[:,0].plot()
df_acfcc.iloc[:,1].plot()
df_p_cal["sc_sp"].plot()

def show_me(i,k,j) :






df_p_cal["sc_sp"].plot()
fig, axes_list = plt.subplots(3, 3, figsize=(20, 20), tight_layout=True)

