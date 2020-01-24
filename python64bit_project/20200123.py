"""
KOSPI_Price_DB_merge_final 파일 생성
"""

import pandas as pd
import sqlite3


# 종목명, 코드 불러오기
with open("C:\\Users\\S\\Desktop\\바탕화면(임시)\\KOSPI\\KOSPI_codelist.txt", "r") as f :
    code_list = [line[1:].split("\n")[0] for line in f.readlines()]

with open("C:\\Users\\S\\Desktop\\바탕화면(임시)\\KOSPI\\KOSPI_namelist.txt", "r") as f :
    name_list = [line.split("\n")[0] for line in f.readlines()]

columns = ['Date', 'Price', 'Asset', 'Capital', 'Sales', 'Operating', 'Profit',
       'Retention', 'CFO', 'CFI', 'CFF', 'Liability', 'Sa_Margin',
       'non-operating', 'COGS', 'SGA', 'EBIT', 'NetCF', 'div_rate', 'EBITDA',
       'PayoutRatio', 'Return'] # columns 지정
con = sqlite3.connect("C:/Users/S/desktop/바탕화면(임시)/KOSPI/tmp/KOSPI_PriceFinance_DB.db")
con2 = sqlite3.connect("C:/Users/S/Desktop/바탕화면(임시)/KOSPI/tmp/KOSPI_Price_DB_merge2.db")
con3 = sqlite3.connect("C:/Users/S/Desktop/바탕화면(임시)/KOSPI/tmp/KOSPI_Price_DB_merge_final.db")
i = 1
for code in code_list :
    try :
        print(i," / ", len(code_list))
        i += 1
        code = "A" + code
        df1 = pd.read_sql("select * from %s" %code, con, index_col=None)
        df2 = pd.read_sql("select * from %s" %code, con2, index_col=None)
        df_merge = pd.merge(df2,df1[columns],on="Date", how="outer")
        df_merge.to_sql(code,con3,index=False)
    except : continue


con.close()
con2.close()
con3.close()



"""
데이터 조합 1
"""
import pandas as pd
import sqlite3

# 종목명, 코드 불러오기
with open("C:\\Users\\S\\Desktop\\바탕화면(임시)\\KOSPI\\KOSPI_codelist.txt", "r") as f :
    code_list = [line[1:].split("\n")[0] for line in f.readlines()]

with open("C:\\Users\\S\\Desktop\\바탕화면(임시)\\KOSPI\\KOSPI_namelist.txt", "r") as f :
    name_list = [line.split("\n")[0] for line in f.readlines()]

con1 = sqlite3.connect("C:/Users/S/desktop/바탕화면(임시)/KOSPI/tmp/KOSPI_Price_DB10.db")
con2 = sqlite3.connect("C:/Users/S/desktop/바탕화면(임시)/KOSPI/tmp/KOSPI_Price_DB11.db")
con3 = sqlite3.connect("C:/Users/S/desktop/바탕화면(임시)/KOSPI/tmp/KOSPI_Price_DB12.db")
con4 = sqlite3.connect("C:/Users/S/desktop/바탕화면(임시)/KOSPI/tmp/KOSPI_Price_DB_merge_adj.db")
con5 = sqlite3.connect("C:/Users/S/desktop/바탕화면(임시)/KOSPI/tmp/KOSPI_Price_DB_merge_adj2.db")

i = 1
for code in code_list :
    try :
        print(i," / ",len(code_list))
        i += 1
        code = "A" + code
        df1 = pd.read_sql("SELECT * FROM %s" %code, con1, index_col=None)
        df2 = pd.read_sql("SELECT * FROM %s" %code, con2, index_col=None)
        df3 = pd.read_sql("SELECT * FROM %s" %code, con3, index_col=None)
        df4 = pd.read_sql("SELECT * FROM %s" %code, con4, index_col=None)
        df_merge = pd.concat([df4,df3,df2,df1])
        df_merge = df_merge.sort_values(by="Date")

        df_merge.index = range(len(df_merge["Date"]))
        df_merge.to_sql(code, con5, index = False)
        df_merge.to_csv("c:/Users/S/Desktop/ss.csv")
    except : continue

con1.close()
con2.close()
con3.close()
con4.close()
con5.close()

"""
데이터 조합 2
"""
import pandas as pd
import sqlite3

# 종목명, 코드 불러오기
with open("C:\\Users\\S\\Desktop\\바탕화면(임시)\\KOSPI\\KOSPI_codelist.txt", "r") as f:
    code_list = [line[1:].split("\n")[0] for line in f.readlines()]

with open("C:\\Users\\S\\Desktop\\바탕화면(임시)\\KOSPI\\KOSPI_namelist.txt", "r") as f:
    name_list = [line.split("\n")[0] for line in f.readlines()]

