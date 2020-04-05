"""
ETF를 활용한 pair trading 연습
"""

import pandas as pd
import os
import sqlite3
import statsmodels.formula.api as smf
import numpy as np
import matplotlib.pyplot as plt

os.chdir("C:/Users/S/Desktop/바탕화면(임시)/ETF/")

# ETF 코드명 불러오기
df_ETF_index = pd.read_excel("C:/Users/S/Desktop/ETF기초지수.xlsx")

def fine_ETFindex_code_multiple(df_ETF_index, index_name) :
    df1 = df_ETF_index[df_ETF_index["추적지수명"] == "%s" % index_name].iloc[:,[0,3]]
    return df1

baseindex = "F-KOSPI200"
df_index = fine_ETFindex_code_multiple(df_ETF_index,baseindex)

def conv_close_to_return(df_index):
    """
    레버리지와 인버스 구분하고 변수명에 배수 정보를 넣어 통합된 Dataframe반환한다.
    """
    os.chdir("C:/Users/S/Desktop/바탕화면(임시)/ETF/")
    con = sqlite3.connect("tmp/ETF.db")
    rng = pd.date_range('1/1/2000', '03/20/2020', freq='D')
    df_merge = pd.DataFrame({"Date": rng})
    df_merge_inv = pd.DataFrame({"Date": rng})

    for i in range(len(df_index)) :
        # i = 3 #temp
        code = df_index.iloc[i,0]
        df_data = pd.read_sql("Select * from %s" % code, con, index_col=None)

        # ln(price)
        df_data["lnClose"] = np.log(df_data["Close"])

        # Date 열 int -> Datetime으로 타입변환
        df_data["Date"] = df_data["Date"].astype(str)
        df_data["Date"] = pd.to_datetime(df_data["Date"])
        df_data = df_data.iloc[:,[0,3]]
        df_data.columns = ["Date",
                           "%s_lnClose" %code]

        # inverse와 일반 구분
        try :
            condition = int(df_index.iloc[i, 1][0])
        except :
            condition = -1

        if condition > 0 :
            df_merge = pd.merge(df_merge, df_data, on='Date', how='left')
        else :
            df_merge_inv = pd.merge(df_merge_inv, df_data, on='Date', how='left')

    con.close()
    return df_merge, df_merge_inv
df_comparable, df_comparable_inv = conv_close_to_return(df_index)

# 두 log 가격 데이터의 선형관계 확인 -> regression을 통해 헷지비율 추정
df_comparable
df_merge_1 = pd.merge(df_comparable.iloc[:,[0,6]],df_comparable_inv.iloc[:,[0,1]],on="Date",how="left")
df_merge_1 = df_merge_1.dropna()
df_merge_1["p1"] = df_merge_1.iloc[:,1].shift(1)
df_merge_1["p2"] = df_merge_1.iloc[:,2].shift(1)
df_merge_1["return1"] = df_merge_1.iloc[:,1]-df_merge_1.iloc[:,3]
df_merge_1["return2"] = df_merge_1.iloc[:,2]-df_merge_1.iloc[:,4]


plt.plot(df_merge_1["return1"],df_merge_1["return2"], "bo")

# OLS 추정
df_merge_1
model = smf.ols(formula="return1 ~ return2" ,data = df_merge_1)
result = model.fit()
result.summary()

df_merge_1["yhat"] = result.params["Intercept"] + result.params["return2"]*df_merge_1["return2"]
df_merge_1["spread"] = df_merge_1["return1"]-df_merge_1["yhat"]
df_merge_1["spread"].plot()

# Stationary 확인




















df_comparable[1]
# 누적곱변화율 계산해서 비교하기
def make_index(df_comparable, df_comparable_inv, CloseNAV):
    # ETF1 누적수익률 - ETF2 누적수익률 만들기 위해 생성한 함수
    count1 = int((len(df_comparable.columns) - 1) / 2)
    count2 = int((len(df_comparable_inv.columns) - 1) / 2)
    rng = pd.date_range("1/1/2000", "03/20/2020", freq="D")
    df_Cum = pd.DataFrame({"Date": rng})

    for i in range(1, count1 + 1):
        for j in range(1, count2 + 1):
            # i = 1 # temp
            # j = 1 # temp
            df1 = pd.DataFrame()
            df1 = pd.merge(df_comparable.iloc[:, [0, i * 2 - 1]],
                           df_comparable_inv.iloc[:, [0, j * 2 - 1]],
                           on="Date", how="left")
            df1 = df1.dropna(how="any")

            for k in range(1, 3):
                # k = 1 # temp
                # k = 2 # temp
                # CloseNAV = "Close" # temp
                # 비교를 위해 배수 조정
                try:
                    condition = int(df1.columns[k].split("_")[-1][0])
                except:
                    condition = int(df1.columns[k].split("_")[-1][1])
                df1.iloc[:, k] = df1.iloc[:, k].cumprod()
                df1.iloc[:, k] = (df1.iloc[:, k] / condition) - (1 / condition) + 1

                df1["Cum_%s_return%s" % (CloseNAV, str(k))] = df1.iloc[:, k]

            code1 = df1.columns[1].split("_")[0]
            code2 = df1.columns[2].split("_")[0]
            if CloseNAV == "Close":
                # 회귀분석 파트
                df1["Yield"] = df1["Cum_Close_return1"] + df1["Cum_Close_return2"] - 2
                df1["time"] = [i for i in range(len(df1["Yield"]))]
                model = smf.ols(formula="Yield ~ time", data=df1)
                result = model.fit()
                df1["Yield2"] = result.params["Intercept"] + result.params["time"] * df1["time"]
                df1["Cum_%s-%s" % (code1 + "C", code2 + "C")] = df1["Yield"]-df1["Yield2"]

            else:
                # 회귀분석 파트
                df1["Yield"] = df1["Cum_NAV_return1"] + df1["Cum_NAV_return2"] - 2
                df1["time"] = [i for i in range(len(df1["Yield"]))]
                model = smf.ols(formula="Yield ~ time", data=df1)
                result = model.fit()
                df1["Yield2"] = result.params["Intercept"] + result.params["time"] * df1["time"]
                df1["Cum_%s-%s" % (code1 + "N", code2 + "N")] = df1["Yield"] - df1["Yield2"]
            df_Cum = pd.merge(df_Cum, df1.iloc[:, [0, -1]], on="Date", how="left")


    df_Cum.index = df_Cum["Date"]
    df_Cum = df_Cum.iloc[:, 1:].dropna(how="all")
    df_Cum.insert(0, "Date", df_Cum.index)
    df_Cum.index = [i for i in range(0, len(df_Cum["Date"]))]
    return df_Cum

df_Cum_close = make_index(df_comparable, df_comparable_inv, "Close")
df_Cum_NAV = make_index(df_comparable, df_comparable_inv, "NAV")

df_Cum_close.to_excel("C:/Users/S/Desktop/%s_close_cumprod.xlsx" % baseindex)
df_Cum_NAV.to_excel("C:/Users/S/Desktop/%s_NAV_cumprod.xlsx" % baseindex)