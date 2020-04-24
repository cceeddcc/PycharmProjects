import win32com.client
import os
import sqlite3
from datetime import datetime, timedelta
import time
import pandas as pd
import sys
import random
os.getcwd()
sys.path

"""
Cybos를 활용해서 금융 시계열 데이터를 DB에 저장하기 위해 생성 
"""
KOSPI_codelist = []
KOSPI_namelist = []
error_codelist = []

# 공통 함수
def Get_login_status():
    """
    Cybos plus 로그인 상태 확인 및 연결
    """
    objCpCybos = win32com.client.Dispatch("CpUtil.CpCybos")

    # 1: 연결, 0: 비연결
    if objCpCybos.IsConnect == 1:
        print("정상적으로 연결되었습니다.")
        return True
    else:
        print("CybosPlus가 연결되어있지 않습니다.")
        os.startfile("C:\\Users\\S\\Desktop\\CybosPlus.lnk")
        return False


# 코스피 관련 함수
def Get_KOSPI_code():
    """
    Get the KOSPI codes
    """
    try :
        objCpCodeMgr = win32com.client.Dispatch("CpUtil.CpCodeMgr")
        tmp_code_list = objCpCodeMgr.GetStockListByMarket(1)  # KOSPI

        # 코스피 보통주만 선별
        global KOSPI_codelist
        global KOSPI_namelist
        KOSPI_codelist = [code[1:] for code in tmp_code_list
                          if code[-1] == "0" and objCpCodeMgr.GetStockSectionKind(code) == 1]
        KOSPI_namelist = [objCpCodeMgr.CodeToName(code) for code in KOSPI_codelist]
        print("정상적으로 처리되었습니다.")
        return KOSPI_codelist, KOSPI_namelist

    except :
        print("오류")
        pass

def Get_KOSPI_Industry(code):
    """
    Get the KOSPI Industry
    """
    try :
        objCpCodeMgr = win32com.client.Dispatch("CpUtil.CpCodeMgr")
        tmp_code_list = objCpCodeMgr.GetStockIndustryCode(code)
        return tmp_code_list

    except:
        print("오류")
    pass

def Get_KOSPI_Data_adj(*code_list,SDate,EDate,DBname):
    """
    :param code_list: Kospi_codelist
    :param SDate: Start Date ex) 20190101
    :param EDate: End Date ex) 20200101
    :param DBname: DB name
    :return: 코스피 주가관련 데이터 반환
    """
    instStockChart = win32com.client.Dispatch("CpSysDib.StockChart")
    con = sqlite3.connect("C:/Users/S/desktop/바탕화면(임시)/KOSPI/tmp/" + DBname + ".db")  # sqlite 연결 db 객체 생성
    i = 1
    try :
        for code in code_list:
            code = "A" + code
            print((i), "/", len(code_list))
            instStockChart.SetInputValue(0, code)  # 종목코드
            instStockChart.SetInputValue(1, ord('1'))  # 기간 요청
            instStockChart.SetInputValue(2, EDate)  # 요청 종료 날짜 지정
            instStockChart.SetInputValue(3, SDate)  # 요청 시작 날짜 지정
            instStockChart.SetInputValue(5, (0, 2, 3, 4, 5, 8, 9, 12, 14, 15, 16, 17, 20, 21))  # 데이터의 종류
            instStockChart.SetInputValue(6, ord('D'))  # 차트의 종류, D : 일단위 데이터
            instStockChart.SetInputValue(9, ord('1'))  # 수정 주가의 반영 여부, 0:무수정 주가 1 : 반영
            time.sleep(0.255)
            instStockChart.BlockRequest()
            numData = instStockChart.GetHeaderValue(3)

            Date = []
            Open = []
            High = []
            Low = []
            Close = []
            Volume = []
            Transaction = []  # 거래대금
            ShareNum = []  # 상장주식수
            Foreign_1 = []  # 외국인주문한도수량
            Foreign_2 = []  # 외국인주문가능수량
            Foreign_3 = []  # 외국인현보유수량
            Foreign_4 = []  # 외국인현보유비율
            Company_1 = []  # 기관순매수
            Company_2 = []  # 기관누적순매수


            for j in range(numData):
                Date.append(str(instStockChart.GetDataValue(0, j)))
                Open.append(instStockChart.GetDataValue(1, j))
                High.append(instStockChart.GetDataValue(2, j))
                Low.append(instStockChart.GetDataValue(3, j))
                Close.append(instStockChart.GetDataValue(4, j))
                Volume.append(instStockChart.GetDataValue(5, j))
                Transaction.append(instStockChart.GetDataValue(6, j))
                ShareNum.append(instStockChart.GetDataValue(7, j))
                Foreign_1.append(instStockChart.GetDataValue(8, j))
                Foreign_2.append(instStockChart.GetDataValue(9, j))
                Foreign_3.append(instStockChart.GetDataValue(10, j))
                Foreign_4.append(instStockChart.GetDataValue(11, j))
                Company_1.append(instStockChart.GetDataValue(12, j))
                Company_2.append(instStockChart.GetDataValue(13, j))


            Kospi_Data = pd.DataFrame({"Date": Date,
                                       "Open": Open,
                                       "High": High,
                                       "Low": Low,
                                       "Close": Close,
                                       "Volume": Volume,
                                       "Transaction": Transaction,
                                       "ShareNum": ShareNum,
                                       "Foreign_1": Foreign_1,
                                       "Foreign_2": Foreign_2,
                                       "Foreign_3": Foreign_3,
                                       "Foreign_4": Foreign_4,
                                       "Company_1": Company_1,
                                       "Company_2": Company_2
                                       })
            Kospi_Data= Kospi_Data.sort_values(by="Date")
            # SQLite DB로 저장
            try:
                Kospi_Data.to_sql(code, con, index=False)
            except:
                print(code, "오류")
                pass

            i += 1

    except :
        print("오류")
        pass

    con.close()
    return "정상적으로 완료했습니다."

