"""
SARIMA model fitting fomula test

"""

import pandas as pd
import numpy as np
import statsmodels.api as sm
import statsmodels.tsa.api as tsa
import matplotlib.pyplot as plt
import statsmodels.formula.api as smf
import itertools



df = sm.datasets.get_rdataset("AirPassengers", "datasets").data
date = pd.date_range(start="19490101", end="19601201", freq="MS", closed=None)
df.index = date
df = df.drop(columns="time",)
df.columns = ["passengers"]
# df["passengers"].plot()

# remove trend, hetero
# df["log"] = np.log(df["passengers"])
# df["log_diff"] = df["log"].diff()
# df["log_diff"].plot()
# df.dropna(inplace=True)

# split the data into train and test
num = int(df.shape[0]*2/3)
train_df = df.iloc[:num,:]
test_df = df.drop(index=train_df.index)
#


train_df_log = np.log(train_df)
test_df_log = np.log(test_df)

m1 = tsa.SARIMAX(train_df_log,order=(1,1,0)).fit()
m1.summary()

m1_df = train_df_log.copy()
m1_df["dx"] = m1_df["passengers"].diff()
m1_df["dxhat"] = m1.params[0]*m1_df["dx"].shift(1)
m1_df["xhat"] = m1_df["dxhat"]+m1_df["passengers"].shift(1)
m1_df["m_fit"] = m1.fittedvalues
m1_df["err"] = m1_df["xhat"] -m1_df["m_fit"]
m1_df["err"].iloc[3:].plot()



m1 = tsa.SARIMAX(train_df_log,order=(1,1,1)).fit()

m1_df = train_df_log.copy()
m1_df["dx"] = m1_df["passengers"].diff()
m1_df["res"] = m1.resid
m1_df["dxhat"] = m1.params[0]*m1_df["dx"].shift(1)+ m1.params[1]*m1_df["res"].shift(1)
m1_df["xhat"] = m1_df["dxhat"]+m1_df["passengers"].shift(1)
m1_df["m_fit"] = m1.fittedvalues
m1_df["err"] = m1_df["xhat"] -m1_df["m_fit"]
m1_df["err"].iloc[3:].plot()



m1 = tsa.SARIMAX(train_df_log,order=(1,1,1), seasonal_order=(1,0,0,12), enforce_invertibility=False, enforce_stationarity=False).fit()

m1_df = train_df_log.copy()
m1_df["dx"] = m1_df["passengers"].diff()
m1_df["res"] = m1.resid

m1_df["dxhat"] = m1.params[0]*m1_df["dx"].shift(1) + m1.params[1]*m1_df["res"].shift(1) + \
                 m1.params[2]*m1_df["dx"].shift(12) - m1.params[0]*m1.params[2]*m1_df["dx"].shift(13)

m1_df["xhat"] = m1_df["dxhat"]+m1_df["passengers"].shift(1)
m1_df["m_fit"] = m1.fittedvalues
m1_df["err"] = m1_df["xhat"] -m1_df["m_fit"]
m1_df["err"].iloc[3:].plot()


m1 = tsa.SARIMAX(train_df_log,order=(1,1,1), seasonal_order=(1,0,1,12), enforce_invertibility=False, enforce_stationarity=False).fit()

m1_df = train_df_log.copy()
m1_df["dx"] = m1_df["passengers"].diff()
m1_df["res"] = m1.resid

m1_df["dxhat"] = m1.params[0]*m1_df["dx"].shift(1) + m1.params[1]*m1_df["res"].shift(1) + \
                 m1.params[2]*m1_df["dx"].shift(12) - m1.params[0]*m1.params[2]*m1_df["dx"].shift(13) + \
                 m1.params[3]*m1_df["res"].shift(12) + m1.params[1]*m1.params[3]*m1_df["res"].shift(13)

m1_df["xhat"] = m1_df["dxhat"]+m1_df["passengers"].shift(1)
m1_df["m_fit"] = m1.fittedvalues
m1_df["err"] = m1_df["xhat"] -m1_df["m_fit"]
m1_df["err"].iloc[3:].plot()


m1 = tsa.SARIMAX(train_df_log,order=(0,0,0), seasonal_order=(1,1,0,12), enforce_invertibility=False, enforce_stationarity=False).fit()
m1_df = train_df_log.copy()
m1_df["zt"] = m1_df["passengers"].diff(12)
# m1_df["res"] = m1.resid

m1_df["zthat"] = m1.params[0]*m1_df["zt"].shift(12)
m1_df["xhat"] = m1_df["zthat"]+m1_df["passengers"].shift(12)
m1_df["m_fit"] = m1.fittedvalues
m1_df["err"] = m1_df["xhat"] -m1_df["m_fit"]
m1_df["err"].plot()


