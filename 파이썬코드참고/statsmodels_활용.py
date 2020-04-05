import statsmodels.api as sm
import pandas as pd
from patsy import dmatrices
import numpy as np
import matplotlib.pyplot as plt


## sm.datasets.get_rdataset()
"""
r data sets 불러오기  
"""
df = sm.datasets.get_rdataset("Guerry","HistData").data
df = df.dropna()

## sm.webdoc()
"""
search for documentation in the web 
"""
sm.webdoc() # go to Documentation site
sm.webdoc("glm") # search for glm in docs
sm.webdoc(sm.webdoc)
sm.webdoc(sm.OLS, stable=False)

## sm.stats.linear_rainbow()
"""
apply the Rainbow test for linearity
H0 is that the relationship is properly modelled as linear
"""
sm.stats.linear_rainbow(res)
print(sm.stats.linear_rainbow.__doc__)


#### Linear Regression

### OLS(Ordinary Least Squares)
# ex)
np.random.seed(9876789)

# OLS estimation
nsample = 100
x = np.linspace(0, 10, 100)
X = np.column_stack((x, x**2))
beta = np.array([1, 0.1, 10])
e = np.random.normal(size=nsample)

X = sm.add_constant(X)
y = np.dot(X, beta) + e

model = sm.OLS(y, X)
results = model.fit()
print(results.summary())

print('Parameters: ', results.params)
print('R2: ', results.rsquared)

# ex) OLS non-linear curve but linear in parameters
nsample = 50
sig = 0.5
x = np.linspace(0, 20, nsample)
X = np.column_stack((x, np.sin(x), (x-5)**2, np.ones(nsample)))
beta = [0.5, 0.5, -0.02, 5.]

y_true = np.dot(X, beta)
y = y_true + sig * np.random.normal(size=nsample)

res = sm.OLS(y, X).fit()
print(res.summary())

print('Parameters: ', res.params)
print('Standard errors: ', res.bse)
print('Predicted values: ', res.predict())

# draw plot
from statsmodels.sandbox.regression.predstd import wls_prediction_std
prstd, iv_l, iv_u = wls_prediction_std(res)

fig, ax = plt.subplots(figsize=(8,6))

ax.plot(x, y, 'o', label="data")
ax.plot(x, y_true, 'b-', label="True")
ax.plot(x, res.fittedvalues, 'r--.', label="OLS")
ax.plot(x, iv_u, 'r--')
ax.plot(x, iv_l, 'r--')
ax.legend(loc='best');


# ex) OLS with dummy variables
nsample = 50
groups = np.zeros(nsample, int)
groups[20:40] = 1
groups[40:] = 2
#dummy = (groups[:,None] == np.unique(groups)).astype(float)
dummy = sm.categorical(groups, drop=True)
x = np.linspace(0, 20, nsample)
# drop reference category

X = np.column_stack((x, dummy[:,1:]))
X = sm.add_constant(X, prepend=False)

beta = [1., 3, -3, 10]
y_true = np.dot(X, beta)
e = np.random.normal(size=nsample)
y = y_true + e

res2 = sm.OLS(y, X).fit()
print(res2.summary())

# draw plot
prstd, iv_l, iv_u = wls_prediction_std(res2)

fig, ax = plt.subplots(figsize=(8,6))

ax.plot(x, y, 'o', label="Data")
ax.plot(x, y_true, 'b-', label="True")
ax.plot(x, res2.fittedvalues, 'r--.', label="Predicted")
ax.plot(x, iv_u, 'r--')
ax.plot(x, iv_l, 'r--')
legend = ax.legend(loc="best")

# ex) Joint hypothesis test
"""
We want to test the hypothesis that both coefficients 
on the dummy variables are equal to zero, that is, R×β=0. 
An F test leads us to strongly reject the null hypothesis 
of identical constant in the 3 groups:
"""

R = [[0, 1, 0, 0],
     [0, 0, 1, 0]]
print(np.array(R))
print(res2.f_test(R))

beta = [1., 0.3, -0.0, 10]
y_true = np.dot(X, beta)
y = y_true + np.random.normal(size=nsample)

res3 = sm.OLS(y, X).fit()
print(res3.f_test(R))
print(res3.f_test("x2 = x3 = 0"))


# ex) Multicollinearity
from statsmodels.datasets.longley import load_pandas
y = load_pandas().endog
X = load_pandas().exog
X = sm.add_constant(X)

