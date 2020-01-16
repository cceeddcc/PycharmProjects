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
Cybos_function.Get_KOSPI_Data(*Kospi_codelist,SDate=20091127,EDate=20200115,DBname="KOSPI_Price_DB1")
# Cybos_function.Get_KOSPI_Data(*Kospi_codelist,SDate=20050101,EDate=20091126,DBname="KOSPI_Price_DB2")
# Cybos_function.Get_KOSPI_Data(*Kospi_codelist,SDate=20000101,EDate=20041231,DBname="KOSPI_Price_DB3")
# Cybos_function.Get_KOSPI_Data(*Kospi_codelist,SDate=19950101,EDate=19991231,DBname="KOSPI_Price_DB4")
# Cybos_function.Get_KOSPI_Data(*Kospi_codelist,SDate=19900101,EDate=19941231,DBname="KOSPI_Price_DB5")
# Cybos_function.Get_KOSPI_Data(*Kospi_codelist,SDate=19850101,EDate=19891231,DBname="KOSPI_Price_DB6")
# Cybos_function.Get_KOSPI_Data(*Kospi_codelist,SDate=19800101,EDate=19841231,DBname="KOSPI_Price_DB7")
# Cybos_function.Get_KOSPI_Data(*Kospi_codelist,SDate=19750101,EDate=19791231,DBname="KOSPI_Price_DB8")
# Cybos_function.Get_KOSPI_Data(*Kospi_codelist,SDate=19700101,EDate=19741231,DBname="KOSPI_Price_DB9")
# Cybos_function.Get_KOSPI_Data(*Kospi_codelist,SDate=19650101,EDate=19691231,DBname="KOSPI_Price_DB10")
# Cybos_function.Get_KOSPI_Data(*Kospi_codelist,SDate=19600101,EDate=19641231,DBname="KOSPI_Price_DB11")

# 코스피 데이터 업데이트
error_codelist = Cybos_function.Update_KOSPI_Data(*Kospi_codelist,DBname="KOSPI_PriceFinance_DB")
