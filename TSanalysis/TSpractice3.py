import pandas as pd
import numpy as np
import statsmodels.api as sm
import statsmodels.tsa.api as tsa
import matplotlib.pyplot as plt
import datetime

df = sm.datasets.get_rdataset("AirPassengers", "datasets").data
date = pd.date_range(start="19490101", end="19601201", freq="MS", closed=None)
df["time"] = date
df.columns = ["Month", "passengers"]
indexedDataset = df.set_index(["Month"])
indexedDataset_logSacle = np.log(indexedDataset)
datasetLogDiffShifting = indexedDataset_logSacle.diff()
datasetLogDiffShifting = datasetLogDiffShifting.dropna()


df["passengers"].plot()

# stationary visual test
help(df.rolling)
rolmean = df["passengers"].rolling(window=12).mean()
rolstd = df["passengers"].rolling(window=12).std(ddof=1)
df["passengers"].plot()
rolmean.plot() # changing over time
rolstd.plot() # changing over time

# adf test
adf = tsa.adfuller(df["passengers"], autolag="AIC")
def print_adf(adf):
    print("test statistic : ", "{0:.4f}".format(adf[0]), "\n",
          "pvalue : ", "{0:.4f}".format(adf[1]), "\n",
          "The number of lags used : ", adf[2], "\n",
          "The number of observations used : ", adf[3], "\n",
          "critical values : ", adf[4], "\n")
print_adf(adf) # nonstationary

df["log_v"] = np.log(df["passengers"])
rolmean = df["log_v"].rolling(window=12).mean()
rolstd = df["log_v"].rolling(window=12).std(ddof=1)
df["log_v"].plot()
rolmean.plot() # changing over time
rolstd.plot() # changing over time

# first diff
df["log_diff"] = df["log_v"].diff(1)
df = df.dropna()
rolmean = df["log_diff"].rolling(window=12).mean()
rolstd = df["log_diff"].rolling(window=12).std(ddof=1)

df["log_diff"].plot() # have seasonality
rolmean.plot() # stationary
rolstd.plot() # stationary

adf = tsa.adfuller(df["log_diff"], autolag="AIC")
def print_adf(adf):
    print("test statistic : ", "{0:.4f}".format(adf[0]), "\n",
          "pvalue : ", "{0:.4f}".format(adf[1]), "\n",
          "The number of lags used : ", adf[2], "\n",
          "The number of observations used : ", adf[3], "\n",
          "critical values : ", adf[4], "\n")
print_adf(adf)

# decompose seasonality
help(tsa.seasonal_decompose)
decomposition = tsa.seasonal_decompose(indexedDataset_logSacle)
trend = decomposition.trend
seasonal = decomposition.seasonal
residual = decomposition.resid

plt.subplot(411)
plt.plot(indexedDataset_logSacle)
plt.legend(loc="best")
plt.subplot(412)
plt.plot(trend)
plt.legend(loc="best")
plt.subplot(413)
plt.plot(seasonal)
plt.legend(loc="best")
plt.subplot(414)
plt.plot(residual)
plt.legend(loc="best")

decomposedLogData = residual
decomposedLogData.dropna(inplace =True)
decomposedLogData.plot()
adf=tsa.adfuller(decomposedLogData)
print_adf(adf)


# acf ,pacf
datasetLogDiffShifting.plot()
tsa.graphics.plot_acf(datasetLogDiffShifting)
tsa.graphics.plot_pacf(datasetLogDiffShifting)

indexedDataset_logSacle.plot()

# find arima best order
tsa.arma_order_select_ic(datasetLogDiffShifting) #(2,1,2)

# arima model fitting
m = tsa.ARIMA(indexedDataset_logSacle, order=(2,1,2))
r = m.fit(disp=1)
plt.plot(datasetLogDiffShifting)
plt.plot(r.fittedvalues, color ="red")

indexedDataset_logSacle.plot()
predictions_ARIAM_diff_cumsum.plot()


