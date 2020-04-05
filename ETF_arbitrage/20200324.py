"""
수익률을 누적합이아니라 누적곱으로 해야하는 문제점 해결
"""

import pandas as pd
import sqlite3
import os

os.getcwd()
os.chdir("C:/Users/S/Desktop/")

# ETF 기초지수 Dataframe
df_ETF_index = pd.read_excel("ETF기초지수.xlsx")

# ETF 기초지수에 해당하는 코드 및 배수 저장
def fine_ETFindex_code_multiple(df_ETF_index, index_name) :
    df1 = df_ETF_index[df_ETF_index["추적지수명"] == "%s" % index_name].iloc[:,[0,3]]
    return df1
# baseindex = "10년국채선물지수"
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
        df_data["Close1"] = df_data["Close"].shift(1)
        df_data["NAV1"] = df_data["NAV"].shift(1)
        df_data["Close_return"] = df_data["Close"] / df_data["Close1"]
        df_data["NAV_return"] = df_data["NAV"] / df_data["NAV1"]
        df_data = df_data.iloc[:, [0, 5, 6]].dropna(how="any")

        # Date 열 int -> Datetime으로 타입변환
        df_data["Date"] = df_data["Date"].astype(str)
        df_data["Date"] = pd.to_datetime(df_data["Date"])
        df_data.columns = ["Date",
                           "%s_Close_return_%s" %(code,df_index.iloc[i,1]),
                           "%s_NAV_return_%s" %(code,df_index.iloc[i,1])]

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

# 누적곱변화율 계산해서 비교하기
def make_index(df_comparable, df_comparable_inv, CloseNAV):
    # ETF1 누적수익률 - ETF2 누적수익률 만들기 위해 생성한 함수
    count1 = int((len(df_comparable.columns) - 1) / 2)
    count2 = int((len(df_comparable_inv.columns) - 1) / 2)
    rng = pd.date_range("1/1/2000", "03/20/2020", freq="D")
    df_Cum = pd.DataFrame({"Date": rng})

    for i in range(1, count1 + 1):
        for j in range(1, count2 + 1):
            df1 = pd.DataFrame()
            df1 = pd.merge(df_comparable.iloc[:, [0, i * 2 - 1]],
                           df_comparable_inv.iloc[:, [0, j * 2 - 1]],
                           on="Date", how="left")
            df1 = df1.dropna(how="any")

            for k in range(1, 3):
                # k = 1 # temp
                # k = 2 # temp
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
                df1["Cum_%s-%s" % (code1 + "C", code2 + "C")] = df1["Cum_Close_return1"] + df1["Cum_Close_return2"] - 2
                df_Cum = pd.merge(df_Cum, df1.iloc[:, [0, -1]], on="Date", how="left")
            else:
                df1["Cum_%s-%s" % (code1 + "N", code2 + "N")] = df1["Cum_NAV_return1"] + df1["Cum_NAV_return2"] - 2
                df_Cum = pd.merge(df_Cum, df1.iloc[:, [0, -1]], on="Date", how="left")

    df_Cum.index = df_Cum["Date"]
    df_Cum = df_Cum.iloc[:, 1:].dropna(how="all")
    df_Cum.insert(0, "Date", df_Cum.index)
    df_Cum.index = [i for i in range(0, len(df_Cum["Date"]))]
    return df_Cum
df_Cum_close = make_index(df_comparable, df_comparable_inv, "Close")
df_Cum_NAV = make_index(df_comparable, df_comparable_inv, "NAV")

df_Cum_close.to_excel("C:/Users/S/Desktop/%s_close.xlsx" % baseindex)
df_Cum_NAV.to_excel("C:/Users/S/Desktop/%s_NAV.xlsx" % baseindex)




# 회귀분석 활용한 잔차구하기

import statsmodels.formula.api as smf
import pandas as pd
import sqlite3
import os

os.getcwd()
os.chdir("C:/Users/S/Desktop/")

# ETF 기초지수 Dataframe
df_ETF_index = pd.read_excel("ETF기초지수.xlsx")

# ETF 기초지수에 해당하는 코드 및 배수 저장
def fine_ETFindex_code_multiple(df_ETF_index, index_name) :
    df1 = df_ETF_index[df_ETF_index["추적지수명"] == "%s" % index_name].iloc[:,[0,3]]
    return df1
# df_index = fine_ETFindex_code_multiple(df_ETF_index,"F-KOSPI200")
# df_index = fine_ETFindex_code_multiple(df_ETF_index,"미국달러 선물지수")
# baseindex = "10년국채선물지수"
baseindex = "F-KOSPI200"
# baseindex = "F-KTB3Y 지수"
# baseindex = "미국달러 선물지수"
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
        df_data["Close1"] = df_data["Close"].shift(1)
        df_data["NAV1"] = df_data["NAV"].shift(1)
        df_data["Close_return"] = df_data["Close"] / df_data["Close1"]
        df_data["NAV_return"] = df_data["NAV"] / df_data["NAV1"]
        df_data = df_data.iloc[:, [0, 5, 6]].dropna(how="any")

        # Date 열 int -> Datetime으로 타입변환
        df_data["Date"] = df_data["Date"].astype(str)
        df_data["Date"] = pd.to_datetime(df_data["Date"])
        df_data.columns = ["Date",
                           "%s_Close_return_%s" %(code,df_index.iloc[i,1]),
                           "%s_NAV_return_%s" %(code,df_index.iloc[i,1])]

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

# 추세가 있다면 해당 trend를 회귀분석해서 트렌드 제거하고 보면 정규분포 ?
# 추세를 제거하고 보면 잔차가 1%범위내에서 움직이는데 이는 LP호가의 스프레드와 일치하는 것을 보아
# 추세 = 같은기초자산을 추종하지만 나타날 수 있는 차이 ex) 수수료, 그것을 제외하고 LP에 의해 차익거래 기회가 없는것 같아보인다.
# 그렇다면 높은 Corr을 보이는 자산들로 상대가치거래가능한가 ?? 높은 Corr을 가진 기초자산들을 묶어서 한번 살펴보자



