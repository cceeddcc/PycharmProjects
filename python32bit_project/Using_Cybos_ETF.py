import win32com.client
import os
import Cybos_function

os.getcwd()
os.chdir("C:/Users/S/Desktop/")

# Cybos Plus연결 여부 체크
Cybos_function.Get_login_status()

# ETF 일일데이터 분석 객체 생성
objETF = win32com.client.Dispatch("Dscbo1.CpSvr7246")

# 데이터 수신 및 저장
ETF_df = Cybos_function.ETF_GetData(objETF, "225130")
ETF_df.to_excel("tmp2.xlsx")


