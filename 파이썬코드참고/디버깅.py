
"""
최종작업
재무데이터 merging 및 날짜 변환 -> 종가데이터와 합치기
"""
import pandas as pd
import re
import sqlite3

# 에러코드 불러오기
with open("C:\\Users\\S\\Desktop\\바탕화면(임시)\\KOSPI\\tmp\\error_code.txt", "r") as f :
    code_list = [line.split("\n")[0] for line in f.readlines()]


error_code2 = []
j = 1
con = sqlite3.connect("C:/Users/S/desktop/바탕화면(임시)/KOSPI/tmp/KOSPI_Price_DB_merge.db")
con2 = sqlite3.connect("C:/Users/S/desktop/바탕화면(임시)/KOSPI/tmp/KOSPI_PriceFinance_DB.db")

# KOSPI_PriceFinance_DB 만들기 최종
for code in code_list :
    try:
        print(j," / ",len(code_list))
        j += 1
        df_finance1 = pd.read_csv("C:\\Users\\S\\Desktop\\바탕화면(임시)\\KOSPI재무\\"+ code + ".csv", encoding="euc-kr")
        df_finance2 = pd.read_csv("C:\\Users\\S\\Desktop\\바탕화면(임시)\\KOSPI재무2\\"+ code + ".csv", encoding="euc-kr")
        df_finance_merge = pd.merge(df_finance1,df_finance2)

        columns = ["Date","Price","Asset","Capital","Sales","Operating","Profit","Retention","CFO","CFI","CFF",
                   "Op_Margin","Liability","Sa_Margin","non-operating","COGS","SGA","EBIT","NetCF",
                   'BPS', 'CFPS', 'PSR', 'PER', 'SPS', 'div_rate', 'PBR', 'EBITDA','EPS', "EV/EB",
                   'PayoutRatio', 'Return', 'DPS', 'PCR']
                # 날짜, 주가, 자산, 자본, 매출액, 영업이익, 당기순이익,
        df_finance_merge.columns = columns
        df_finance_merge = df_finance_merge[~df_finance_merge["Date"].isna()]

        # 데이터 형식 float으로 모두 변환
        for col in df_finance_merge.columns :
            for i in range(len(df_finance_merge[col])) :
                try :
                    df_finance_merge[col][i] = df_finance_merge[col][i].replace(",","")
                except : continue
            try :
                df_finance_merge[col] = df_finance_merge[col].astype(float)
            except : continue

        # 결산년도 날짜데이터로 변환시키기
        r = re.compile("[0-9]+")
        Dates_finance1 = [r.findall(Date) for Date in df_finance_merge["Date"]]
        Dates_finance2 = []

        i=0
        for i in range(len(Dates_finance1)) :
            if int(Dates_finance1[i][0]) > 20 :
                year = "19"+Dates_finance1[i][0]
            else:
                year = "20"+Dates_finance1[i][0]
            month_test = int(Dates_finance1[i][1]) + 2

            if month_test > 12:
                year = str(int(year) + 1) + "0" + str(month_test - 11) + "28"

            else:
                if month_test > 9:
                    year = year + str(month_test) + "16"
                else:
                    year = year + "0" + str(month_test) + "16"

            Dates_finance2.append(year)

        df_finance_merge["Date"] = Dates_finance2
        df_finance_merge["Date"] = pd.to_datetime(df_finance_merge["Date"].astype(str))

        # db에서 수정종가 데이터 가져오기
        code = "A" + code
        df_price = pd.read_sql("SELECT * FROM %s" % code, con, index_col=None)  # SQLite DB 읽기

        # Date열 날짜형으로 변환
        df_price["Date"] = pd.to_datetime(df_price["Date"].astype(str))

        # 수정종가 데이터 변환 결과물
        # df_price

        # 날짜 다시한번 맞춰주기
        """
        수정종가 데이터가 재무데이터 날짜보다 적을 수 있음 
        """
        df_finance_merge = df_finance_merge[df_finance_merge["Date"] > min(df_price["Date"])]

        # 재무데이터 날짜가 휴장일일 수 있기 때문에 가장 가까운 날짜로 변환
        Date_check = []
        for Date in df_finance_merge["Date"]:
            if not Date in list(df_price["Date"]):
                Date_check.append(min(df_price["Date"][df_price["Date"] > Date]))
            else:
                Date_check.append(Date)

        df_finance_merge["Date"] = pd.Series(Date_check)

        # 재무데이터, 수정종가데이터 합치기
        df_finance_merge = df_finance_merge.sort_values(by="Date")
        df_final = pd.merge(df_price, df_finance_merge, how="outer", on="Date")
        try:
            df_final.to_sql(code, con2, index=False)
        except:
            pass

    except:
        print(code + " 오류")
        error_code2.append(code)
        continue

con.close()
con2.close()


# error_code 저장

with open("c:/Users/S/Desktop/바탕화면(임시)/KOSPI/tmp/error_code2.txt", "w") as f:
    [f.write(lines + "\n") for lines in error_code2]