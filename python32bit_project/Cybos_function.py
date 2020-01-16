import win32com.client
import os
import sqlite3
from datetime import datetime, timedelta
import time
import pandas as pd

KOSPI_codelist = []
KOSPI_namelist = []
error_codelist = []
def Get_login_status() :
    """
    연결상태 확인 
    1: 연결, 0: 비연결
    """
    instCpCybos = win32com.client.Dispatch("CpUtil.CpCybos")
    if instCpCybos.IsConnect != 1:
        print("CybosPlus가 연결되어있지 않습니다.")
        os.startfile("C:\\Users\\S\\Desktop\\CybosPlus.lnk")
        pass
    else:
        return "정상적으로 연결되었습니다."



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



def Get_KOSPI_Data(*code_list,SDate,EDate,DBname):
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
            instStockChart.SetInputValue(5, (0, 2, 3, 4, 5, 8, 9, 12))  # 데이터의 종류, 날짜, 시고저종, 거래량, 거래대금 , 상장주식수
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
            Transaction = []  # 거래대금
            ShareNum = []  # 상장주식수

            for j in range(numData):
                Date.append(str(instStockChart.GetDataValue(0, j)))
                Open.append(instStockChart.GetDataValue(1, j))
                High.append(instStockChart.GetDataValue(2, j))
                Low.append(instStockChart.GetDataValue(3, j))
                Close.append(instStockChart.GetDataValue(4, j))
                Volume.append(instStockChart.GetDataValue(5, j))
                Transaction.append(instStockChart.GetDataValue(6, j))
                ShareNum.append(instStockChart.GetDataValue(7, j))

            Kospi_Data = pd.DataFrame({"Date": Date,
                                       "Open": Open,
                                       "High": High,
                                       "Low": Low,
                                       "Close": Close,
                                       "Volume": Volume,
                                       "Transaction": Transaction,
                                       "ShareNum": ShareNum
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




if __name__ == "__main__" :
    Get_login_status()
    Get_KOSPI_code()
    print(__name__)

