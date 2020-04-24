" 반드시 32bit python 에서 실행 "

# CpUtil.CpCybos
"""
CYBOS의 각종 상태를 확인할 수 있음.
"""
# 연결상태 확인 1: 연결, 0: 비연결
import win32com.client
instCpCybos = win32com.client.Dispatch("CpUtil.CpCybos")
print(instCpCybos.IsConnect)

# CpSysDib.MarketEye
"""
주식,지수,선물/옵션등의 여러 종목의 필요항목들을 한번에 수신합니다. 
"""

# 펀더멘털 데이터 요청
import win32com.client
instMarketEye = win32com.client.Dispatch("CpSysDib.MarketEye")
instMarketEye.SetInputValue(0, (4, 67, 70, 111)) # 데이터 Input, (현재가, PER, EPS, 최근분기년월)
instMarketEye.SetInputValue(1, 'A003540')
instMarketEye.BlockRequest() # 데이터 요청

print("현재가: ", instMarketEye.GetDataValue(0, 0))
print("PER: ", instMarketEye.GetDataValue(1, 0))
print("EPS: ", instMarketEye.GetDataValue(2, 0))
print("최근분기년월: ", instMarketEye.GetDataValue(3, 0))


# CpUtil.CpCodeMgr
"""
각종코드정보 및 코드리스트를 얻을 수 있습니다.
"""
# ETF, ETN, 주식 구분
import win32com.client

instCpCodeMgr = win32com.client.Dispatch("CpUtil.CpCodeMgr") # 객체 생성
codeList = instCpCodeMgr.GetStockListByMarket(1) # 1 : 거래소
print(codeList)

ETF_list = []
for i, code in enumerate(codeList):
    secondCode = instCpCodeMgr.GetStockSectionKind(code)
    if secondCode == 10 : # secondCode 값이 1이면 주식, 10 : ETF, 17 : ETN 확인 가능
        name = instCpCodeMgr.CodeToName(code)
        ETF_list.append((code))
        print(i, code, secondCode, name)

print(len(ETF_list)) # 450 개 ETF 종목 코드 및 이름

# CpTrade.CpTdUtil
"""
주문 오브젝트를 사용하기 위해 필요한 초기화 과정들을 수행한다
"""
# CpTrade.CpTd0311
"""
장내주식/코스닥주식/ELW주문(현금주문) 데이터를 요청하고수신한다
"""

# 매수/매도하기
"모의투자로 접속 후 실행"
import win32com.client
instCpTdUtil = win32com.client.Dispatch("CpTrade.CpTdUtil") # 객체 생성
instCpTd0311 = win32com.client.Dispatch("CpTrade.CpTd0311")
instCpTdUtil.TradeInit() # 초기화

accountNumber = instCpTdUtil.AccountNumber[0] # 계좌번호

# 데이터 인풋
instCpTd0311.SetInputValue(0, 2) # 매수 주문
instCpTd0311.SetInputValue(1, accountNumber) # 수행할 계좌
instCpTd0311.SetInputValue(3, 'A003540') # 종목
instCpTd0311.SetInputValue(4, 10) # 수량
instCpTd0311.SetInputValue(5, 13000) # 단가

instCpTd0311.BlockRequest() # 주문 내역은 현재 여기서 확인 불가


# DsCbo1.StockMst
"""
종목관련 데이터 구하기 
"""
# 종목코드 리스트 구하기
objStockMst = win32com.client.Dispatch("DsCbo1.StockMst")
objStockMst.SetInputValue(0, 'A005930')   #종목 코드 - 삼성전자
objStockMst.BlockRequest()

# 현재가 통신 및 통신 에러 처리
rqStatus = objStockMst.GetDibStatus()
rqRet = objStockMst.GetDibMsg1()
print("통신상태", rqStatus, rqRet)
if rqStatus != 0: # 0 이 아니면 통신 에러
    exit()

