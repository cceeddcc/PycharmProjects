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
df_index = fine_ETFindex_code_multiple(df_ETF_index,"S&P GSCI Gold Index(TR)")

# ETF 종가, NAV를 변화율데이터로 바꾸고 1배수로 모두 변환해서 합치기
def conv_close_to_return(df_index):
    """
    배수마다 다른 수익률을 비교하기 위해 모두 1배수로 변환하고 하나의 통합된 Dataframe반환한다.
    """
    os.chdir("C:/Users/S/Desktop/바탕화면(임시)/ETF/")
    con = sqlite3.connect("tmp/ETF.db")
    rng = pd.date_range('1/1/2000', '03/20/2020', freq='D')
    df_merge = pd.DataFrame({"Date": rng})
    df_merge_inv = pd.DataFrame({"Date": rng})

    for i in range(len(df_index)) :
        # i = 0 #tmp
        code = df_index.iloc[i,0]
        df_data = pd.read_sql("Select * from %s" % code, con, index_col=None)
        df_data["Close1"] = df_data["Close"].shift(1)
        df_data["NAV1"] = df_data["NAV"].shift(1)
        df_data["Close_return"] = df_data["Close"] / df_data["Close1"] - 1
        df_data["NAV_return"] = df_data["NAV"] / df_data["NAV1"] - 1
        df_data = df_data.iloc[:, [0, 5, 6]].dropna(how="any")

        # 배수마다 다른 변환수식 실행
        if df_index.iloc[i,1] == "2.0x":
            df_data.iloc[:, 1:] = df_data.iloc[:, 1:] / 2
        elif df_index.iloc[i,1] == "-1.0x":
            df_data.iloc[:, 1:] = -df_data.iloc[:, 1:]
        elif df_index.iloc[i,1] == "-2.0x":
            df_data.iloc[:, 1:] = -df_data.iloc[:, 1:] / 2

        # Date 열 int -> Datetime으로 타입변환
        df_data["Date"] = df_data["Date"].astype(str)
        df_data["Date"] = pd.to_datetime(df_data["Date"])
        df_data.columns = ["Date", "%s_Close_return" %code, "%s_NAV_return" %code]

        # inverse와 일반 구분
        if df_index.iloc[i,1] == "1.0x":
            df_merge = pd.merge(df_merge, df_data, on='Date', how='left')
        elif df_index.iloc[i,1] == "2.0x":
            df_merge = pd.merge(df_merge, df_data, on='Date', how='left')
        elif df_index.iloc[i,1] == "-1.0x":
            df_merge_inv = pd.merge(df_merge_inv, df_data, on='Date', how='left')
        elif df_index.iloc[i,1] == "-2.0x":
            df_merge_inv = pd.merge(df_merge_inv, df_data, on='Date', how='left')

    con.close()
    return df_merge, df_merge_inv
df_comparable, df_comparable_inv = conv_close_to_return(df_index)

# 누적변화율 계산해서 비교하기
def cum_compare(df_comparable, df_comparable_inv) :
    count1 = int((len(df_comparable.columns)-1)/2)
    count2 = int((len(df_comparable_inv.columns)-1)/2)

    # 종가 누적 수익률 비교
    rng = pd.date_range("1/1/2000","03/20/2020",freq="D")
    df_Cum_close = pd.DataFrame({"Date":rng})
    for i in range(1,count1+1) :
        for j in range(1,count2+1) :
            # i = 2; j = 2 #tmp
            df_tmp_close = pd.DataFrame()
            df_tmp_close = pd.merge(df_comparable.iloc[:,[0,i*2-1]],df_comparable_inv.iloc[:,[0,j*2-1]],
                                    on="Date", how="left")
            df_tmp_close = df_tmp_close.dropna(how="any")

            df_tmp_close["Cum_Close_return1"] = df_tmp_close.iloc[:, 1].cumsum()
            df_tmp_close["Cum_Close_return2"] = df_tmp_close.iloc[:, 2].cumsum()
            df_tmp_close["Cum_%s-%s" % (df_tmp_close.columns[1].split("_")[0] + "C",
                                        df_tmp_close.columns[2].split("_")[0] + "C")] \
                = df_tmp_close["Cum_Close_return1"] - df_tmp_close["Cum_Close_return2"]


            df_Cum_close= pd.merge(df_Cum_close,df_tmp_close.iloc[:,[0,-1]],on="Date",how="left")

    df_Cum_close.index = df_Cum_close["Date"]
    df_Cum_close = df_Cum_close.iloc[:, 1:].dropna(how="all")
    df_Cum_close.insert(0,"Date", df_Cum_close.index)
    df_Cum_close.index = [i for i in range(0,len(df_Cum_close["Date"]))]

    # NAV 누적 수익률 비교
    rng = pd.date_range("1/1/2000", "03/20/2020", freq="D")
    df_Cum_NAV = pd.DataFrame({"Date": rng})
    for i in range(1, count1 + 1):
        for j in range(1, count2 + 1):
            # i = 2; j = 2 #tmp
            df_tmp_NAV = pd.DataFrame()
            df_tmp_NAV = pd.merge(df_comparable.iloc[:, [0, i * 2 - 1]], df_comparable_inv.iloc[:, [0, j * 2 - 1]],
                                    on="Date", how="left")
            df_tmp_NAV = df_tmp_NAV.dropna(how="any")

            df_tmp_NAV["Cum_NAV_return1"] = df_tmp_NAV.iloc[:, 1].cumsum()
            df_tmp_NAV["Cum_NAV_return2"] = df_tmp_NAV.iloc[:, 2].cumsum()
            df_tmp_NAV["Cum_%s-%s" % (df_tmp_NAV.columns[1].split("_")[0] + "N",
                                        df_tmp_NAV.columns[2].split("_")[0] + "N")] \
                = df_tmp_NAV["Cum_NAV_return1"] - df_tmp_NAV["Cum_NAV_return2"]

            df_Cum_NAV = pd.merge(df_Cum_NAV, df_tmp_NAV.iloc[:, [0, -1]], on="Date", how="left")

    df_Cum_NAV.index = df_Cum_NAV["Date"]
    df_Cum_NAV = df_Cum_NAV.iloc[:, 1:].dropna(how="all")
    df_Cum_NAV.insert(0, "Date", df_Cum_NAV.index)
    df_Cum_NAV.index = [i for i in range(0, len(df_Cum_NAV["Date"]))]

    return df_Cum_close, df_Cum_NAV
df_Cum_close, df_Cum_NAV = cum_compare(df_comparable, df_comparable_inv)

df_Cum_close.to_excel("C:/Users/S/Desktop/close2.xlsx")
df_Cum_NAV.to_excel("C:/Users/S/Desktop/NAV2.xlsx")



# 누적합이 아니라 누적곱이여야 하는 문제점 발견



# 추세가 있다면 해당 trend를 회귀분석해서 트렌드 제거하고 보면 정규분포 ?
# 추세를 제거하고 보면 잔차가 1%범위내에서 움직이는데 이는 LP호가의 스프레드와 일치하는 것을 보아
# 추세 = 같은기초자산을 추종하지만 나타날 수 있는 차이 ex) 수수료, 그것을 제외하고 LP에 의해 차익거래 기회가 없는것 같아보인다.
# 그렇다면 높은 Corr을 보이는 자산들로 상대가치거래가능한가 ?? 높은 Corr을 가진 기초자산들을 묶어서 한번 살펴보자



