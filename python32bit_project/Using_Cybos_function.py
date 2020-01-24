import Cybos_function

# 로그인 확인
Cybos_function.Get_login_status()

# 코스피 코드 및 종목명 리스트 가져오기
Kospi_codelist, Kospi_namelist= Cybos_function.Get_KOSPI_code()

# 코스피 코드 및 종목명 txt파일로 저장
with open("C:\\Users\\S\\Desktop\\바탕화면(임시)\\KOSPI\\KOSPI_codelist.txt", "w") as f :
    for code in Kospi_codelist :
        f.write("A" + code + "\n")
with open("C:\\Users\\S\\Desktop\\바탕화면(임시)\\KOSPI\\KOSPI_namelist.txt", "w") as f :
    for name in Kospi_namelist :
        f.write(name + "\n")


# 코스피 가격, 거래량 등 데이터 저장
# 한번에 가져올 수 있는 데이터 개수는 2500개 -> 여러번 해서 묵어야함
# Cybos_function.Get_KOSPI_Data_adj(*Kospi_codelist,SDate=20160101,EDate=20200131,DBname="KOSPI_Price_DB1")
# Cybos_function.Get_KOSPI_Data_adj(*Kospi_codelist,SDate=20110101,EDate=20151231,DBname="KOSPI_Price_DB2")
# Cybos_function.Get_KOSPI_Data_adj(*Kospi_codelist,SDate=20060101,EDate=20101231,DBname="KOSPI_Price_DB3")
# Cybos_function.Get_KOSPI_Data_adj(*Kospi_codelist,SDate=20010101,EDate=20051231,DBname="KOSPI_Price_DB4")
# Cybos_function.Get_KOSPI_Data_adj(*Kospi_codelist,SDate=19960101,EDate=20001231,DBname="KOSPI_Price_DB5")
# Cybos_function.Get_KOSPI_Data_adj(*Kospi_codelist,SDate=19910101,EDate=19951231,DBname="KOSPI_Price_DB6") s
# Cybos_function.Get_KOSPI_Data_adj(*Kospi_codelist,SDate=19860101,EDate=19901231,DBname="KOSPI_Price_DB7") s
# Cybos_function.Get_KOSPI_Data_adj(*Kospi_codelist,SDate=19810101,EDate=19851231,DBname="KOSPI_Price_DB8") s
# Cybos_function.Get_KOSPI_Data_adj(*Kospi_codelist,SDate=19800101,EDate=19801231,DBname="KOSPI_Price_DB9")
Cybos_function.Get_KOSPI_Data_adj(*Kospi_codelist,SDate=19910101,EDate=19910226,DBname="KOSPI_Price_DB10")
Cybos_function.Get_KOSPI_Data_adj(*Kospi_codelist,SDate=19860101,EDate=19860207,DBname="KOSPI_Price_DB11")
Cybos_function.Get_KOSPI_Data_adj(*Kospi_codelist,SDate=19810101,EDate=19810223,DBname="KOSPI_Price_DB12")


# 수정전 종가 및 상장주식수 가져오기
# Cybos_function.Get_KOSPI_Data_noadj(*Kospi_codelist,SDate=20160101,EDate=20200131,DBname="KOSPI_Price_DB11")
# Cybos_function.Get_KOSPI_Data_noadj(*Kospi_codelist,SDate=20110101,EDate=20151231,DBname="KOSPI_Price_DB22")
# Cybos_function.Get_KOSPI_Data_noadj(*Kospi_codelist,SDate=20060101,EDate=20101231,DBname="KOSPI_Price_DB33")
# Cybos_function.Get_KOSPI_Data_noadj(*Kospi_codelist,SDate=20010101,EDate=20051231,DBname="KOSPI_Price_DB44")
# Cybos_function.Get_KOSPI_Data_noadj(*Kospi_codelist,SDate=19960101,EDate=20001231,DBname="KOSPI_Price_DB55")
# Cybos_function.Get_KOSPI_Data_noadj(*Kospi_codelist,SDate=19910101,EDate=19951231,DBname="KOSPI_Price_DB66")
# Cybos_function.Get_KOSPI_Data_noadj(*Kospi_codelist,SDate=19860101,EDate=19901231,DBname="KOSPI_Price_DB77")
# Cybos_function.Get_KOSPI_Data_noadj(*Kospi_codelist,SDate=19810101,EDate=19851231,DBname="KOSPI_Price_DB88")
# Cybos_function.Get_KOSPI_Data_noadj(*Kospi_codelist,SDate=19800101,EDate=19801231,DBname="KOSPI_Price_DB99")
Cybos_function.Get_KOSPI_Data_noadj(*Kospi_codelist,SDate=19910101,EDate=19910226,DBname="KOSPI_Price_DB1010")
Cybos_function.Get_KOSPI_Data_noadj(*Kospi_codelist,SDate=19860101,EDate=19860207,DBname="KOSPI_Price_DB1111")
Cybos_function.Get_KOSPI_Data_noadj(*Kospi_codelist,SDate=19810101,EDate=19810223,DBname="KOSPI_Price_DB1212")


# 코스피 데이터 업데이트
# "C:/Users/S/desktop/바탕화면(임시)/KOSPI/tmp/DB파일"에 저장됨
error_codelist = Cybos_function.Update_KOSPI_Data(*Kospi_codelist,DBname="KOSPI_PriceFinance_DB")

# 코스피 상장 주식 업데이트
# "C:/Users/S/desktop/바탕화면(임시)/KOSPI/tmp/DB파일"에 저장됨
Cybos_function.Get_KOSPI_Data("344820",SDate=20091127,EDate=20200122,DBname="KOSPI_Price_DB1")
