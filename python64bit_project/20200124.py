"""
데이터 칼럼명 변경 및 Data type 지정
"""

import pandas as pd
import sqlite3

# 종목명, 코드 불러오기
with open("C:\\Users\\S\\Desktop\\바탕화면(임시)\\KOSPI\\KOSPI_codelist.txt", "r") as f:
    code_list = [line[1:].split("\n")[0] for line in f.readlines()]

con = sqlite3.connect("C:/Users/S/desktop/바탕화면(임시)/KOSPI/tmp/KOSPI_Price_DB_merge_final.db")
con2 = sqlite3.connect("C:/Users/S/desktop/바탕화면(임시)/KOSPI/tmp/KOSPI_Price_DB_merge_final2.db")

i = 1
for code in code_list :
    print(i, " / ", len(code_list))
    i += 1
    code = "A" + code
    # code = "A001260" # tmp
    df = pd.read_sql("select * from %s" %code, con, index_col=None)
    df.columns = ['Date', 'Open', 'High', 'Low', 'Close', 'Volume', 'TA',
           'OS', 'LFO', 'AFO', 'FSA', 'FSR',
           'INB', 'CINB', 'Open_noadj', 'High_noadj', 'Low_noadj',
           'Close_noadj', 'Volume_noadj', 'TA_noadj', 'OS_noadj',
           'LFO_noadj', 'AFO_noadj', 'FSA_noadj', 'FSR_noadj',
           'INB_noadj', 'CINB_noadj', 'Price', 'Asset', 'Capital', 'Sales',
           'Operating', 'NI', 'ES', 'CFO', 'CFI', 'CFF', 'Liability',
           'GP', 'Noperating', 'COGS', 'SGA', 'EBIT', 'NetCF',
           'Divrate', 'EBITDA', 'PR', 'CNI']
    dtypes = {i: "REAL" for i in df.columns[1:]}
    dtypes["Date"] = "TEXT"
    df.to_sql(code, con2, index=False, dtype=dtypes)


con.close()
con2.close()


df
df.to_excel("C:/Users/S/desktop/바탕화면(임시)/KOSPI/tmp/meta_KOSPI_Price_DB_merge_final.xlsx")

"""
데이터분석
"""

import pandas as pd
import sqlite3
import matplotlib.pyplot as plt

# 종목명, 코드 불러오기
with open("C:\\Users\\S\\Desktop\\바탕화면(임시)\\KOSPI\\KOSPI_codelist.txt", "r") as f:
    code_list = [line[1:].split("\n")[0] for line in f.readlines()]

con = sqlite3.connect("C:/Users/S/desktop/바탕화면(임시)/KOSPI/tmp/KOSPI_Price_DB_merge_final.db")
df = pd.read_sql("select Date, Close, Close_noadj, Capital, OS_noadj from A000040", con, index_col= None)

# PBR 만들기
df = df.fillna(method="pad")
df = df[~df["Capital"].isna()]
df = df[df["Capital"] >0]
df.insert(len(df.columns), "BPS", (df["Capital"] / df["OS_noadj"])*100000000)
df.insert(len(df.columns), "PBR", (df["Close_noadj"] / df["BPS"]))
# df["PBR"]
plt.plot(df["PBR"])
plt.plot(df["Capital"])
plt.plot(df["OS_noadj"])
df["OS_noadj"]
df.index = range(len(df["Date"]))

for i in range(len(df["Date"])) :
    df["Date"][i] = df["Date"][i].split("-")[0]

df.insert(len(df.columns),"con_high",None)
df.insert(len(df.columns),"con_low",None)
Year_index = df.groupby("Date").mean().index

for Year in Year_index[:-1] :
    # Year = "2000" #tmp
    mean1 = "{0:.4f}".format(df.groupby('Date').mean()["PBR"]["%s" % Year])
    std1 = "{0:.4f}".format(df.groupby('Date').std()["PBR"]["%s" % Year])
    con_high = float(mean1) + 2 * float(std1)
    con_low = float(mean1) - 2 * float(std1)

    df["con_high"][df["Date"] == "%s" %str(int(Year)+1)] = con_high
    df["con_low"][df["Date"] == "%s" %str(int(Year)+1)] = con_low

df.to_excel("C:/Users/S/desktop/임시.xlsx")




pd.DataFrame.insert()
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

    # a = df[df["Date"]=="%s" %str(int(Year)+1)]
    # buy_index = list(a[a["PBR"] < con_low].index)
    # sell_index = list(a[a["PBR"] > con_high].index)






import pandas as pd
import sqlite3
import matplotlib.pyplot as plt

# 종목명, 코드 불러오기
with open("C:\\Users\\S\\Desktop\\바탕화면(임시)\\KOSPI\\KOSPI_codelist.txt", "r") as f:
    code_list = [line[1:].split("\n")[0] for line in f.readlines()]

con = sqlite3.connect("C:/Users/S/desktop/바탕화면(임시)/KOSPI/tmp/KOSPI_Price_DB_merge_final.db")




i = 1
for code in code_list :
    try :
        print(i, " / ", len(code_list))
        i += 1
        code = "A" + code
        code = "A000020" # tmp
        df = pd.read_sql("select Date, Close, Close_noadj, Capital, OS_noadj from %s" % code, con, index_col=None)
        # PBR 만들기
        df[~df["Capital"].isna()]
        df.insert(len(df.columns),"Quarter", None)
        df["Quarter"][~df["Capital"].isna()] = 1
        df = df[~df["Quarter"].isna()]
        df.insert(len(df.columns), "BPS", (df["Capital"] / df["OS_noadj"]) * 100000000)
        df.insert(len(df.columns), "PBR", df["Close_noadj"] / df["BPS"])
        df.insert(len(df.columns), "Market", df["Close_noadj"] * df["OS_noadj"])


        df = df.fillna(method="pad")
        df = df[~df["Capital"].isna()]
        df = df[df["Capital"] > 0]
        df.insert(len(df.columns), "BPS", (df["Capital"] / df["OS_noadj"]) * 100000000)
        df.insert(len(df.columns), "PBR", df["Close_noadj"] / df["BPS"])
        df.insert(len(df.columns), "Market", df["Close_noadj"] * df["OS_noadj"])

        # 분기별 구분
        # 분기별 리밸런싱 투자 성과 측정
        df
        df["Date"]
    except :continue


a = pd.read_excel("C:/Users/S/desktop/D_Finance_200124210113.xlsx")
a = pd.read_table("C:/Users/S/desktop/D_Finance_200124210113.xlsx")
a.columns
a["Unnamed: 0"][7]
a["Unnamed: 1"][7]
a.T