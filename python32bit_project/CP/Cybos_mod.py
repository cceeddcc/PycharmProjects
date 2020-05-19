"""
Cybos module
"""

import win32com.client
import pandas as pd
import os

__doc__ = """
RQ(request) 제한
시세오브젝트 : 15초에최대 60건으로제한, 
초과요청시 첫 요청으로부터 15초가 지날 때 까지 내부적으로 기다림

주문관련오브젝트 : 15초에최대 20건으로제한,
초과요청시 첫 요청으로부터 15초가 지날 때 까지 
요청함수(Request, BlockRequest, BlockRequest2)에서 4를반환

SB(subscibe) 제한
시세오브젝트 : 최대 400건의요청으로제한, 초과요청시오류
주문관련오브젝트 : 제한없음

위의제한사항은당사방침에따라변경될수있습니다.
"""

class CP_Util :

    def __init__(self):
        self.CpCybos = win32com.client.Dispatch("CpUtil.CpCybos")
        self.CP_login_status()

    def CP_login_status(self):
        """
        check CP login status
        """

        if self.CpCybos.IsConnect == 1: # 1: connected , 0: disconnected
            print("CP is connected")
            return True
        else:
            print("CP is disconnected")
            return False

    @staticmethod
    def login_CP():
        os.startfile("C:\\Users\\S\\Desktop\\CybosPlus.lnk")
        print("CybosPlus.exe을 실행합니다.")


    @staticmethod
    def Get_index_code(name="kospi"):

        if name == "kospi":
            code = "U001"
        elif name == "kosdaq":
            code = "U201"
        else :
            code = None

        return code

    @staticmethod
    def string_to_section(string):
        """
        convert section kind("string") to section kind id number
        """
        if string == "주권":
            section = 1
        elif string == "투자회사":
            section = 2
        elif string == "부동산투자회사":
            section = 3
        elif string == "선박투자회사":
            section = 4
        elif string == "사회간접자본투융자회사":
            section = 5
        elif string == "ETF":
            section = 10
        elif string == "외국주권":
            section = 13
        elif string == "ETN":
            section = 17
        elif string == "모두":
            section = 0
        else:
            section = -1
        return section

class CP_KOSPI(CP_Util) :

    def __init__(self):
        super().__init__()
        self.CpCodeMgr = win32com.client.Dispatch("CpUtil.CpCodeMgr")
        self.instStockChart = win32com.client.Dispatch("CpSysDib.StockChart")

    def Get_code_by_seckind(self, kind="모두"):
        """
        return KOSPI codelist classified by section kind
        kind : "모두" "주권" "투자회사" "부동산투자회사" "선박투자회사" "사회간접자본투융자회사" "ETF" 외국주권" ETN"
        """
        KOSPI_codelist = self.CpCodeMgr.GetStockListByMarket(1)  # KOSPI
        codelist = []

        # 부구분 section kind
        section_kind = [self.CpCodeMgr.GetStockSectionKind(KOSPI_codelist[i]) for i in range(KOSPI_codelist.__len__())]
        section = CP_KOSPI.string_to_section(kind)

        # 개선필요
        if section == 0 :
            return KOSPI_codelist
        elif section == -1 :
            print("error in kind")
            return None
        else :
            for i, value in enumerate(section_kind):
                if value == section:
                    codelist.append(KOSPI_codelist[i])

        return codelist

    def Get_name_by_seckind(self, kind="모두"):
        """
        return KOSPI name list classified by section kind
        """
        codelist = self.Get_code_by_seckind(kind=kind)
        namelist = [self.CpCodeMgr.CodeToName(codelist[i]) for i in range(codelist.__len__())]
        return namelist

    def Get_Data(self, code=str, Sdate=int, Edate=int):
        """
        Get periodic dataframe from Sdate to Edate
        """

        # Set input data
        self.instStockChart.SetInputValue(0, code)  # 종목코드
        self.instStockChart.SetInputValue(1, ord('1'))  # 기간 요청
        self.instStockChart.SetInputValue(2, Edate)  # 요청 종료 날짜
        self.instStockChart.SetInputValue(3, Sdate)  # 요청 시작 날짜
        # 날짜, 시가, 고가, 저가, 종가, 거래량, 시총
        self.instStockChart.SetInputValue(5, (0, 2, 3, 4, 5, 8, 9, 13))
        self.instStockChart.SetInputValue(6, ord('D'))  # D : 일단위 데이터
        self.instStockChart.SetInputValue(9, ord('1'))  # 수정주가
        self.instStockChart.BlockRequest()
        numdata = self.instStockChart.GetHeaderValue(3)  # 데이터 개수

        # get output data
        columns = ["Date", "Open", "High", "Low", "Close", "Volume", "Mcap"]
        df = pd.DataFrame()
        for j, col in enumerate(columns):
            df[col] = [self.instStockChart.GetDataValue(j, i) for i in range(numdata)]

        df["Date"] = [str(df["Date"].iloc[i]) for i in range(len(df["Date"].index))]
        df["Date"] = pd.to_datetime(df["Date"])

        return df


