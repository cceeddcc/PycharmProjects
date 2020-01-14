# def get_stockprice() : # 수정주가 가져오기
import win32com.client

# 종목명, 코드 불러오기
f = open('c:\\Users\\S\\Desktop\\code_list2.txt', 'r')
lines = f.readlines()
code_list = []
for line in lines:
        nline = line.split('\n')[0]
        code_list.append(nline)
f.close()


# 연결상태 확인 1: 연결, 0: 비연결
instCpCybos = win32com.client.Dispatch("CpUtil.CpCybos")
if instCpCybos.IsConnect != 1:
    print("CybosPlus가 연결되어있지 않습니다.")
    exit()
else :
    print("정상적으로 연결되었습니다.")

# 종목코드 리스트 구하기
objCpCodeMgr = win32com.client.Dispatch("CpUtil.CpCodeMgr")
codeList = objCpCodeMgr.GetStockListByMarket(1) # 거래소
Kospi_namelist = []
Kospi_codelist = []
for code in code_list:
    Kospi_namelist.append(objCpCodeMgr.CodeToName(code))
    Kospi_codelist.append(code)

# 코드 저장
for code in Kospi_codelist:
    f = open('c:\\Users\\S\\Desktop\\code_list3.txt', 'a')
    f.write(code + '\n')
    f.close()
# 종목명 저장
for name in Kospi_namelist:
    f = open('c:\\Users\\S\\Desktop\\name_list3.txt', 'a')
    f.write(name + '\n')
    f.close()
