from CP import Cybos_mod as cm
import pandas as pd
import sqlite3 as sql
import os

os.chdir("C:/Users/S/Desktop/바탕화면(임시)/KOSPI/")
con = sql.connect("kospi_price.db")
kospi1 = cm.CP_KOSPI()
kospi1.login_CP()

codelist = kospi1.Get_code_by_seckind("주권")
codename = kospi1.Get_name_by_seckind("주권")

# code = codelist[0]
Sdate = 20190401
Edate = 20200425

t = 0
df_kospi = pd.DataFrame({"Date" : pd.date_range("20050101", "20100101")})
for code in codelist[:10] :
    t += 1
    print(t, " / ", len(codelist))
    df = kospi1.Get_Data(code, Sdate=Sdate, Edate=Edate)
    df_kospi = df_kospi.merge(df.iloc[:,[0,4]],on="Date",how="left")
    df_kospi.to_sql()

con.close()




