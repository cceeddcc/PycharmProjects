import win32com.client
import os
import sqlite3
from datetime import datetime, timedelta

KOSPI_codelist = []
KOSPI_namelist = []

def Get_login_status() :
    """
    연결상태 확인 
    1: 연결, 0: 비연결
    """
    instCpCybos = win32com.client.Dispatch("CpUtil.CpCybos")
    if instCpCybos.IsConnect != 1:
        print("CybosPlus가 연결되어있지 않습니다.")
        os.startfile("C:\\Users\\S\\Desktop\\CybosPlus.lnk")
        return exit()
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
        return "정상적으로 처리되었습니다."

    except : return "오류"


#     
# timedelta(days = -1)
# datetime.today() + timedelta(days = -1)
# datetime.today()
# datetime.now().strftime("%Y-%m-%d")
def Update_KOSPI_Data():
    """
    :return: KOSPI DB 업데이트
    """
    KOSPI_namelist
    KOSPI_codelist
    instStockChart = win32com.client.Dispatch("CpSysDib.StockChart")
    con = sqlite3.connect("C:/Users/S/desktop/바탕화면(임시)/KOSPI/KOSPI_Price_Data.db")
    cursor = con.cursor()
    today = datetime.now().strftime("%Y%m%d")

    i = 0
    code = KOSPI_codelist[0] # 임시
    for code in KOSPI_codelist:
        print((i+1), "/", len(KOSPI_codelist))
        instStockChart.SetInputValue(0, code)  # 종목코드
        instStockChart.SetInputValue(1, ord('1'))  # 기간 요청
        instStockChart.SetInputValue(2, 20200115)  # 요청 종료 날짜 지정
        instStockChart.SetInputValue(3, 20200110)  # 요청 시작 날짜 지정
        instStockChart.SetInputValue(5, (0, 2, 3, 4, 5, 8, 9, 12))  # 데이터의 종류, 날짜, 시고저종, 거래량, 거래대금 , 상장주식수
        instStockChart.SetInputValue(6, ord('D'))  # 차트의 종류, D : 일단위 데이터
        instStockChart.SetInputValue(9, ord('1'))  # 수정 주가의 반영 여부, 1 : 반영
        time.sleep(0.255)
        instStockChart.BlockRequest()

        Date = instStockChart.GetDataValue(0, 0)
        Open = instStockChart.GetDataValue(1, 0)
        High = instStockChart.GetDataValue(2, 0)
        Low = instStockChart.GetDataValue(3, 0)
        Close = instStockChart.GetDataValue(4, 0)
        Volume = instStockChart.GetDataValue(5, 0)
        Transaction = instStockChart.GetDataValue(6, 0)  # 거래대금
        ShareNum = instStockChart.GetDataValue(7, 0)  # 상장주식수

        Data = pd.DataFrame({"Date": Date,
                                   "Open": Open,
                                   "High": High,
                                   "Low": Low,
                                   "Close": Close,
                                   "Volume": Volume,
                                   "Transaction": Transaction,
                                   "ShareNum": ShareNum
                                   })
        # SQLite DB로 저장
        try:
            cursor.execute("INSERT INTO {} VALUES('16.06.03', 97000, 98600, 96900, 98000, 321405)").format(code)

        except:
            pass

        i += 1


if __name__ == "__main__" :
    Get_login_status()
    Get_KOSPI_code()
    print(__name__)

del os
