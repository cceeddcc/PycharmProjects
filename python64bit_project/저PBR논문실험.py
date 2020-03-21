import pandas as pd
import sqlite3
import re
import numpy as np

# 금융업 제외 코드 불러오기
with open("C:\\Users\\S\\Desktop\\바탕화면(임시)\\KOSPI\\KOSPI_Industrylist.txt", "r") as f:
    code_list = [line.split("\n")[0].split(",")[0] for line in f.readlines() if line.split("\n")[0].split(",")[1] != "021"]

"""
데이터 추출 및 정제
설명 :
t-1년도 사업보고서를 기준으로 시가총액과 PBR을 계산해서 t년 6월의 마지막 날에 포트폴리오를 구성 후 
t+1년 6월 마지막날까지 보유할 시 수익률을 계산하고 싶음

추출해야 하는 데이터
1. 매 년 6월 마지막날에 해당하는 주가 데이터
2. t년 3월에 발행됐을 t-1년 사업보고서 데이터
"""

con = sqlite3.connect("C:/Users/S/desktop/바탕화면(임시)/KOSPI/tmp/KOSPI_Price_DB_merge_final.db")
p = re.compile(r".*-03-.*")
columns = ['Date', 'Close', 'PBR', 'Market', 'Code', 'Close_6m_t']
Dates = list(range(2001, 2020))
# 사업년도를 Key로 해당 년도의 Dataframe을 Value로 하는 dictionary생성
Data1 = {"{}".format(str(Date)): pd.DataFrame(columns=columns) for Date in Dates}
i = 1

for code in code_list :
    print(i , " / ", len(code_list))
    i += 1

    #  : 1. 매 년 6월 마지막날에 해당하는 주가 데이터
    """
    df_6m : 매 년 6월 마지막날에 해당하는 데이터 프레임 변수
    """

    # code = "A000020" #tmp
    try :
        df = pd.read_sql("select Date, Close, Close_noadj, Capital, OS_noadj from %s" %code, con, index_col=None)

        df["Date"] = pd.to_datetime(df["Date"])
        df_6m = pd.DataFrame(columns=df.columns)
        for j in range(0, len(df["Date"])):
            if df["Date"][j].timetuple().tm_mon == 6 and df["Date"][j + 1].timetuple().tm_mon == 7: # 매년 6월 마지막날 추출
                df_6m = pd.concat([df_6m, df[df["Date"] == df["Date"][j]]])

        # 2. t년 3월에 발행됐을 t-1년 사업보고서 데이터
        """
        df_3m : t년 3월에 발행됐을 t-1년 사업보고서의 데이터 프레임    
        """
        df = df[~df["Capital"].isna()]
        df["Date"] = pd.to_datetime(df["Date"])
        df.insert(len(df.columns), "BPS", (df["Capital"] / df["OS_noadj"]) * 100000000)
        df.insert(len(df.columns), "PBR", df["Close_noadj"] / df["BPS"])
        df.insert(len(df.columns), "Market", df["Close_noadj"] * df["OS_noadj"])
        df.insert(len(df.columns), "Code", code)
        df = df.iloc[:, [0, 1, 6, 7, 8]]  # 필요한 열 빼고 나머지 잘라냄
        df_3m = pd.DataFrame(columns=df.columns)

        for line in df["Date"].astype(str):
            m = p.search(line)
            try:
                df_3m = pd.concat([df_3m, df[df["Date"] == m.group()]])
            except:
                continue

        # t년 6월 종가 데이터(df_6m)를 t년 사업보고서(df_3m)에 할당
        Close_6m_t = []
        for line in df_3m["Date"]:
            for line2 in df_6m["Date"]:
                if line.timetuple().tm_year == line2.timetuple().tm_year:
                    Close_6m_t.append(float(df_6m[df_6m["Date"] == line2]["Close"]))
        df_3m.insert(len(df_3m.columns), "Close_6m_t", Close_6m_t)

        # Data1에 사업년도 별로 Data 분배
        for Date_check in list(Data1.keys()) :
            try :
                df_3m["Date"] = df_3m["Date"].astype(str).apply(lambda x: x.split("-")[0])
                df3 = df_3m[df_3m["Date"] == Date_check]
                Data1[Date_check] = pd.concat([df3, Data1[Date_check]])
            except : continue
    except: continue