ols_model = sm.OLS(y, X)
ols_results = ols_model.fit()
print(ols_results.summary())

# Condition number
"""
One way to assess multicollinearity is to compute the condition number. 
Values over 20 are worrisome (see Greene 4.9). 
The first step is to normalize the independent variables 
to have unit length:
"""
norm_x = X.values
for i, name in enumerate(X):
    if name == "const":
        continue
    norm_x[:,i] = X[name]/np.linalg.norm(X[name])
norm_xtx = np.dot(norm_x.T,norm_x)

eigs = np.linalg.eigvals(norm_xtx)
condition_number = np.sqrt(eigs.max() / eigs.min())
print(condition_number)

# Dropping an observation
ols_results2 = sm.OLS(y.iloc[:14], X.iloc[:14]).fit()
print("Percentage change %4.2f%%\n"*7 % tuple([i for i in (ols_results2.params - ols_results.params)/ols_results.params*100]))



#### Time Series Analysis
df = sm.datasets.get_rdataset("AirPassengers", "datasets").data
df
plt.plot(df.iloc[:,0],df.iloc[:,1])

# data setting
df["diff"] = df.iloc[:,1]-df.iloc[:,1].shift(1)
plt.plot(df.iloc[:,0],df.iloc[:,2]) # remove trend

df["log"] = np.log(df.iloc[:,1])
plt.plot(df.iloc[:,0],df.iloc[:,3]) # remove heteroskedasticity

df["log_diff"] = df.iloc[:,3] - df.iloc[:,3].shift(1)
plt.plot(df.iloc[:,0],df.iloc[:,4])

df["log_diff_12"] = df.iloc[:,4]-df.iloc[:,4].shift(12)
plt.plot(df.iloc[:,0],df.iloc[:,5])

## sm.tsa.stattools.acovf
from statsmodels.tsa.stattools import acovf
autocov = acovf(df["log_diff_12"], missing="drop")
autocov

## sm.tsa.stattools.acf()
from statsmodels.tsa.stattools import acf
acf(df["log_diff_12"], missing="drop")

## sm.tsa.stattools.pacf()
from statsmodels.tsa.stattools import pacf
pacf(df["log_diff_12"].dropna(),method="ywm")

## statsmodels.tsa.stattools.q_stat()
"""
Compute Ljung-Box Q Statistic.
Returns q-statistics, p-value
"""
from statsmodels.tsa.stattools import q_stat
q_stat(df["log_diff_12"].dropna(),10)


## sm.tsa.arima.ARIMA()
m = sm.tsa.arima.ARIMA(endog=df["value"],
                       order=(1,1,0),
                       exog=df["time"])
res = m.fit()
print(res.summary())



#### Graphics

## sm.qqplot()
"""
Q-Q plot of the quantiles of x versus the quantiles/ppf of a distribution.
"""
ax = plt.subplot(1,1,1)
sm.qqplot(df["log_diff_12"], ax=ax)


## sm.graphics.tsa.plot_acf()
"""
Plot the autocorrelation function
Plots lags on the horizontal and the correlations on vertical axis.
"""
from statsmodels.graphics.tsaplots import plot_acf
plot_acf(df["log_diff_12"],lags=40,missing="drop")
plot_acf(df["log_diff_12"],missing="drop")
plot_acf(df["log_diff_12"],missing="drop",alpha=.01)
plot_acf(df["log_diff_12"],missing="drop",alpha=.01, unbiased=True)

## sm.graphics.tsa.plot_pacf()
"""
Plot the partial autocorrelation function
"""
from statsmodels.graphics.tsaplots import plot_pacf
plot_pacf(df["log_diff_12"].dropna(), method="ywmle", zero=False)


## sm.qqplot_2samples()
"""
Q-Q Plot of two samples’ quantiles.
"""
x = df["log_diff_12"]
y = np.random.normal(0,1,len(df["log_diff_12"]))
sm.qqplot_2samples(x, y)







sm.qqline(ax=ax, line="q", y= df["log_diff_12"],x=None)




## Correlation matrix
import numpy as np
import matplotlib.pyplot as plt
import statsmodels.graphics.api as smg
hie_data = sm.datasets.randhie.load_pandas()
corr_matrix = np.corrcoef(hie_data.data.T)
smg.plot_corr(corr_matrix, xnames=hie_data.names)
plt.show()