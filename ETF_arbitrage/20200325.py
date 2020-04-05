import pandas as pd
import sqlite3
import os
import statsmodels.formula.api as smf
import matplotlib.pyplot as plt
from scipy import stats
df_ETF_index = pd.read_excel("C:/Users/S/Desktop/ETF기초지수.xlsx")

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
            i = 1 # temp
            j = 1 # temp
            df1 = pd.DataFrame()
            df1 = pd.merge(df_comparable.iloc[:, [0, i * 2 - 1]],
                           df_comparable_inv.iloc[:, [0, j * 2 - 1]],
                           on="Date", how="left")
            df1 = df1.dropna(how="any")

            for k in range(1, 3):
                # k = 1 # temp
                # k = 2 # temp
                CloseNAV = "Close" # temp
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

            ###########################################################################



            if CloseNAV == "Close":
                # 회귀분석 파트
                df1.columns
                df1.iloc[:,1]= (df1.iloc[:,1]-1)/condition
                df1.iloc[:,2]= (df1.iloc[:,2]-1)/condition

                df_merge = pd.merge(df1.iloc[:, [0, 1]], df1.iloc[:, [0, 2]], on="Date")
                df_merge.columns = ["Date", code1, code2]
                # outlier 제거
                # plt.plot(df_merge.iloc[:,[1]],df_merge.iloc[:,[2]], "bo")
                # df_merge.iloc[:,[1,2]].plot()

                # 인버스와 일반수익률 변화를 회귀분석시켜서 잔차가 정규분포를 따른다면
                # 차익거래 수익가능성에 대해
                models1 = smf.ols(formula="%s ~ %s" %(code1,code2), data=df_merge)
                models1 = smf.ols(formula="A152280 ~ A114800" , data=df_merge)
                result = models1.fit()
                df_merge["Y_hat"] = result.params["Intercept"] + result.params["A114800"] * df_merge["A114800"]
                df_merge["residual"] = df_merge[code1] - df_merge["Y_hat"]
                df_merge["residual"].to_excel("C:/Users/S/Desktop/resi.xlsx")
                mean = df_merge["residual"].mean()
                std = df_merge["residual"].std()
                upper = mean + 1 * std
                lower = mean - 1 * std

                df1["Yield"] = df1["Cum_Close_return1"] + df1["Cum_Close_return2"] - 2
                df1["time"] = [i for i in range(len(df1["Yield"]))]
                model = smf.ols(formula="Yield ~ time", data=df1)
                result = model.fit()
                df1["Yield2"] = result.params["Intercept"] + result.params["time"] * df1["time"]
                df1["Cum_%s-%s" % (code1 + "C", code2 + "C")] = df1["Yield"]-df1["Yield2"]
                df1 = pd.merge(df1,df_merge[["Date","residual"]],on="Date")

                df_resi = pd.DataFrame({"Date": df1["Date"]})
                df_resi = pd.merge(df_resi, df1[df1["residual"] > upper].iloc[:,[0,-2]], on="Date", how= "left")
                df_resi = pd.merge(df_resi, df1[df1["residual"] < lower].iloc[:,[0,-2]], on="Date", how = "left")
                Date = df_resi["Date"]
                df_resi = df_resi.iloc[:,1:].dropna(how="all")
                df_resi.to_excel("C:/Users/S/Desktop/dmwk.xlsx")



                df_resi = df_resi.fillna("wow")
                sell = 0
                buy = 0
                returns = []
                import numpy as np












                for i in range(len(df_resi["Date"])) :
                    # i = 1 # temp
                    if df_resi.iloc[i,1] !="wow":
                        if buy == 0 :
                            pass
                        elif buy != 0:
                            returns.append(sell - buy)
                            buy = 0

                    if df_resi.iloc[i,2] !="wow" :
                        if sell == 0 and buy == 0 :
                            buy = df_resi[i,2]


                        elif sell != 0 :
                            returns.append(sell - buy)
                            sell = 0
                            buy = 0


                df_resi.fillna(0)

                df_resi.to_excel("C:/Users/S/Desktop/wow.xlsx")
                os.getcwd()

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


df_merge.to_excel("C:/Users/S/Desktop/tmp.xlsx")

df1["Yield2"] = result.params["Intercept"] + result.params["time"] * df1["time"]
import matplotlib.pyplot as plt
plt.plot(df_merge.iloc[:,1],df_merge.iloc[:,2],'bo')
df_merge