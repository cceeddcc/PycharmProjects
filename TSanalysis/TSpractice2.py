"""
DF, ADF, KPSS, PP 검정에 대해서 연습
"""

import statsmodels.tsa.api as tsa
import statsmodels.api as sm

# feeding data
sm.datasets.__all__
data = sm.datasets.co2.load_pandas()
co2_df = data.data
co2_df.plot()

# dealing missing data
co2_df = co2_df.fillna(method="ffill")
co2_df.plot()

# remove trend
co2_df["diff"] = co2_df["co2"].diff()
co2_df = co2_df.dropna()
co2_df["diff"].plot()

# unit root test
def print_adf(adf):
    print("test statistic : ", adf[0], "\n",
          "pvalue : ", adf[1], "\n",
          "The number of lags used : ", adf[2], "\n",
          "The number of observations used : ", adf[3], "\n",
          "critical values : ", adf[4], "\n")

adf = tsa.adfuller(x=co2_df["diff"]) # y is stationary
print_adf(adf)
tsa.kpss(x=co2_df["diff"]) # y is stationary

# find arma
# graphics
tsa.graphics.plot_acf(x=co2_df["diff"], zero=False) # seasonality 보임
tsa.graphics.plot_pacf(x=co2_df["diff"], zero=False) # seasonality 보임
tsa.graphics.plot_acf(x=co2_df["co2"], zero=False) # seasonality 보임
tsa.graphics.plot_pacf(x=co2_df["co2"], zero=False) # seasonality 보임
co2_df["diff_4"] = co2_df["co2"] - co2_df["co2"].shift(4)
co2_df["diff_4"].dropna().plot()
adf = tsa.adfuller(x=co2_df["diff_4"].dropna()) # y is stationary
print_adf(adf)

tsa.graphics.plot_acf(x=co2_df["diff_4"], zero=False, missing="drop")
tsa.graphics.plot_pacf(x=co2_df["diff_4"].dropna(), zero=False)

co2_df["diff_42"] = co2_df["diff_4"] - co2_df["diff_4"].shift(1)
tsa.graphics.plot_acf(x=co2_df["diff_42"], zero=False, missing="drop") # ma(5) 추정
tsa.graphics.plot_pacf(x=co2_df["diff_42"].dropna(), zero=False)

order = tsa.arma_order_select_ic(y=co2_df["diff_42"].dropna(),max_ar=5,max_ma=5,ic="aic")
# ARMA(5,4)

m = tsa.arima.ARIMA(endog=co2_df["diff_42"].dropna(),order=(5,0,4))
r = m.fit()
r.summary()
r.predict().plot()