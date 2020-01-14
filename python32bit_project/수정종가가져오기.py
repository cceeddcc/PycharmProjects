# def get_stockprice() : # 수정주가 가져오기
# 기간 , 거래소, 코스닥 구분

import win32com.client
import pandas as pd
import time
import sqlite3
import os

import Cybos_function
Cybos_function.Get_login_status() # 로그인 확인
Kospi_codelist, Kospi_namelist = Cybos_function.Get_KOSPI_code() # 코스피 코드리스트 가져오기

# 데이터 추출
instStockChart = win32com.client.Dispatch("CpSysDib.StockChart")
i = 1
Kospi_codelist = ['A000020', 'A000040', 'A000050', 'A000060'] # 테스트용
con = sqlite3.connect("C:/Users/S/desktop/바탕화면(임시)/KOSPI/KOSPI(1995~2020).db")  # sqlite 연결 db 객체 생성

for code in Kospi_codelist :
    print((i),"/", len(Kospi_codelist))
    instStockChart.SetInputValue(0, code)  # 종목코드
    instStockChart.SetInputValue(1, ord('1')) # 기간 요청
    instStockChart.SetInputValue(2, 20200130)  # 요청 종료 날짜 지정
    instStockChart.SetInputValue(3, 19951231)  # 요청 시작 날짜 지정
    instStockChart.SetInputValue(5, (0, 2,3,4,5,8,9, 12)) # 데이터의 종류, 날짜, 시고저종, 거래량, 거래대금 , 상장주식수
    instStockChart.SetInputValue(6, ord('D'))  # 차트의 종류, D : 일단위 데이터
    instStockChart.SetInputValue(9, ord('1'))  # 수정 주가의 반영 여부, 1 : 반영
    time.sleep(0.255)
    instStockChart.BlockRequest()
    numData = instStockChart.GetHeaderValue(3)

    Date = []
    Open = []
    High = []
    Low = []
    Close = []
    Volume = []
    Transaction = [] # 거래대금
    ShareNum = [] # 상장주식수

    for j in range(numData):
        Date.append(instStockChart.GetDataValue(0,j))
        Open.append(instStockChart.GetDataValue(1,j))
        High.append(instStockChart.GetDataValue(2,j))
        Low.append(instStockChart.GetDataValue(3,j))
        Close.append(instStockChart.GetDataValue(4,j))
        Volume.append(instStockChart.GetDataValue(5,j))
        Transaction.append(instStockChart.GetDataValue(6,j))
        ShareNum.append(instStockChart.GetDataValue(7,j))

    Kospi_Data = pd.DataFrame({"Date" : Date,
                               "Open" : Open,
                               "High" : High,
                               "Low" : Low,
                               "Close" : Close,
                               "Volume" : Volume,
                               "Transaction" : Transaction,
                               "ShareNum" : ShareNum
                               })
    # SQLite DB로 저장
    try :
        Kospi_Data.to_sql(Kospi_namelist[i],con, index=False)
    except : pass

    i += 1



# DB에서 데이터 가져오기
import sqlite3

con = sqlite3.connect("C:/Users/S/desktop/바탕화면(임시)/KOSPI/KOSPI최종2.db")  # sqlite 연결 db 객체 생성
df = []
index = Kospi_namelist[0:2]
for i in range(2) :
    df.append(pd.read_sql("SELECT * FROM %s" %Kospi_namelist[i], con, index_col=None)) # SQLite DB 읽기

s = pd.Series(df,index=index)
s.head()

s["동화약품"]