# 현재가 정보 조회
code = objStockMst.GetHeaderValue(0)  # 종목코드
name = objStockMst.GetHeaderValue(1)  # 종목명
time = objStockMst.GetHeaderValue(4)  # 시간
cprice = objStockMst.GetHeaderValue(11)  # 종가
diff = objStockMst.GetHeaderValue(12)  # 대비
open = objStockMst.GetHeaderValue(13)  # 시가
high = objStockMst.GetHeaderValue(14)  # 고가
low = objStockMst.GetHeaderValue(15)  # 저가
offer = objStockMst.GetHeaderValue(16)  # 매도호가
bid = objStockMst.GetHeaderValue(17)  # 매수호가
vol = objStockMst.GetHeaderValue(18)  # 거래량
vol_value = objStockMst.GetHeaderValue(19)  # 거래대금

# 예상 체결관련 정보
exFlag = objStockMst.GetHeaderValue(58)  # 예상체결가 구분 플래그
exPrice = objStockMst.GetHeaderValue(55)  # 예상체결가
exDiff = objStockMst.GetHeaderValue(56)  # 예상체결가 전일대비
exVol = objStockMst.GetHeaderValue(57)  # 예상체결수량

print("코드", code)
print("이름", name)
print("시간", time)
print("종가", cprice)
print("대비", diff)
print("시가", open)
print("고가", high)
print("저가", low)
print("매도호가", offer)
print("매수호가", bid)
print("거래량", vol)
print("거래대금", vol_value)


# DsCbo1.StockWeek
"""
일자별 데이터
"""
import win32com.client

objStockWeek = win32com.client.Dispatch("DsCbo1.StockWeek")
objStockWeek.SetInputValue(0, 'A005930')   #종목 코드 - 삼성전자
objStockWeek.BlockRequest() # 데이터 요청
count = objStockWeek.GetHeaderValue(1) # 데이터 수

# 일자별 데이터 요청
def ReqeustData(obj):
    # 데이터 요청
    obj.BlockRequest()

    # 통신 결과 확인
    rqStatus = obj.GetDibStatus()
    rqRet = obj.GetDibMsg1()
    print("통신상태", rqStatus, rqRet)
    if rqStatus != 0:
        return False

    # 일자별 정보 데이터 처리
    count = obj.GetHeaderValue(1)  # 데이터 개수
    for i in range(count):
        date = obj.GetDataValue(0, i)  # 일자
        open = obj.GetDataValue(1, i)  # 시가
        high = obj.GetDataValue(2, i)  # 고가
        low = obj.GetDataValue(3, i)  # 저가
        close = obj.GetDataValue(4, i)  # 종가
        diff = obj.GetDataValue(5, i)  # 종가
        vol = obj.GetDataValue(6, i)  # 종가
        print(date, open, high, low, close, diff, vol)

    return True

ret = ReqeustData(objStockWeek)
if ret == False:
    exit()

# CpSysDib.StockChart
""" 
차트 데이터 구하기
"""
import win32com.client

objStockChart = win32com.client.Dispatch("CpSysDib.StockChart") # 객체 생성

objStockChart.SetInputValue(0, 'A005930')  # 종목 코드 - 삼성전자
objStockChart.SetInputValue(1, ord('2'))  # 개수로 조회
objStockChart.SetInputValue(4, 100)  # 최근 100일 치
objStockChart.SetInputValue(5, [0, 2, 3, 4, 5, 8])  # 날짜,시가,고가,저가,종가,거래량
objStockChart.SetInputValue(6, ord('T'))  # '차트 주가 - 일간 차트 요청
objStockChart.SetInputValue(9, ord('1'))  # 수정주가 사용
objStockChart.BlockRequest()

len = objStockChart.GetHeaderValue(3)

print("날짜", "시가", "고가", "저가", "종가", "거래량")
print("--==============================================-")