def Update_KOSPI_Data(*code_list, DBname):
    instStockChart = win32com.client.Dispatch("CpSysDib.StockChart")
    con = sqlite3.connect("C:/Users/S/desktop/바탕화면(임시)/KOSPI/tmp/" + DBname + ".db")
    cur = con.cursor()
    CDate = int(datetime.today().strftime("%Y%m%d"))
    global error_codelist

    i = 1
    for code in code_list:
        try:
            print((i), "/", len(code_list))
            i += 1
            code = "A" + code
            cur.execute('select Date from %s' % code)
            a = cur.fetchall()[-1][0].split(" ")[0].replace("-","")
            SDate = datetime.strptime(a, "%Y%m%d") + timedelta(days=+1)
            SDate = int(SDate.strftime("%Y%m%d"))

            if SDate >= CDate :
                print("오류 : " + code +" 시작날짜가 오늘날짜와 같거나 큽니다.")
                error_codelist.append(code)
                continue

            else:
                instStockChart.SetInputValue(0, code)  # 종목코드
                instStockChart.SetInputValue(1, ord('1'))  # 기간 요청
                instStockChart.SetInputValue(2, CDate)  # 요청 종료 날짜 지정
                instStockChart.SetInputValue(3, SDate)  # 요청 시작 날짜 지정
                instStockChart.SetInputValue(5, (0, 2, 3, 4, 5, 8, 9, 12))  # 데이터의 종류, 날짜, 시고저종, 거래량, 거래대금 , 상장주식수
                instStockChart.SetInputValue(6, ord('D'))  # 차트의 종류, D : 일단위 데이터
                instStockChart.SetInputValue(9, ord('1'))  # 수정 주가의 반영 여부, 1 : 반영
                time.sleep(0.255)
                instStockChart.BlockRequest()
                numData = instStockChart.GetHeaderValue(3) # 받아온 데이터 개수
                Kospi_Data = []

                for j in range(numData):
                    Date=datetime.strptime(str(instStockChart.GetDataValue(0, j)), "%Y%m%d")
                    Open=instStockChart.GetDataValue(1, j)
                    High=instStockChart.GetDataValue(2, j)
                    Low=instStockChart.GetDataValue(3, j)
                    Close=instStockChart.GetDataValue(4, j)
                    Volume=instStockChart.GetDataValue(5, j)
                    Transaction=instStockChart.GetDataValue(6, j)
                    ShareNum=instStockChart.GetDataValue(7, j)
                    row = (Date, Open, High, Low, Close, Volume, Transaction, ShareNum, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None)
                    try :
                        if Kospi_Data[0][0] == row[0] :
                            continue
                        else : Kospi_Data.append(row)
                    except :
                        Kospi_Data.append(row)
                        continue

                Kospi_Data.reverse()
                cur.executemany("insert into %s values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)" %code, Kospi_Data)
                con.commit()

        except:
            print(code + "오류")
            error_codelist.append(code)
            continue
    con.close()
    return error_codelist

