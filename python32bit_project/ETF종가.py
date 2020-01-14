"ETF 종가 가져오기"

import win32com.client
import pandas as pd
import time


### 연결상태 확인 1: 연결, 0: 비연결
instCpCybos = win32com.client.Dispatch("CpUtil.CpCybos")
print(instCpCybos.IsConnect)

# ETF에 해당하는 종목만 코드 추출
instCpCodeMgr = win32com.client.Dispatch("CpUtil.CpCodeMgr")
codeList = instCpCodeMgr.GetStockListByMarket(1)

ETF_codelist = []
ETF_namelist = []
for i, code in enumerate(codeList):
    secondCode = instCpCodeMgr.GetStockSectionKind(code)
    if secondCode == 10 :
        ETF_namelist.append(instCpCodeMgr.CodeToName(code))  # ETF명
        ETF_codelist.append(code)

instStockChart = win32com.client.Dispatch("CpSysDib.StockChart")
i = 0
ETF_Data_2 = pd.DataFrame({"하하":[1, 2, 3]})

# ETF_codelist = ['A069500','A069660','A139230','A174360'] # 임시
for code2 in ETF_codelist :
    print(i)
    instStockChart.SetInputValue(0, code2)  # 종목코드
    instStockChart.SetInputValue(1, ord('1'))
    instStockChart.SetInputValue(2, 20191231)  # 요청 종료 날짜 지정
    instStockChart.SetInputValue(3, 20001231)  # 요청 시작 날짜 지정
    instStockChart.SetInputValue(5, (0, 5)) # 데이터의 종류, 날짜, 종가
    instStockChart.SetInputValue(6, ord('D'))  # 차트의 종류, D : 일단위 데이터
    instStockChart.SetInputValue(9, ord('1'))  # 수정 주가의 반영 여부, 1 : 반영
    time.sleep(0.255)
    instStockChart.BlockRequest()
    numData = instStockChart.GetHeaderValue(3)

    Date = []
    Close = []

    for j in range(numData):
        Date.append(instStockChart.GetDataValue(0,j))
        Close.append(instStockChart.GetDataValue(1,j))

    ETF_Data_1 = pd.DataFrame({ETF_codelist[i] : Date, ETF_namelist[i] : Close})

    ETF_Data_2 = pd.concat([ETF_Data_2,ETF_Data_1], axis=1)

    i += 1

# ETF 데이터 저장
ETF_Data_2.to_csv('c:\\Users\\S\\Desktop\\ETF2.csv', encoding= "euc-kr")





