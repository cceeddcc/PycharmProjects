import pandas as pd
import os
import matplotlib.pyplot as plt
import numpy as np
import statsmodels.api as stm
import statsmodels.tsa.stattools as tsa

os.chdir("C:/Users/S/Desktop/")
df_wti_f = pd.read_csv("wti_future_price.csv")
df_kodex_wti = pd.read_csv("KODEX WTI.csv")

df_merge = pd.merge(df_kodex_wti,df_wti_f,on="Date",how="left")

df_merge.columns = ['Date', 'Open_K', 'High_K', 'Low_K', 'Close_K', 'Volume_K', 'Close_F', 'Open_F','High_F', 'Low_F']
df_merge = df_merge.loc[:,['Date',"Close_K","Close_F"]]
df_merge =  df_merge.sort_values(by='Date', ascending=True)
df_merge.index = [i for i in range(len(df_merge.index))]
df_merge["log_K"] = np.log(df_merge.iloc[:,1])
df_merge["log_W"] = np.log(df_merge.iloc[:,2])
df_merge["norm_K"] = (df_merge["Close_K"]-df_merge["Close_K"].mean())/df_merge["Close_K"].std(ddof=1)
df_merge["norm_W"] = (df_merge["Close_F"]-df_merge["Close_F"].mean())/df_merge["Close_F"].std(ddof=1)


fig, ax1 = plt.subplots()
ax1.plot(df_merge["norm_K"], color="red")
ax2 = ax1.twinx()
ax2.plot(df_merge["norm_W"], color="blue")


# 회귀분석
m = stm.formula.ols("Close_K~Close_F", data=df_merge)
r = m.fit()
r.summary()
df_merge["hat_Close_K"] = r.fittedvalues

df_merge["Close_K"].plot()
df_merge["hat_Close_K"].plot()

r.resid.plot()
r.fittedvalues



# outlier 제거
df_merge2 = df_merge.copy()
df_merge2 = df_merge2.drop(index=810)

# 회귀분석
m = stm.formula.ols("Close_K~Close_F", data=df_merge2)
r = m.fit()
r.summary()
df_merge2["hat_Close_K"] = r.fittedvalues

df_merge2["Close_K"].plot()
df_merge2["hat_Close_K"].plot()
r.resid.plot()
tsa.acf(r.resid, fft=False)
r.resid.hist(bins=100)

dir(r.predict)
help(r.predict)

# kodex price 예측
r.params[0] + r.params[1]*13.00

df_merge2