def Get_KOSPI_Data_noadj(*code_list,SDate,EDate,DBname):
    """
    :param code_list: Kospi_codelist
    :param SDate: Start Date ex) 20190101
    :param EDate: End Date ex) 20200101
    :param DBname: DB name
    :return: 코스피 주가관련 데이터 반환
    """
    instStockChart = win32com.client.Dispatch("CpSysDib.StockChart")
    con = sqlite3.connect("C:/Users/S/desktop/바탕화면(임시)/KOSPI/tmp/" + DBname + ".db")  # sqlite 연결 db 객체 생성
    i = 1
    try :
        for code in code_list:
            code = "A" + code
            print(i, "/", len(code_list))
            instStockChart.SetInputValue(0, code)  # 종목코드
            instStockChart.SetInputValue(1, ord('1'))  # 기간 요청
            instStockChart.SetInputValue(2, EDate)  # 요청 종료 날짜 지정
            instStockChart.SetInputValue(3, SDate)  # 요청 시작 날짜 지정
            instStockChart.SetInputValue(5, (0, 2, 3, 4, 5, 8, 9, 12, 14, 15, 16, 17, 20, 21))  # 데이터의 종류
            instStockChart.SetInputValue(6, ord('D'))  # 차트의 종류, D : 일단위 데이터
            instStockChart.SetInputValue(9, ord('0'))  # 수정 주가의 반영 여부
            time.sleep(0.255)
            instStockChart.BlockRequest()
            numData = instStockChart.GetHeaderValue(3)

            Date = []
            Open_noadj = []
            High_noadj = []
            Low_noadj = []
            Close_noadj = []
            Volume_noadj = []
            Transaction_noadj = []  # 거래대금
            ShareNum_noadj = []  # 상장주식수
            Foreign_1 = []  # 외국인주문한도수량
            Foreign_2 = []  # 외국인주문가능수량
            Foreign_3 = []  # 외국인현보유수량
            Foreign_4 = []  # 외국인현보유비율
            Company_1 = []  # 기관순매수
            Company_2 = []  # 기관누적순매수

            for j in range(numData):
                Date.append(str(instStockChart.GetDataValue(0, j)))
                Open_noadj.append(instStockChart.GetDataValue(1, j))
                High_noadj.append(instStockChart.GetDataValue(2, j))
                Low_noadj.append(instStockChart.GetDataValue(3, j))
                Close_noadj.append(instStockChart.GetDataValue(4, j))
                Volume_noadj.append(instStockChart.GetDataValue(5, j))
                Transaction_noadj.append(instStockChart.GetDataValue(6, j))
                ShareNum_noadj.append(instStockChart.GetDataValue(7, j))
                Foreign_1.append(instStockChart.GetDataValue(8, j))
                Foreign_2.append(instStockChart.GetDataValue(9, j))
                Foreign_3.append(instStockChart.GetDataValue(10, j))
                Foreign_4.append(instStockChart.GetDataValue(11, j))
                Company_1.append(instStockChart.GetDataValue(12, j))
                Company_2.append(instStockChart.GetDataValue(13, j))

            Kospi_Data = pd.DataFrame({"Date": Date,
                                       "Open_noadj": Open_noadj,
                                       "High_noadj": High_noadj,
                                       "Low_noadj": Low_noadj,
                                       "Close_noadj": Close_noadj,
                                       "Volume_noadj": Volume_noadj,
                                       "Transaction_noadj": Transaction_noadj,
                                       "ShareNum_noadj": ShareNum_noadj,
                                       "Foreign_1": Foreign_1,
                                       "Foreign_2": Foreign_2,
                                       "Foreign_3": Foreign_3,
                                       "Foreign_4": Foreign_4,
                                       "Company_1": Company_1,
                                       "Company_2": Company_2
                                       })
            Kospi_Data = Kospi_Data.sort_values(by="Date")
            # SQLite DB로 저장
            try:
                Kospi_Data.to_sql(code, con, index=False)
            except:
                print(code, "오류")
                pass

            i += 1

    except :
        print("오류")
        pass

    con.close()
    return "정상적으로 완료했습니다."

