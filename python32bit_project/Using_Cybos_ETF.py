import win32com.client
import os
import Cybos_function
import sqlite3

os.chdir("C:\\Users\\S\\Desktop\\바탕화면(임시)\\ETF\\")
os.getcwd()

# Cybos Plus연결 여부 체크
Cybos_function.Get_login_status()

# ETF code, name 불러오기
ETF_code_list, ETF_name_list = Cybos_function.Get_ETF_code_name()

# ETF 코드 및 종목명 txt파일로 저장
with open("ETF_code_list.txt", "w") as f :
    for code in ETF_code_list :
        f.write(code + "\n")
with open("ETF_name_list.txt", "w") as f :
    for name in ETF_name_list :
        f.write(name + "\n")

# ETF 일일데이터 객체 생성
objETF = win32com.client.Dispatch("Dscbo1.CpSvr7246")

# 데이터 수신 및 DB에 저장
count = 1
con = sqlite3.connect("tmp/ETF.db")
for code in ETF_code_list :
    try :
        print(count, " / " , len(ETF_code_list))
        count += 1
        ETF_df = Cybos_function.ETF_GetData(objETF, code)
        ETF_df.to_sql(code, con, index=False)

    except :
        print("오류 : ", code)
        continue
con.close()


