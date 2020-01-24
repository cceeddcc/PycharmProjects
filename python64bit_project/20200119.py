import numpy as np
import statsmodels.api as sm
import statsmodels.formula.api as smf
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt

# 종목명, 코드 불러오기
with open("C:\\Users\\S\\Desktop\\바탕화면(임시)\\KOSPI\\KOSPI_codelist.txt", "r") as f :
    code_list = [line.split("\n")[0] for line in f.readlines()]

with open("C:\\Users\\S\\Desktop\\바탕화면(임시)\\KOSPI\\KOSPI_namelist.txt", "r") as f :
    name_list = [line.split("\n")[0] for line in f.readlines()]

codetoname = {}
for i in range(len(code_list)):
    codetoname["%s" %code_list[i]] = name_list[i]

con = sqlite3.connect("C:/Users/S/desktop/바탕화면(임시)/KOSPI/tmp/KOSPI_PriceFinance_DB.db")
i = 0
PBR_dict ={}
for code in code_list :
    try :
        # code = "A000020"
        print(i, "/", len(code_list))
        i += 1
        df = pd.read_sql("select Date, Close, BPS from %s" %code,con,index_col=None)
        df = df.fillna(method="pad")
        df = df[~df["BPS"].isna()]
        df = df[df["BPS"] >0]
        df.insert(len(df.columns), "PBR", df["Close"] / df["BPS"])
        df = df[df["Date"] > "2015"]
        PBR_dict["%s" %code] = "{0:.3f}".format(min(df["PBR"]))
        # plt.plot(df["PBR"], color="red")
        # plt.plot(df["Close"], color="blue")
    except : continue

a = list(PBR_dict.values())
plt.plot(a, "ro")
min(a)
max(a)
PBR_dict
PBR_dict_sort = sorted(PBR_dict.items(), key=(lambda x:x[1]))
PBR_dict_sort[0:20]
PBR_dict_sort[-21:-1]
code= "A001470"
df = pd.read_sql("select Date, Close, BPS from %s" %code,con,index_col=None)
df = df.fillna(method="pad")
df = df[~df["BPS"].isna()]
df = df[df["BPS"] >0]
df.insert(len(df.columns), "PBR", df["Close"] / df["BPS"])
df = df[df["Date"] > "2015"]
plt.plot(df["PBR"])
codetoname[code]



con.close()








A=list(PBR_dict.values())
for name,value in PBR_dict.items() :
    if value < -17 :
        print(name)

B=pd.Series(A)
plt.plot(B,"ro")

B=B[B>-50]