con1 = sqlite3.connect("C:/Users/S/desktop/바탕화면(임시)/KOSPI/tmp/KOSPI_Price_DB1010.db")
con2 = sqlite3.connect("C:/Users/S/desktop/바탕화면(임시)/KOSPI/tmp/KOSPI_Price_DB1111.db")
con3 = sqlite3.connect("C:/Users/S/desktop/바탕화면(임시)/KOSPI/tmp/KOSPI_Price_DB1212.db")
con4 = sqlite3.connect("C:/Users/S/desktop/바탕화면(임시)/KOSPI/tmp/KOSPI_Price_DB_merge_noadj.db")
con5 = sqlite3.connect("C:/Users/S/desktop/바탕화면(임시)/KOSPI/tmp/KOSPI_Price_DB_merge_noadj2.db")

i = 1
for code in code_list:
    try:
        print(i, " / ", len(code_list))
        i += 1
        code = "A" + code
        df1 = pd.read_sql("SELECT * FROM %s" % code, con1, index_col=None)
        df2 = pd.read_sql("SELECT * FROM %s" % code, con2, index_col=None)
        df3 = pd.read_sql("SELECT * FROM %s" % code, con3, index_col=None)
        df4 = pd.read_sql("SELECT * FROM %s" % code, con4, index_col=None)
        df_merge = pd.concat([df4, df3, df2, df1])
        df_merge = df_merge.sort_values(by="Date")

        df_merge.index = range(len(df_merge["Date"]))
        df_merge.to_sql(code, con5, index=False)
    except:
        continue

con1.close()
con2.close()
con3.close()
con4.close()
con5.close()


"""
데이터 베이스 merge2
"""
import sqlite3
import pandas as pd

con_merge_adj = sqlite3.connect("C:/Users/S/desktop/바탕화면(임시)/KOSPI/tmp/KOSPI_Price_DB_merge_adj2.db")
con_merge_noadj = sqlite3.connect("C:/Users/S/desktop/바탕화면(임시)/KOSPI/tmp/KOSPI_Price_DB_merge_noadj2.db")
con_merge = sqlite3.connect("C:/Users/S/desktop/바탕화면(임시)/KOSPI/tmp/KOSPI_Price_DB_merge2.db")


i = 1
for code in code_list :
    try :
        # code = "000020"
        print(i," / ",len(code_list))
        i += 1
        code = "A" + code
        df1 = pd.read_sql("SELECT * FROM %s" %code, con_merge_adj, index_col=None)
        df2 = pd.read_sql("SELECT * FROM %s" %code, con_merge_noadj, index_col=None)
        df1 = df1.iloc[:-1, :]
        df2 = df2.iloc[:-1, :]
        df1["Date"] = pd.to_datetime(df1["Date"].astype(str))
        df2["Date"] = pd.to_datetime(df2["Date"].astype(str))
        df_merge = pd.merge(df1, df2, on='Date')  # outer join
        df_merge.index = range(len(df_merge["Date"]))
        df_merge.to_sql(code, con_merge, index = False)
    except : continue
con_merge_adj.close()
con_merge_noadj.close()
con_merge.close()

"""
데이터 형식 float으로 변환 
"""
# 데이터 형식 float으로 모두 변환

import sqlite3
import pandas as pd
# 종목명, 코드 불러오기
with open("C:\\Users\\S\\Desktop\\바탕화면(임시)\\KOSPI\\KOSPI_codelist.txt", "r") as f:
    code_list = [line[1:].split("\n")[0] for line in f.readlines()]

con = sqlite3.connect("C:/Users/S/desktop/바탕화면(임시)/KOSPI/tmp/KOSPI_Price_DB_merge_final.db")
con2 = sqlite3.connect("C:/Users/S/desktop/바탕화면(임시)/KOSPI/tmp/KOSPI_Price_DB_merge_final2.db")
j = 1
for code in code_list :
    print(j , " / ", len(code_list))
    j += 1
    code = "A" + code
    df = pd.read_sql("select * from %s" %code, con, index_col=None)

    for col in df.columns :
        for i in range(len(df[col])) :
            try :
                df[col][i] = df[col][i].replace(",","")
            except : continue
        try :
            df[col] = df[col].astype(float)
        except : continue
    df.to_sql(code,con2, index= False)

con.close()
con2.close()

"""
데이터 분석 
"""

import sqlite3
import pandas as pd
con = sqlite3.connect("C:/Users/S/desktop/바탕화면(임시)/KOSPI/tmp/KOSPI_Price_DB_merge_final.db")
df = pd.read_sql("select * from A000020", con, index_col=None)
df.columns
con.close()