for i in range(len):
    day = objStockChart.GetDataValue(0, i)
    open = objStockChart.GetDataValue(1, i)
    high = objStockChart.GetDataValue(2, i)
    low = objStockChart.GetDataValue(3, i)
    close = objStockChart.GetDataValue(4, i)
    vol = objStockChart.GetDataValue(5, i)
    print(day, open, high, low, close, vol)

# 기간으로 데이터 요청
objStockChart.SetInputValue(1, ord('1'))
objStockChart.SetInputValue(2, 20161031) # 요청 종료 날짜 지정
objStockChart.SetInputValue(3, 20161020) # 요청 시작 날짜 지정

objStockChart.BlockRequest()
numData = objStockChart.GetHeaderValue(3)
numField = objStockChart.GetHeaderValue(1)

for i in range(numData):
    for j in range(numField):
        print(objStockChart.GetDataValue(j, i), end=" ") # 원래 줄바꿈으로 지정되어있는 값을 띄어쓰기로 바꿈
    print("")

# 거래량 관련 알고리즘 예제
import win32com.client

# Create object
instStockChart = win32com.client.Dispatch("CpSysDib.StockChart")

# SetInputValue
instStockChart.SetInputValue(0, "A003540")
instStockChart.SetInputValue(1, ord('2'))
instStockChart.SetInputValue(4, 60) # 60일치 거래량
instStockChart.SetInputValue(5, 8)
instStockChart.SetInputValue(6, ord('D'))
instStockChart.SetInputValue(9, ord('1'))

# BlockRequest
instStockChart.BlockRequest()

# GetData
volumes = []
numData = instStockChart.GetHeaderValue(3)
for i in range(numData):
    volume = instStockChart.GetDataValue(0, i)
    volumes.append(volume)
print(volumes)

# 거래량 1000% 증가 확인하기
averageVolume = (sum(volumes) - volumes[0]) / (len(volumes) -1) # 최근일 제외하고 59일간의 평균 거래량

if(volumes[0] > averageVolume * 10):
    print("대박 주")
else:
    print("일반 주", volumes[0] / averageVolume)

# 전 종목에 대해 거래량 급증여부 체크 알고리즘
"""
함수를 작성할 때는 함수의 인자를 어떻게 구성할지가 중요
CheckVolumn 함수는 함수 내부에서 StockChart 인스턴스를 생성하지 않고 함수를 호출하는 곳에서 인스턴스를 생성하는 구조
만약 함수 내에서 인스턴스를 생성하도록 구현한다면 함수가 호출될 때마다 인스턴스가 생성됐다가 함수가 종료되면 인스턴스도 소멸해야 하므로 프로그램이 느려짐
"""
import win32com.client
import time

def CheckVolumn(instStockChart, code): # 함수 생성
    # SetInputValue
    instStockChart.SetInputValue(0, code)
    instStockChart.SetInputValue(1, ord('2'))
    instStockChart.SetInputValue(4, 60)
    instStockChart.SetInputValue(5, 8)
    instStockChart.SetInputValue(6, ord('D'))
    instStockChart.SetInputValue(9, ord('1'))

    # BlockRequest
    instStockChart.BlockRequest()

    # GetData
    volumes = []
    numData = instStockChart.GetHeaderValue(3)
    for i in range(numData):
        volume = instStockChart.GetDataValue(0, i)
        volumes.append(volume)

    # Calculate average volume
    averageVolume = (sum(volumes) - volumes[0]) / (len(volumes) -1)

    if(volumes[0] > averageVolume * 10):
        return 1
    else:
        return 0

if __name__ == "__main__":
    instStockChart = win32com.client.Dispatch("CpSysDib.StockChart")
    instCpCodeMgr = win32com.client.Dispatch("CpUtil.CpCodeMgr")
    codeList = instCpCodeMgr.GetStockListByMarket(1)

    buyList = []
    i = 1
    codeList = codeList[0:9] # 임시로 10개만
    for code in codeList:
        print(i)
        i += 1
        if CheckVolumn(instStockChart, code) == 1:
            buyList.append(code)
            print(code)
        time.sleep(1)
