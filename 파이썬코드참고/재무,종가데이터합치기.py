"""
재무데이터와 종가데이터 합치는 작업
"""
import pandas as pd
import re
import sqlite3
con = sqlite3.connect("C:/Users/S/desktop/바탕화면(임시)/KOSPI/KOSPI최종.db")  # sqlite 연결 db 객체 생성
con2 = sqlite3.connect("C:/Users/S/desktop/바탕화면(임시)/KOSPI/KOSPI재무종가합2.db")

# 종목명, 코드 불러오기
with open("c:/Users/S/Desktop/code_list.txt", "r") as f :
    code_list = [line.split("\n")[0] for line in f.readlines()]

with open("c:/Users/S/Desktop/name_list.txt", "r") as f :
    name_list = [line.split("\n")[0] for line in f.readlines()]

error_code = []

j = 0
for j in range(len(code_list)) :
    try:
        print(j+1 ,"/", len(code_list))
        df_1= pd.read_csv("C:\\Users\\S\\Desktop\\바탕화면(임시)\\KOSPI재무\\"+ code_list[j] + ".csv", encoding="euc-kr")
        df_2= pd.read_csv("C:\\Users\\S\\Desktop\\바탕화면(임시)\\KOSPI재무2\\"+ code_list[j] + ".csv", encoding="euc-kr")
        df_merge = pd.merge(df_1,df_2)
        columns = ["Date","Price","Asset","Capital","Sales","Operating","Profit","Retention","CFO","CFI","CFF",
                   "Op_Margin","Liability","Sa_Margin","non-operating","COGS","SGA","EBIT","NetCF",
                   'BPS', 'CFPS', 'PSR', 'PER', 'SPS', 'div_rate', 'PBR', 'EBITDA','EPS', "EV/EB",
                   'PayoutRatio', 'Return', 'DPS', 'PCR']
        df_merge.columns = columns

        # 결산년도 날짜데이터로 변환시키기
        r = re.compile("[0-9]+")
        Dates = [r.findall(Date) for Date in df_merge["Date"]]
        Dates2 = []

        i=0
        for i in range(len(Dates)) :
            year = "20"+Dates[i][0]
            Date_test = int(Dates[i][1]) + 2

            if Date_test > 12:
                year = str(int(year) + 1)
                year = year + "0" + str(Date_test - 11) + "28"

            else:
                if Date_test > 9:
                    year = year + str(Date_test) + "16"
                else:
                    year = year + "0" + str(Date_test) + "16"

            Dates2.append(year)

        df_merge["Date"] = Dates2
        df_merge["Date"] = pd.to_datetime(df_merge["Date"].astype(str))

        # 재무데이터 변환 결과물
        # df_merge

        # db에서 수정종가 데이터 가져오기
        df = pd.read_sql("SELECT * FROM %s" %name_list[j], con, index_col=None) # SQLite DB 읽기

        # Date열 날짜형으로 변환
        df["Date"] = pd.to_datetime(df["Date"].astype(str))


        # 수정종가 데이터 변환 결과물
        # df

        # 날짜 다시한번 맞춰주기
        """
        수정종가 데이터가 2009년 11월 부터 밖에 없음 
        """
        df_merge = df_merge[df_merge["Date"] > min(df["Date"])]
        """
        재무데이터 날짜가 휴장일일 수 있기 때문에 가장 가까운 날짜로 변환
        """
        Date = [] # 변수 초기화
        Dates2 = [] # 변수 초기화
        for Date in df_merge["Date"]:
            if not Date in list(df["Date"]) :
                Dates2.append(min(df["Date"][df["Date"] > Date]))
            else :
                Dates2.append(Date)

        df_merge["Date"] = pd.Series(Dates2)

        # 재무데이터, 수정종가데이터 합치기
        df_fin = pd.merge(df,df_merge, how = "outer", on= "Date")
        try :
            df_fin.to_sql(name_list[j] + "," + code_list[j],con2, index=False)
        except : pass

    except :
        print(name_list[j] + "," + code_list[j] + " 오류")
        error_code.append(name_list[j] + "," + code_list[j])
        continue

con.close()
con2.close()


