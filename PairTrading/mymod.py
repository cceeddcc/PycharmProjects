import pandas as pd
import sys
import os
import numpy as np
import sqlite3 as sql
import statsmodels.api as stm


"""
for saving my code, method
"""
def road_KOSPI_codename():
    """
    KOSPI 종목명, 코드 불러오기 위함
    """
    with open("C:\\Users\\S\\Desktop\\바탕화면(임시)\\KOSPI\\KOSPI_codelist.txt", "r") as f:
        code_list = [line[1:].split("\n")[0] for line in f.readlines()]

    with open("C:\\Users\\S\\Desktop\\바탕화면(임시)\\KOSPI\\KOSPI_namelist.txt", "r") as f:
        name_list = [line.split("\n")[0] for line in f.readlines()]

    code_dict = {}
    for i in range(0, len(code_list)):
        code_dict["%s" % name_list[i]] = code_list[i]

    return code_dict, code_list, name_list

# code_dict, code_list, name_list = road_KOSPI_codename()


start = "2012-01-02" # tmp
end = "2015-01-01" # tmp
num_data = 200  # tmp
def road_KOSPI_data_db(start, end, num_data):
    """
    db에서 KOSPI log price 데이터 불러오기 위함
    """
    os.chdir("C:/Users/S/Desktop/바탕화면(임시)/KOSPI/")
    date = pd.date_range(start,end)
    df_kospi = pd.DataFrame({"Date" : date})
    con = sql.connect("KOSPI_Price_DB_merge_final.db")

    code_dict, code_list, name_list = road_KOSPI_codename()
    t = 1

    for code in code_list[:num_data]:
        try :
            code = code_list[0] # tmp
            print(t, " / " , len(code_list))
            code = "A" + code
            df = pd.read_sql("select Date, Close from %s" %code, con, index_col= None)
            df["Date"] = pd.to_datetime(df["Date"])
            df["log_%s" %code] = np.log(df["Close"])
            df = df.iloc[:,[0,2]]
            df = df[df["Date"] >= start]
            df = df[df["Date"] <= end]
            df_kospi = df_kospi.merge(df, how="left", on="Date")
            df_kospi = df_kospi.dropna()
            len(df_kospi.index)
            t += 1
        except :
            t += 1
            continue
    con.close()

    df_kospi = df_kospi.dropna()