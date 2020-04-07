import pandas as pd
import numpy as np
import statsmodels.formula.api as smf
from pandas.plotting import scatter_matrix
import pandas_datareader as dr

# scatter plot
sm = scatter_matrix(housing, figsize=(10,10))

# OLS
m = smf.ols(formula="y~x", data=housing).fit()
m.summary()

# Durbin Watson test for serial correlation
# H0 : no firts order autocorrelation

# normality
# qq plot, qqline
import scipy.stats as stats
import matplotlib.pyplot as plt
z = np.random.normal(10,4,100)
stats.probplot(z, dist="norm", plot=plt)

# linear regression assumption 위반한 경우
# 가설검정 불가능 -> std.error가 문제
# model의 accuracy, consistency는 유지됨
# coefficient 사용가능하다는 의미

# multiple linear regression model
formula = 'spy~spy_lag1+sp500+nasdaq+dji+cac40+aord+daxi+nikkei+hsi'
lm = smf.ols(formula=formula, data=Train).fit()
lm.summary()

# prediction
Train['PredictedY'] = lm.predict(Train)
Test['PredictedY'] = lm.predict(Test)

# Evaluation of model

# Sharpe Ratio on Train data
Train['Return'] = np.log(Train['Wealth']) - np.log(Train['Wealth'].shift(1))
dailyr = Train['Return'].dropna()

print('Daily Sharpe Ratio is ', dailyr.mean()/dailyr.std(ddof=1))
print('Yearly Sharpe Ratio is ', (252**0.5)*dailyr.mean()/dailyr.std(ddof=1))

# Maximum Drawdown in Train data
Train['Peak'] = Train['Wealth'].cummax()
Train['Drawdown'] = (Train['Peak'] - Train['Wealth'])/Train['Peak']
print('Maximum Drawdown in Train is ', Train['Drawdown'].max())
