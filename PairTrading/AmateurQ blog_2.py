import pandas as pd
import numpy as np
import os
import sqlite3 as sql
import pandas_datareader.data as web
import statsmodels.api as stm
from statsmodels.tsa.stattools import acf
import matplotlib.pyplot as plt


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

# 데이터 불러오기
def road_data(start, end, p_code_list):
    """
    기간에 해당하는 종목들의 로그 price 데이터를 얻기 위함
    """
    date = pd.date_range(start, end)
    p_df = pd.DataFrame({"Date": date})
    for code in p_code_list :
        df = web.DataReader(start=start, end=end, data_source="yahoo", name="%s" %code)
        df["Date"] = df.index
        df.index = [i for i in range(0,len(df["Date"]))]
        df["log_C"] = np.log(df["Close"])
        df = df[["Date", "log_C"]]
        df.columns= ["Date", "C_%s" %code]
        p_df = pd.merge(p_df, df, on="Date", how="right")
    return p_df

# 야후에 없는 데이터 db에서 불러오기
def road_data_db(start, end, p_code_list):
    """
    db에서 데이터 불러오기 위함
    """
    os.chdir("C:/Users/S/Desktop/바탕화면(임시)/KOSPI/tmp/")
    con = sql.connect("KOSPI_Price_DB_merge_final.db")
    date = pd.date_range(start, end)
    df_p = pd.DataFrame({"Date": date})
    for code in p_code_list:
        # code = "A017670" #tmp
        df = pd.read_sql("Select Date, Close from %s" % code, con, index_col=None)
        df["Date"] = pd.to_datetime(df["Date"])
        df["log_C"] = np.log(df.iloc[:, 1])
        df = df.iloc[:, [0, 2]]
        df.columns = ["Date", "C_%s" % code]
        df_p = pd.merge(df_p, df, on="Date", how="left")
    df_p = df_p.dropna()
    con.close()
    return df_p

    date = pd.date_range("20080101", "20130101")
    df_tmp = pd.DataFrame({"Date": date})
    df_sk["Date"] = pd.to_datetime(df_sk["Date"])
    df_lg["Date"] = pd.to_datetime(df_lg["Date"])

    df_merg1 = pd.merge(df_tmp, df_sk, on="Date", how="left")
    df_merg1 = pd.merge(df_merg1, df_lg, on="Date", how="left")
    df_merg1 = df_merg1.dropna()
    df_merg1["log_sk"] = np.log(df_merg1.iloc[:, 1])
    df_merg1["log_lg"] = np.log(df_merg1.iloc[:, 2])


# 가격 상관계수와 수익률 상관계수 확인해보기
start = '2009-09-29'
end = '2022-02-28'
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
df_merg1["r_sam"] = df_merg1["log_sam"] - df_merg1["log_sam"].shift(1)
df_merg1["r_samwoo"] = df_merg1["log_samwoo"] - df_merg1["log_samwoo"].shift(1)
df_cor = df_merg1.corr()
df_cor.loc["r_sam","r_samwoo"] # 수익률상관계수
df_cor.loc["log_sam","log_samwoo"] # 가격상관계수


m = stm.formula.ols("log_sam~log_samwoo", data=df_merg1)
r = m.fit()
r.summary()
df_merg1["hat_log_sam"] = r.fittedvalues
df_merg1["sp"] = df_merg1["hat_log_sam"]-df_merg1["log_sam"]
df_merg1["sp"].plot()



# 다중페어 구성해서 정상성 확인

# 종목명, 코드 불러오기
with open("C:\\Users\\S\\Desktop\\바탕화면(임시)\\KOSPI\\KOSPI_codelist.txt", "r") as f :
    code_list = [line[1:].split("\n")[0] for line in f.readlines()]

with open("C:\\Users\\S\\Desktop\\바탕화면(임시)\\KOSPI\\KOSPI_namelist.txt", "r") as f :
    name_list = [line.split("\n")[0] for line in f.readlines()]

code_dict = {}
for i in range(0,len(code_list)) :
    code_dict["%s" %name_list[i]] = code_list[i]

p_list = ["LG", "LG전자", "LG화학"]

p_code_list = []
for name in p_list :
    p_code_list.append(code_dict[name]+".KS")


start = "2010-02-09"
end = "2013-01-01"
date = pd.date_range("20100209","20130101")
p_df = pd.DataFrame({"Date":date})

for code in p_code_list :
    df = web.DataReader(start=start, end=end, data_source="yahoo", name="%s" %code)
    df["Date"] = df.index
    df.index = [i for i in range(0,len(df["Date"]))]
    df["log_C"] = np.log(df["Close"])
    df = df[["Date", "log_C"]]
    df.columns= ["Date", "C_%s" %code]
    p_df = pd.merge(p_df, df, on="Date", how="right")


