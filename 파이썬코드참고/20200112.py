"""
재무데이터와 종가데이터 합치는 작업
"""
import pandas as pd
import os

# 종목명, 코드 불러오기
f = open('c:\\Users\\S\\Desktop\\code_list.txt', 'r')
lines = f.readlines()
code_list = []
for line in lines:
        nline = line.split('\n')[0]
        code_list.append(nline)
f.close()

f = open('c:\\Users\\S\\Desktop\\name_list.txt', 'r')
lines = f.readlines()
name_list = []
for line in lines:
        nline = line.split('\n')[0]
        name_list.append(nline)
f.close()

# 재무데이터 불러오기
# file_list = os.listdir("C:\\Users\\S\\Desktop\\바탕화면(임시)\\KOSPI재무")
# file_list2 = []
# for file in file_list :
#     file_list2.append(file.split(".")[0])

df_1= pd.read_csv("C:\\Users\\S\\Desktop\\바탕화면(임시)\\KOSPI재무\\"+ code_list[0] + ".csv", encoding="euc-kr")
df_2= pd.read_csv("C:\\Users\\S\\Desktop\\바탕화면(임시)\\KOSPI재무2\\"+ code_list[0] + ".csv", encoding="euc-kr")
df_merge = pd.merge(df_1,df_2)
df_merge.columns
columns = ["Date","Price","Asset","Capital","Sales","Operating","Profit","Retention","CFO","CFI","CFF",
           "Op_Margin","Liability","Sa_Margin","non-operating","COGS","SGA","EBIT","NetCF",
           'BPS', 'CFPS', 'PSR', 'PER', 'SPS', 'div_rate', 'PBR', 'EBITDA','EPS', "EV/EB",
           'PayoutRatio', 'Return', 'DPS', 'PCR']
df_merge.columns = columns

# 결산년도 날짜데이터로 변환시키기
import re
r = re.compile("[0-9]+")
Dates = [r.findall(Date) for Date in df_merge["Date"]]
Dates2 = []

for i in range(len(Dates)) :
    if int(Dates[i][0]) > 21 :
        year = "19"+Dates[i][0]
    else :
        year = "20"+Dates[i][0]

    if Dates[i][1] == "03" :
        year += "0516"
    elif Dates[i][1] == "06" :
        year += "0816"
    elif Dates[i][1] == "09" :
        year += "1114"
    elif Dates[i][1] == "12" :
        year = str(int(year) + 1)
        year += "0331"
    else :
        print("잘못된 자료입니다.")
        exit()

    Dates2.append(year)

df_merge["Date"] = Dates2
df_merge["Date"] = pd.to_datetime(df_merge["Date"].astype(str))

# 재무데이터 변환 결과물
df_merge

# db에서 수정종가 데이터 가져오기
import sqlite3
con = sqlite3.connect("C:/Users/S/desktop/바탕화면(임시)/KOSPI/KOSPI최종.db")  # sqlite 연결 db 객체 생성
df = pd.read_sql("SELECT * FROM %s" %name_list[0], con, index_col=None) # SQLite DB 읽기

# Date열 날짜형으로 변환
df["Date"] = pd.to_datetime(df["Date"].astype(str))

con.close()

# 수정종가 데이터 변환 결과물
df


# 날짜 다시한번 맞춰주기
"""
수정종가 데이터가 2009년 11월 부터 밖에 없음 
"""
df_merge = df_merge[df_merge["Date"] > min(df["Date"])]
"""
재무데이터 날짜가 휴장일일 수 있기 때문에 가장 가까운 날짜로 변환
"""
Date = [] # 변수 초기화
Dates2 = [] # 변수 초기화
for Date in df_merge["Date"]:
    if not Date in list(df["Date"]) :
        Dates2.append(min(df["Date"][df["Date"] > Date]))
    else :
        Dates2.append(Date)

df_merge["Date"] = pd.Series(Dates2)

# 재무데이터, 수정종가데이터 합치기
df_fin = pd.merge(df,df_merge, how = "outer", on= "Date")
df_fin.to_csv("C:/Users/S/desktop/바탕화면(임시)/KOSPI/KOSPI최종.csv")



# for columns in df_merge.columns :
#     df.insert(len(df.columns),columns,df_merge["%s" % columns])


# DB에서 데이터 가져오기
import sqlite3
import pandas as pd
con = sqlite3.connect("C:/Users/S/desktop/바탕화면(임시)/KOSPI/KOSPI최종2.db")  # sqlite 연결 db 객체 생성
df = pd.read_sql("SELECT * FROM 경방", con, index_col=None)# SQLite DB 읽기
df["BPS"]

