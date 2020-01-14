# def get_code():  # 종목 코드 가져오기
#     import win32com.client
#     import sys
#
#     # 연결상태 확인 1: 연결, 0: 비연결
#     instCpCybos = win32com.client.Dispatch("CpUtil.CpCybos")
#     if instCpCybos.IsConnect != 1:
#         print("CybosPlus가 연결되어있지 않습니다.")
#         return exit()
#
#
#     objCpCodeMgr = win32com.client.Dispatch("CpUtil.CpCodeMgr")
#     codeList = objCpCodeMgr.GetStockListByMarket(1)  # 거래소
#     Kospi_codelist = []
#
#     # 코스피 보통주
#     for i, code in enumerate(codeList):
#         if code[-1] == "0" and objCpCodeMgr.GetStockSectionKind(code) == 1:  # 주권, 보통주에 해당하는 것만 추출
#             Kospi_codelist.append(code[1:])
#
#     # 코드 저장
#     for code in Kospi_codelist:
#         f = open('c:\\Users\\S\\Desktop\\code_list.txt', 'a')
#         f.write(code + '\n')
#         f.close()
#     return "성공적으로 저장했습니다."


def get_login_status() :
    import win32com.client
    # 연결상태 확인 1: 연결, 0: 비연결
    instCpCybos = win32com.client.Dispatch("CpUtil.CpCybos")
    if instCpCybos.IsConnect != 1:
        print("CybosPlus가 연결되어있지 않습니다.")
        return exit()
    else:
        print("정상적으로 연결되었습니다.")


if __name__ == "__main__" :
    get_login_status()
    print(__name__)