# cc구해보기
# 비중 0.5 사용
p_df.corr()
acf_list = []
index = []
for cc in np.arange(0.5,2,0.1) :
    hat_data = (p_df.iloc[:, 2]*0.5 + p_df.iloc[:, 3]*0.5) * cc
    p_df["sp_0.5"] = p_df["C_003550.KS"] - hat_data
    acf_list.append(acf(p_df["sp_0.5"], missing="drop")[1])
    index.append(cc)

acf_df = pd.DataFrame({"acf" : acf_list}, index=index)
# acf_df.iloc[:,0].plot() # 최소가 되는 cc 찾기
acf_df[acf_df.iloc[:,0] == min(acf_list)]
cc = acf_df[acf_df.iloc[:,0] == min(acf_list)].index[0]
hat_data = (p_df.iloc[:, 2]*0.5 + p_df.iloc[:, 3]*0.5) * cc
p_df["sp_0.5"] = p_df["C_003550.KS"] - hat_data
p_df["sp_0.5"].plot() # 스프레드 시각화


# 다중페어 비중 변화
acf_list = []
cc_list = []
w1_list = []
for cc in np.arange(0.5,2,0.1) :
    for w1 in np.arange(0,1,0.001) :
        w2 = 1-w1
        hat_data = (w1*p_df.iloc[:,2]+w2*p_df.iloc[:,3])*cc
        p_df["sp"] = p_df["C_003550.KS"] - hat_data
        acf_list.append(acf(p_df["sp"], missing="drop")[1])
        cc_list.append(cc)
        w1_list.append(w1)

acf_df = pd.DataFrame({"acf" : acf_list,
                       "cc" : cc_list,
                       "w1": w1_list},)

# acf_df.iloc[:,0].plot() # 최적 cc 찾기
acf_df[acf_df.iloc[:,0] == min(acf_list)] # 정상성 가장 높은 지점
cc = acf_df[acf_df.iloc[:,0] == min(acf_list)].iloc[:,1].values[0]
w1 = acf_df[acf_df.iloc[:,0] == min(acf_list)].iloc[:,2].values[0]
w2 = 1-w1
hat_data = (w1*p_df.iloc[:,2]+w2*p_df.iloc[:,3])*cc
p_df["sp"] = p_df["C_003550.KS"] - hat_data
p_df["sp"].mean()
p_df["sp_w1"] = p_df["sp"] - p_df["sp"].mean()
p_df["sp_w1"].plot() # 스프레드 확인



# 최근데이터로 확인
start = "2015-02-09"
end = "2020-04-20"
date = pd.date_range("20150209","20200420")
p_df = pd.DataFrame({"Date":date})

for code in p_code_list :
    df = web.DataReader(start=start, end=end, data_source="yahoo", name="%s" %code)
    df["Date"] = df.index
    df.index = [i for i in range(0,len(df["Date"]))]
    df["log_C"] = np.log(df["Close"])
    df = df[["Date", "log_C"]]
    df.columns= ["Date", "C_%s" %code]
    p_df = pd.merge(p_df, df, on="Date", how="right")

# 다중페어 비중 변화
acf_list = []
cc_list = []
w1_list = []
for cc in np.arange(0.5,2,0.1) :
    for w1 in np.arange(0,1,0.001) :
        print(w1)
        w2 = 1-w1
        hat_data = (w1*p_df.iloc[:,2]+w2*p_df.iloc[:,3])*cc
        p_df["sp"] = p_df["C_003550.KS"] - hat_data
        acf_list.append(acf(p_df["sp"], missing="drop")[1])
        cc_list.append(cc)
        w1_list.append(w1)

acf_df = pd.DataFrame({"acf" : acf_list,
                       "cc" : cc_list,
                       "w1": w1_list},)

acf_df[acf_df.iloc[:,0] == min(acf_list)] # 정상성 가장 높은 지점
cc = acf_df[acf_df.iloc[:,0] == min(acf_list)].iloc[:,1].values[0]
w1 = acf_df[acf_df.iloc[:,0] == min(acf_list)].iloc[:,2].values[0]
w2 = 1-w1
hat_data = (w1*p_df.iloc[:,2]+w2*p_df.iloc[:,3])*cc
p_df["sp"] = p_df["C_003550.KS"] - hat_data
p_df["sp"].mean()
p_df["sp_w1"] = p_df["sp"] - p_df["sp"].mean()
p_df["sp_w1"].plot() # 스프레드 확인




# 몬테카를로 시뮬레이션 해보기
code_dict, code_list, name_list = road_codename()
p_list = ["SK텔레콤", "KT"]
p_code_list = []
for name in p_list :
    p_code_list.append("A"+code_dict[name])

