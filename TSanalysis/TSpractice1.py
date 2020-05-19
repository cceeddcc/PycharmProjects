import statsmodels.tsa.stattools as tsat
import pandas as pd
import matplotlib.pyplot as plt

df_con = pd.DataFrame()
for i in range(1,15) :
    i = str(i)
    df = pd.read_csv("C:/Users/S/Desktop/tsdata/data (%s).csv" %i)
    df_con = pd.concat([df_con, df.iloc[:, [0, 1]]], axis=0)

df_con.columns = ["Date", "PER"]
df_con.iloc[:,0] = pd.to_datetime(df_con.iloc[:,0])
df_con = df_con.sort_values(by="Date", ascending=True)
df_con.index = [i for i in range(len(df_con.index))]
plt.plot(df_con["PER"], "--o")

tsat.acf(df_con["PER"])

import statsmodels.graphics.tsaplots as tsap
tsap.plot_acf(df_con["PER"], lags=36)
tsap.plot_pacf(df_con["PER"], lags=36, zero=False)

dir(statsmodels.api.tsa)
import statsmodels.api as api
m = api.tsa.arma_order_select_ic(df_con["PER"])

m = api.tsa.arima.ARIMA(df_con["PER"], order = (1, 0 , 0))
res = m.fit()
print(res.summary())