# Data1 : 사업년도를 Key로하고 해당년도에 필요한 Data를 가지고 있는 3차원 데이터

# 포트폴리오 수익률 계산
columns = list(Data1[list(Data1.keys())[0]].columns) + ["Close_6m_t+1", "return_t+1"]

for t in range(0, len(Data1.keys())-1): # 사업년도별 dataframe에 접근
    Key = list(Data1.keys())[t]
    p1 = Data1[list(Data1.keys())[t]]
    p2 = Data1[list(Data1.keys())[t+1]] # t+1년
    Close_6m_t1 = []

    for code in p1["Code"]:
        try :
            Close_6m_t1.append(float(p2[p2["Code"] == code]["Close_6m_t"]))
        except :
            Close_6m_t1.append(None)
            continue
    p1.insert(len(p1.columns), "Close_6m_t+1", Close_6m_t1)
    p1.insert(len(p1.columns), "return_t+1", p1["Close_6m_t+1"]/p1["Close_6m_t"]-1)

# 최종 통계
"""
기업 규모 기준으로 정렬한 데이터 만들기 
"""
# 기업 규모 기준 (위부터 소규모)
dict_stat = {}
for k in range(0, len(Data1.keys())-1) : # Data1 각각 Value에 접근
    df_stat = pd.DataFrame()
    df_sort_size = Data1[list(Data1.keys())[k]].sort_values(by="Market") # 소규모 기업 순 정렬
    df_sort_size = df_sort_size[df_sort_size["PBR"] > 0] # PBR 마이너스인 것 제외
    count = int(len(df_sort_size["Date"])/10) # 10분위 나누기 위함  

    # 수익률 평균 계산
    # Size로 정렬된 Dataframe을 10분위로 나눠서 Dataframe 생성 : df_sort_size_10
    # 10분위로 구분된 Data(df_sort_size_10)을 다시 PBR을 기준으로 정렬 (df_sort_size_10_PBR)
    for i in range(1, 11) : # size별로 10분위 접근
        df_sort_size_10 = df_sort_size.iloc[(i-1)*count:i*count]
        df_sort_size_10_PBR = df_sort_size_10.sort_values(by="PBR") # PBR기준 정렬
        count2 = int(len(df_sort_size_10_PBR["Date"])/10) # 10분위 나누기 위함
        returns = []

        # Size별로 10분위로 구분된 Data에 PBR을 기준으로 다시 10분위로 나눔 (df_sort_size_10_PBR_10)
        for j in range(1,11) :
            df_sort_size_10_PBR_10 = df_sort_size_10_PBR.iloc[(j-1)*count2:j*count2]
            try :
                returns.append(np.mean(df_sort_size_10_PBR_10["return_t+1"]))
            except :
                returns.append(None)
                continue
        S_returns = pd.Series(returns)
        df_stat = pd.concat([df_stat,S_returns], axis=1)
    dict_stat[list(Data1.keys())[k]] = df_stat


# columns가 Size 순
# rows가 PBR 순



# 각 사업년도 별 100개 포트폴리오 수익률 평균 내서 엑셀로 보내기
df_stat = dict_stat[list(dict_stat.keys())[0]]

for i in range(1,len(dict_stat.keys())) :
    df_stat = df_stat + dict_stat[list(dict_stat.keys())[i]]

df_stat = df_stat/18
df_stat.columns = ["SIZE1","SIZE2","SIZE3","SIZE4","SIZE5","SIZE6","SIZE7","SIZE8","SIZE9","SIZE10"]
df_stat.index = ["PBR1","PBR2","PBR3","PBR4","PBR5","PBR6","PBR7","PBR8","PBR9","PBR10"]

# 최종 엑셀저장
df_stat.to_excel("C:/Users/S/desktop/tmp2.xlsx")