if __name__ == '__main__' :

    kospi1 = CP_KOSPI()
    # codelst = kospi1.Get_code_by_seckind()
    # namelst  = kospi1.Get_name_by_seckind()
    # code = codelst[1] # tmp
    # SDate = 20190101 # tmp
    # EDate = 20191201 # tmp

    # df = kospi1.Get_Data(code=code, Sdate=SDate, Edate=EDate)
    # df_kospi = kospi1.Get_Data(code=kospi1.Get_index_code(), Sdate=SDate, Edate=EDate)
    print("완료")



# 추가해야하는 기능
#
# # code 에해당하는증권전산업종코드를반환한다.
# Industry_code = [CpCodeMgr.GetStockIndustryCode(codelist[i]) for i in range(codelist.__len__())]
#
# value2 = CpCodeMgr.GetGroupCodeList("024") # 증권업
# for value in value2:
#     print(CpCodeMgr.CodeToName(value))
#
# value = CpCodeMgr.GetGroupName("024")
# """
# 관심종목(700 ~799 ) 및업종코드에해당하는명칭을반환한다
#
# 반환값 : 관심종목명및업종코드명
# """
# aa = collections.Counter(Industry_code)
# for value in aa.keys():
#     print(CpCodeMgr.GetGroupName(value))
#
#
# # code 에해당하는소속부를반환한다.
# # 코스피라 다 1 나오는듯
# aa = [CpCodeMgr.GetStockMarketKind(codelist[i]) for i in range(codelist.__len__())]
# """
# [("구분없음")]CPC_MARKET_NULL= 0,
# [("거래소")]   CPC_MARKET_KOSPI= 1,
# [("코스닥")]   CPC_MARKET_KOSDAQ= 2,
# [("K-OTC")] CPC_MARKET_FREEBOARD= 3,
# [("KRX")]       CPC_MARKET_KRX= 4,
# [("KONEX")] CPC_MARKET_KONEX= 5,
# """
#
# CAPITAL_SIZE = [CpCodeMgr.GetStockCapital(codelist[i]) for i in range(codelist.__len__())]
# """
# code 에해당하는자본금규모구분반환한다.
# typedefenum {
# [helpstring("제외")]   CPC_CAPITAL_NULL  = 0,
# [helpstring("대")]   CPC_CAPITAL_LARGE  = 1,
# [helpstring("중")]   CPC_CAPITAL_MIDDLE  = 2,
# [helpstring("소")]   CPC_CAPITAL_SMALL  = 3
# }CPE_CAPITAL_SIZE;
# """
#
# Groupcode = [CpCodeMgr.GetStockGroupCode(codelist[i]) for i in range(codelist.__len__())]
#
# for i, value in enumerate(Groupcode):
#     if value == 907 :
#         print(KOSPI_namelist[i])
# """
# code 에해당하는그룹(계열사)코드반환한다.
# 반환값 : 그룹(계열사)코드
# """






















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