predictions_ARIAM_diff = pd.Series(r.fittedvalues, copy=True)
predictions_ARIAM_diff_cumsum = predictions_ARIAM_diff.cumsum() # 차분데이터니까

predictions_ARIAM_log = pd.Series(indexedDataset_logSacle["passengers"])
predictions_ARIAM_log = predictions_ARIAM_log.add(predictions_ARIAM_diff_cumsum, fill_value=0)
predictions_ARIAM_log.plot()
indexedDataset_logSacle.plot()
predictions_ARIAM_diff_cumsum.plot()

# prediction
r.plot_predict()
help(r.plot_predict)
r.fittedvalues

# forecast
help(r.forecast)
data_for,a,b = r.forecast(steps=120)
df_for = pd.Series(data_for)
df_for.plot()


###############################################################################################################
###############################################################################################################
###############################################################################################################
import pandas as pd
import numpy as np
import statsmodels.api as sm
import statsmodels.tsa.api as tsa
import matplotlib.pyplot as plt


df = sm.datasets.get_rdataset("AirPassengers", "datasets").data
date = pd.date_range(start="19490101", end="19601201", freq="MS", closed=None)
df["time"] = date
df.columns = ["Month", "passengers"]
df["passengers"].plot()

# remove trend, hetero
df["log"] = np.log(df["passengers"])
df["log_diff"] = df["log"].diff()
df["log_diff"].plot()
df["log_diff"].dropna(inplace=True)

# adf test
adf = tsa.adfuller(df["log_diff"]) # 10% stationary

# acf, pacf
tsa.graphics.plot_acf(df["log_diff"], lags=140) # seasonality 12
tsa.graphics.plot_pacf(df["log_diff"], lags=140) # arma 유력

# remove seasonality
df["log_diff_12"] = df["log_diff"].diff(12)
df["log_diff_12"].plot()
df.dropna(inplace=True)
adf = tsa.adfuller(df["log_diff_12"])
adf # stationary

# acf, pacf
tsa.graphics.plot_acf(df["log_diff_12"], lags=100)
tsa.graphics.plot_pacf(df["log_diff_12"], lags=100)


# find model
order = tsa.arma_order_select_ic(y=df["log_diff_12"])
order

# sarima(0,1,0,0,1,1,12)
raw_s = pd.Series(df["log"])
raw_s.index = df["Month"]
sarima_m = tsa.SARIMAX(endog=raw_s, order=(0,1,0), seasonal_order=(0,1,1,12))
sarima_r = sarima_m.fit()
sarima_r.summary()

# arima
s2 = df["log_diff"]
s2.index = df["Month"]
tsa.arma_order_select_ic(s2) # arima(4,1,2)
arima_m = tsa.ARIMA(endog=raw_s,order=(4,1,2))
arima_r = arima_m.fit()
arima_r.summary()

print("sarima_aic : ", sarima_r.aic, "\n",
      "arima_aic : ", arima_r.aic, "\n",)
# sarima가 훨씬 좋은 모델 확인

# prediction 비교
dir(arima_r)
arima_r.resid
tsa.adfuller(arima_r.resid) # nonstationary
tsa.adfuller(sarima_r.resid) # stationary
fitted = sarima_r.fittedvalues
fitted.index = [i for i in range(len(fitted.index))]
df.index = [i for i in range(len(df.index))]
df_sarima = pd.DataFrame({"pass" : df["log"],
                          "sarima" : fitted})
df_sarima = df_sarima.iloc[20:,:]
dir(arima_r)
plt.plot(df_sarima.iloc[:,0])
plt.plot(df_sarima.iloc[:,1])

fitted = arima_r.fittedvalues
fitted.index = [i for i in range(len(fitted.index))]
df_arima = pd.DataFrame({"pass" : df["log"],
                          "arima" : fitted})
plt.subplot(111)
plt.plot(df_arima.iloc[:,0])
plt.plot(df_arima.iloc[:,1])
# resid diagnostics
sarima_r.plot_diagnostics()

sarima_r.summary()
