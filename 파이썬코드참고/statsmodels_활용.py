import numpy as np
import statsmodels.api as sm
import statsmodels.formula.api as smf
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt




# 데이터 불러오기 및 정제
con = sqlite3.connect("C:/Users/S/desktop/바탕화면(임시)/KOSPI/tmp/KOSPI_PriceFinance_DB.db")
df = pd.read_sql("select Date, Close, BPS from A000020",con,index_col=None)
df = pd.read_sql("select * from A001260",con,index_col=None)
df.to_csv("C:/Users/S/Desktop/akak.csv")
df = df.fillna(method="pad")
df = df[~df["BPS"].isna()]
df.insert(len(df.columns), "PBR", df["Close"] / df["BPS"])

df.index = range(len(df["Date"]))

for i in range(len(df["Date"])) :
    df["Date"][i] = df["Date"][i].split("-")[0]

Year_index = df.groupby("Date").mean().index
df

model =smf.ols(formula= "Close ~ BPS", data = df)
result = model.fit()
result.summary()
result.params["Intercept"]
result.params["BPS"]
price1 = -2478.0952 + 1.1760*df["BPS"]
df.insert(len(df[""]))
pd.DataFrame.insert(df,len(df.columns),"Y",price1)
df

plt.plot(df["BPS"],df["Close"],"ro", color = "red")
plt.plot(df["BPS"],df["Residual2"],"ro", color = "red")
plt.plot(df["BPS"],df["Y"], color = "blue")
plt.plot(df["BPS"],df["Residual"], color = "blue")
pd.DataFrame.insert(df,len(df.columns),"Residual2",df["Close"] - df["BPS"])
df

plt.hist(df["Residual"])
plt.show()





import numpy as np
import statsmodels.api as sm
import statsmodels.formula.api as smf
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt

# 종목명, 코드 불러오기
with open("C:\\Users\\S\\Desktop\\바탕화면(임시)\\KOSPI\\KOSPI_codelist.txt", "r") as f :
    code_list = [line.split("\n")[0] for line in f.readlines()]
con = sqlite3.connect("C:/Users/S/desktop/바탕화면(임시)/KOSPI/tmp/KOSPI_PriceFinance_DB.db")
i = 0
PBR_dict ={}
for code in code_list :
    try :
        print(i, "/", len(code_list))
        i += 1
        df = pd.read_sql("select Date, Close, BPS from %s" %code,con,index_col=None)
        df = df.fillna(method="pad")
        df = df[~df["BPS"].isna()]
        df = df[df["BPS"] >0]
        df = df[df["Date"] > "2010"]
        model = smf.ols(formula="Close ~ BPS", data=df)
        result = model.fit()
        price1 = result.params["Intercept"] + result.params["BPS"] * df["BPS"]
        df.insert(len(df.columns), "Residual", (df["Close"]-price1)/df["Close"])
        PBR_dict["%s" %code] = min(df["Residual"])


    except : continue



con.close()
A=list(PBR_dict.values())
for name,value in PBR_dict.items() :
    if value < -17 :
        print(name)

B=pd.Series(A)
plt.plot(B,"ro")

B=B[B>-50]

# A025620': -135.2346191682887
code= "A025620"
con = sqlite3.connect("C:/Users/S/desktop/바탕화면(임시)/KOSPI/tmp/KOSPI_PriceFinance_DB.db")

df = pd.read_sql("select Date, Close, BPS from %s" %code,con,index_col=None)
df = df.fillna(method="pad")
df = df[~df["BPS"].isna()]
df = df[df["BPS"] >0]
df[df["Date"]>"2010"]
model = smf.ols(formula="Close ~ BPS", data=df)
result = model.fit()
price1 = result.params["Intercept"] + result.params["BPS"] * df["BPS"]
plt.plot(price1, "ro")
df.insert(len(df.columns), "Residual", (df["Close"]-price1)/df["Close"])

import numpy as np
pip install tensorflow
import tensorflow as tf
import matplotlib.pyplot as plt

num_points = 1000
vectors_set = []
for i in range(num_points):
    x1 =np.random.normal(0.0, 0.5)
    y1 = x1*0.1 + 0.3 + np.random.normal(0.0, 0.03) #y = x*0.1 + 0.3의 함수식으로 회귀되는 1000개의 [x, y]데이터를 생성
    vectors_set.append([x1, y1])
    #y = 0.1x + 0.3의 관계에있는 점들에 조금의 변수를 줌 (normal distribution의 편차를 둠))
x_data = [v[0] for v in vectors_set]
y_data = [v[1] for v in vectors_set]

plt.plot(x_data, y_data, "ro", label = "Original Data")
plt.legend()
plt.show()