start = "2010-07-08"
end = "2012-12-28"

# 데이터 로드
p_df = road_data_db(start, end, p_code_list)
p_df["r_sk"] = p_df["C_A017670"] - p_df["C_A017670"].shift(1)
p_df["r_kt"] = p_df["C_A030200"] - p_df["C_A030200"].shift(1)

cc = 1.571
p_df["hat_kt"] = cc*p_df["C_A017670"]
p_df["sp"] = p_df["C_A030200"] - p_df["hat_kt"]
p_df["sp"] = p_df["sp"]- p_df["sp"].mean()
p_df["sp"].plot()


# 최적 공적분 찾기 알고리즘
# 황금비율 구간 검색법
def find_cc_golden(upper, lower, p_df, error) :
    loop = 1000
    ratio = 0.618033
    ran = upper - lower

    for i in range(0,loop) :
        x1 = lower + ratio * ran
        x2 = upper - ratio * ran
        fx = []

        for x in [x1,x2] :
            """
            acf coef 계산위함 
            임시용 데이터  
            """
            p_df["hat_kt"] = x * p_df["C_A017670"]
            p_df["sp"] = p_df["C_A030200"] - p_df["hat_kt"]
            fx.append(acf(p_df["sp"])[1])

        # golden section search algorithm
        if fx[0] > fx[1] : # f(x1) > f(x2)
            upper = x1
            ran = upper - lower
        else :
            lower = x2
            ran = upper - lower

        if ran < error :
            cc = (upper+lower)/ 2
            print("최적 acf : ", acf(p_df["sp"])[1])
            return cc
            break

cc = find_cc_golden(10, -10, p_df, 0.00001)
# 최적 CC 사용
p_df["hat_kt"] = cc*p_df["C_A017670"]
p_df["sp"] = p_df["C_A030200"] - p_df["hat_kt"]
p_df["sp"] = p_df["sp"]- p_df["sp"].mean()
p_df["sp"].plot()

# spread qqplot, qqline
ax = plt.subplot(1,1,1)
stm.qqplot(p_df["sp"], ax=ax)



















# 시뮬레이션 데이터 생성
corr1 = 0.556
corr2 = 0.831
w1 = np.random.randn()
w2 = w1*corr1+np.random.randn()*0.831
w1 = []
w2 = []
for i in range(0,40) :
    tmp = np.random.randn()
    w1.append(np.random.randn())
    w2.append(tmp*corr1+np.random.randn()*0.831)

df_tmp = pd.DataFrame({"w1": w1,
                      "w2":w2})
df_tmp.corr()

p_df.corr()
p_df.corr()
















# 마코위츠 최적포트폴리오 구성해보고 수익률 계산해보기
# 종목명, 코드 불러오기
with open("C:\\Users\\S\\Desktop\\바탕화면(임시)\\KOSPI\\KOSPI_codelist.txt", "r") as f :
    code_list = [line[1:].split("\n")[0] for line in f.readlines()]

with open("C:\\Users\\S\\Desktop\\바탕화면(임시)\\KOSPI\\KOSPI_namelist.txt", "r") as f :
    name_list = [line.split("\n")[0] for line in f.readlines()]

code_dict = {}
for i in range(0,len(code_list)) :
    code_dict["%s" %name_list[i]] = code_list[i]

p_list = ["삼성전자", "SK텔레콤", "POSCO", "KT", "한국전력", "현대차", "삼성증권"]

p_code_list = []
for name in p_list :
    p_code_list.append(code_dict[name]+".KS")

start = "20140101"
end = "20141230"

date = pd.date_range("20140101","20141230")
p_df = pd.DataFrame({"Date":date})

for code in p_code_list :
    df = web.DataReader(start=start, end=end, data_source = "yahoo", name= "%s" %code)
    df["Date"] = df.index
    df.index = [i for i in range(0,len(df["Date"]))]
    df["log_C"] = np.log(df["Close"])
    df["return"] = df["log_C"] - df["log_C"].shift(1) # 일일 수익률
    df = df.fillna(1)
    df["C_return"] = df["return"].cumprod()
    df = df[["Date", "C_return"]]
    df.columns= ["Date", "r_%s" %code]
    p_df = pd.merge(p_df, df, on="Date", how="right")

p_df




emean = [p_df.iloc[:,i].mean()-1 for i in range(1,len(p_df.columns))]
estd = [p_df.iloc[:,i].std(ddof=1) for i in range(1,len(p_df.columns))]
p_eres = pd.DataFrame({"emean" : emean,
                       "estd" : estd}, index=p_df.columns[1:])


