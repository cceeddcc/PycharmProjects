import sqlite3
import pandas as pd
import os
os.getcwd()
os.chdir("C:/Users/S/Desktop/바탕화면(임시)/ETF/")

# ETF 종목명, 코드 불러오기
with open("ETF_code_list.txt", "r") as f:
    ETF_code_list = [line.split("\n")[0] for line in f.readlines()]
with open("ETF_name_list.txt", "r") as f:
    ETF_name_list = [line.split("\n")[0] for line in f.readlines()]

# DB에서 ETF 데이터 불러오기
con = sqlite3.connect("tmp/ETF.db")
con2 = sqlite3.connect("tmp/ETF_v0.2.db") # 신규 저장할 DB
count = 1
for code in ETF_code_list :
    try:
        print(count, " / ", len(ETF_code_list))
        count += 1
        ETF_df = pd.read_sql("select * from %s" %code, con, index_col=None)

        # 데이터 수정
        """
        새로운 계산 열 추가
        """
        ETF_df.insert(len(ETF_df.columns), "Close1", ETF_df["Close"].shift(1))
        ETF_df.insert(len(ETF_df.columns), "Close_return", (ETF_df["Close"]/ETF_df["Close1"])-1)
        ETF_df.insert(len(ETF_df.columns), "NAV1", ETF_df["NAV"].shift(1))
        ETF_df.insert(len(ETF_df.columns), "NAV_return", (ETF_df["NAV"]/ETF_df["NAV1"])-1)
        ETF_df = ETF_df.fillna(value=0)
        ETF_df.insert(len(ETF_df.columns), "Cum_Close_return", ETF_df["Close_return"].cumsum())
        ETF_df.insert(len(ETF_df.columns), "Cum_NAV_return", ETF_df["NAV_return"].cumsum())
        ETF_df.insert(len(ETF_df.columns), "dif_CCR_CNR", ETF_df["Cum_Close_return"]-ETF_df["Cum_NAV_return"])

        # 데이터 DB 저장
        ETF_df.to_sql(code, con2, index=False)

    except :
        print("오류 : ", code)
        continue

con.close()
con2.close()


# 분석
"""
ETF가격 등락률 누적 = ETF NAV 등락률 누적
검증 결과 만족하는 것으로 보임 
"""
con = sqlite3.connect("tmp/ETF_v0.2.db")
count = 1
mindif = []
maxdif = []
avgdif = []
for code in ETF_code_list :
    try:
        # code = ETF_code_list[0]
        print(count, " / ", len(ETF_code_list))
        count += 1
        ETF_df = pd.read_sql("select * from %s" %code, con, index_col=None)
        mindif.append(min(ETF_df["dif_CCR_CNR"])*100)
        maxdif.append(max(ETF_df["dif_CCR_CNR"])*100)
        avgdif.append(ETF_df["dif_CCR_CNR"].mean()*100)
    except :
        print("오류 : ", code)
        continue

con.close()

df1 = pd.DataFrame({"mindif" : mindif,
                    "maxdif" : maxdif,
                    "avgdif" : avgdif})

# df1.to_excel("C:/Users/S/Desktop/tmp1.xlsx")


# Corr 기준으로 ETF 짝짓기
con = sqlite3.connect("tmp/ETF_v0.2.db")
count = 1
NAV_merge = pd.DataFrame()
for code in ETF_code_list :
    try:
        # code = ETF_code_list[0] # tmp
        print(count, " / ", len(ETF_code_list))
        count += 1
        ETF_df = pd.read_sql("select NAV_return from %s" %code, con, index_col=None)
        NAV_merge.insert(len(NAV_merge.columns),code,ETF_df["NAV_return"])
    except :
        print("오류 : ", code)
        continue

con.close()

# ETF code,name 변환용 dict 변수생성
ETF_code_name_dict = {}
i = 0
for i in range(0,len(ETF_name_list)) :
    ETF_code_name_dict[ETF_code_list[i]] = ETF_name_list[i]
ETF_code_name_dict

# corr matrix 생성
NAV_corr_matrix = NAV_merge.corr()


# 양의 상관관계 묶기
i = 0
plus_group_codedict = {}
plus_group_namedict = {}
for i in range(0,len(NAV_corr_matrix.columns)) :
# for i in range(0,9) : # tmp
    plus_group_codelist = []
    plus_group_namelist = []
    plus_group = NAV_corr_matrix[NAV_corr_matrix > 0.90].iloc[i].dropna().index
    for code in plus_group:
        plus_group_codelist.append(code)
        plus_group_namelist.append(ETF_code_name_dict[code])
    plus_group_codedict[i] = plus_group_codelist
    plus_group_namedict[i] = plus_group_namelist

# 중복제거
plus_group_codelist = []
plus_group_namelist = []
for value in plus_group_codedict.values() :
    if value in plus_group_codelist :
        continue
    plus_group_codelist.append(value)

for value in plus_group_namedict.values() :
    if value in plus_group_namelist :
        continue
    plus_group_namelist.append(value)

last_group = []
for last in plus_group_codelist :
    if len(last) == 1 :
        continue
    else :
        last_group.append(last)

last_group_name = []
for last in plus_group_namelist :
    if len(last) == 1 :
        continue
    else :
        last_group_name.append(last)


# 최종결과물
last_group
last_group_name
df_group_name = pd.DataFrame(last_group_name)
df_group_code = pd.DataFrame(last_group)

df_group_name.to_excel("동일기초자산ETF명2.xlsx")
df_group_code.to_excel("동일기초자산ETF코드명2.xlsx")
#
# # 음의 상관관계 묶기
# i = 0
# minus_group_codedict = {}
# minus_group_namedict = {}
# for i in range(0,len(NAV_corr_matrix.columns)) :
# # for i in range(0, 9):  # tmp
#     minus_group_codelist = []
#     minus_group_namelist = []
#     minus_group = NAV_corr_matrix[NAV_corr_matrix > 0.97].iloc[i].dropna().index
#     for code in minus_group:
#         minus_group_codelist.append(code)
#         minus_group_namelist.append(ETF_code_name_dict[code])
#     minus_group_codedict[i] = minus_group_codelist
#     minus_group_namedict[i] = minus_group_namelist
#
# # 중복제거
# minus_group_codelist = []
# minus_group_namelist = []
# for value in minus_group_codedict.values():
#     if value in minus_group_codelist:
#         continue
#     if len(minus_group_codelist[0]) == 1:
#         continue
#     minus_group_codelist.append(value)
#
# for value in minus_group_namedict.values():
#     if value in minus_group_namelist:
#         continue
#     if len(minus_group_namelist[0]) == 1:
#         continue
#     minus_group_namelist.append(value)