def KOSPI_Index_Data(SDate,EDate):
    """
    KOSPI 지수 데이터를 얻기 위함
    """
    if Get_login_status() : # CP로그인 상태 확인
        pass
    else :
        exit()
    Cybosobj = win32com.client.Dispatch("CpSysDib.StockChart")
    Cybosobj.SetInputValue(0, "U001")  # 종목코드
    Cybosobj.SetInputValue(1, ord('1'))  # 기간 요청
    Cybosobj.SetInputValue(2, EDate)  # 요청 종료 날짜 지정
    Cybosobj.SetInputValue(3, SDate)  # 요청 시작 날짜 지정
    Cybosobj.SetInputValue(5, (0, 2, 3, 4, 5, 8, 9))  # 데이터의 종류
    Cybosobj.SetInputValue(6, ord('D'))  # 차트의 종류, D : 일단위 데이터
    Cybosobj.SetInputValue(9, ord('1'))  # 수정 주가의 반영 여부, 0:무수정 주가 1 : 반영
    Cybosobj.BlockRequest()
    numData = Cybosobj.GetHeaderValue(3)

    Date = []
    Open = []
    High = []
    Low = []
    Close = []
    Volume = []
    Transaction = []  # 거래대금

    for j in range(numData):
        Date.append(str(Cybosobj.GetDataValue(0, j)))
        Open.append(Cybosobj.GetDataValue(1, j))
        High.append(Cybosobj.GetDataValue(2, j))
        Low.append(Cybosobj.GetDataValue(3, j))
        Close.append(Cybosobj.GetDataValue(4, j))
        Volume.append(Cybosobj.GetDataValue(5, j))
        Transaction.append(Cybosobj.GetDataValue(6, j))

    Kospi_Data = pd.DataFrame({"Date": Date,
                               "Open": Open,
                               "High": High,
                               "Low": Low,
                               "Close": Close,
                               "Volume": Volume,
                               "Transaction": Transaction,
                               })
    df_Kospi_Data = Kospi_Data.sort_values(by="Date")
    return df_Kospi_Data


# ETF 분석 관련 함수
def Get_ETF_code_name():
    """
    ETF 코드명과 종목명 추출
    ETF_code_list와 ETF_name_list 반환
    """
    try:
        objCpCodeMgr = win32com.client.Dispatch("CpUtil.CpCodeMgr")
        code_list = objCpCodeMgr.GetStockListByMarket(1)  # 0 : 구분없음, 1 : 거래소, 2: 코스닥
        ETF_code_list = []
        ETF_name_list = []
        for code in code_list:
            if objCpCodeMgr.GetStockSectionKind(code) == 10:  # 0: 구분없음, 1: 주권, 10: ETF
                ETF_code_list.append(code)
                ETF_name_list.append(objCpCodeMgr.CodeToName(code))

        return ETF_code_list, ETF_name_list

    except:
        print("오류")
        pass

def ETF_RequestData(Cybos_obj, ETFcode):
    """
    ETF 분석에 필요한 일자별 데이터 요청 실행
    """
    # 데이터 요청
    Cybos_obj.SetInputValue(0, ETFcode)
    Cybos_obj.BlockRequest()

    # 통신 결과 확인
    rqStatus = Cybos_obj.GetDibStatus() # DB통신상태 (-1 : 오류, 0 : 정상, 1 : 수신대기)
    rqMsg = Cybos_obj.GetDibMsg1() # DB통신상태 문자열
    if rqStatus != 0:
        print("통신상태", rqStatus, rqMsg)
        return False

def ETF_GetData(Cybos_obj, ETFcode):
    """
    ETF 분석에 필요한 일자별 데이터 얻기
    :return: Dataframe타입 ETF 데이터
    """
    etfDate = []
    etfNAV = []
    etfClose = []

    # 최초 데이터 요청
    ETF_RequestData(Cybos_obj, ETFcode)
    count = Cybos_obj.GetHeaderValue(0)  # 수신 데이터 수

    def Data_Save(startnum,endnum):
        """
        최초 데이터 요청과 연속데이터 요청을 분리실행으로 중복되는 코드
        요청한 ETF 데이터를 변수에 저장해주는 기능
        최초 데이터 요청에서 가장 최근 데이터를 빼는 문제 때문에, startnum, endnum구분했음
        """
        for i in range(startnum, endnum):
            # 필요한 데이터가 다르면 수정해야하는 부분
            date = Cybos_obj.GetDataValue(0, i)  # 날짜
            close = Cybos_obj.GetDataValue(1, i)  # ETF종가
            NAV = Cybos_obj.GetDataValue(6, i)  # NAV

            etfDate.append(date)
            etfClose.append(close)
            etfNAV.append(NAV)
    Data_Save(0, count)

    # 연속 데이터 요청
    NextCount = 1
    while Cybos_obj.Continue:  # 연속데이터 유무(1: 연속, 0: 연속없음)
        time.sleep(0.251) # 최대 1초에 최대 4개 조회 가능
        ETF_RequestData(Cybos_obj, ETFcode)
        count = Cybos_obj.GetHeaderValue(0)  # 수신 데이터 수
        Data_Save(1, count)
        print(NextCount); NextCount += 1
        if (NextCount > 500): # 임의값 500 수정가능
            break

    ETF_df = pd.DataFrame({"Date": etfDate,
                           "Close": etfClose,
                           "NAV": etfNAV})
    ETF_df = ETF_df.sort_values("Date")
    return ETF_df