error_code
# error_code 저장
with open("c:/Users/S/Desktop/error_code.txt", "w") as f :
    [f.write(lines +"\n") for lines in error_code]


## 에러난 것만 다시

import pandas as pd
import re
import sqlite3
con = sqlite3.connect("C:/Users/S/desktop/바탕화면(임시)/KOSPI/KOSPI최종.db")  # sqlite 연결 db 객체 생성
con2 = sqlite3.connect("C:/Users/S/desktop/바탕화면(임시)/KOSPI/KOSPI재무종가합2.db")

# 종목명, 코드 불러오기
code_list2 = [ code.split(",")[1] for code in error_code]
name_list2 = [ code.split(",")[0] for code in error_code]

error_code2 = []
j = 0
for j in range(len(code_list2)) :
    try:
        print(j+1 ,"/", len(code_list2))
        df_1= pd.read_csv("C:\\Users\\S\\Desktop\\바탕화면(임시)\\KOSPI재무\\"+ code_list2[j] + ".csv", encoding="euc-kr")
        df_2= pd.read_csv("C:\\Users\\S\\Desktop\\바탕화면(임시)\\KOSPI재무2\\"+ code_list2[j] + ".csv", encoding="euc-kr")
        df_merge = pd.merge(df_1,df_2)
        columns = ["Date","Price","Asset","Capital","Sales","Operating","Profit","Retention","CFO","CFI","CFF",
                   "Op_Margin","Liability","Sa_Margin","non-operating","COGS","SGA","EBIT","NetCF",
                   'BPS', 'CFPS', 'PSR', 'PER', 'SPS', 'div_rate', 'PBR', 'EBITDA','EPS', "EV/EB",
                   'PayoutRatio', 'Return', 'DPS', 'PCR']
        df_merge.columns = columns

        # 결산년도 날짜데이터로 변환시키기
        r = re.compile("[0-9]+")
        df_merge = df_merge[~pd.isna(df_merge["Date"])]
        Dates = [r.findall(Date) for Date in df_merge["Date"]]
        Dates2 = []

        i=0
        for i in range(len(Dates)) :
            year = "20"+Dates[i][0]
            Date_test = int(Dates[i][1]) + 2

            if Date_test > 12:
                year = str(int(year) + 1)
                year = year + "0" + str(Date_test - 11) + "28"

            else:
                if Date_test > 9:
                    year = year + str(Date_test) + "16"
                else:
                    year = year + "0" + str(Date_test) + "16"

            Dates2.append(year)

        df_merge["Date"] = Dates2
        df_merge["Date"] = pd.to_datetime(df_merge["Date"].astype(str))

        # 재무데이터 변환 결과물
        # df_merge

        # db에서 수정종가 데이터 가져오기
        df = pd.read_sql("SELECT * FROM %s" %name_list2[j], con, index_col=None) # SQLite DB 읽기

        # Date열 날짜형으로 변환
        df["Date"] = pd.to_datetime(df["Date"].astype(str))


        # 수정종가 데이터 변환 결과물
        # df

        # 날짜 다시한번 맞춰주기
        """
        수정종가 데이터가 2009년 11월 부터 밖에 없음 
        """
        df_merge = df_merge[df_merge["Date"] > min(df["Date"])]
        """
        재무데이터 날짜가 휴장일일 수 있기 때문에 가장 가까운 날짜로 변환
        """
        Date = [] # 변수 초기화
        Dates2 = [] # 변수 초기화
        for Date in df_merge["Date"]:
            if not Date in list(df["Date"]) :
                Dates2.append(min(df["Date"][df["Date"] > Date]))
            else :
                Dates2.append(Date)

        df_merge["Date"] = pd.Series(Dates2)

        # 재무데이터, 수정종가데이터 합치기
        df_fin = pd.merge(df,df_merge, how = "outer", on= "Date")
        try :
            df_fin.to_sql(name_list2[j] + "," + code_list2[j],con2, index=False)
        except : pass

    except :
        print(name_list2[j] + "," + code_list2[j] + " 오류")
        error_code2.append(name_list2[j] + "," + code_list2[j])
        continue

con.close()
con2.close()

error_code2

