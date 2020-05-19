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
# train_df = df.iloc[:131,:]
# test_df = df.drop(index=train_df.index)

# adf test
# adf = tsa.adfuller(train_df["log_diff"]) # 10% stationary
# def print_adf(adf):
#     print("test statistic : ", "{0:.4f}".format(adf[0]), "\n",
#           "pvalue : ", "{0:.4f}".format(adf[1]), "\n",
#           "The number of lags used : ", adf[2], "\n",
#           "The number of observations used : ", adf[3], "\n",
#           "critical values : ", adf[4], "\n")
# print_adf(adf)

# df_tmp = train_df.copy()
# df_tmp["dyt"] = df_tmp["log_diff"].diff()
# df_tmp["gamma"] = df_tmp["log_diff"].shift(1)
#
# for i in range(1,13) :
#     df_tmp["exo%s" %str(i)] = df_tmp["dyt"].shift(i)
#
# df_tmp.dropna(inplace=True)
# form = "dyt~gamma"
# for i in range(1,13) :
#     form += "+exo%s" %str(i)
#
#
# m = smf.ols(formula=form,data=df_tmp)
# r = m.fit()
# r.summary()
# print_adf(adf)

# acf, pacf
# tsa.graphics.plot_acf(train_df["log_diff"]) # quarterly, monthly seasonality보임
# tsa.graphics.plot_pacf(train_df["log_diff"])

# find model





def find_best_sarima(train, eval_metric, pdq, seasonal_pdq):

    # p = d = q = range(0,2)
    # pdq = list(itertools.product(p,d,q))
    # # 4로 수정해서 기간 넓혀보기
    # seasonal_pdq = [(x[0], x[1], x[2], 12) for x in pdq]

    counter = 0
    myDict = {}

    # train = train_df["log"] # tmp
    # train.index = train_df["Month"] # tmp
    # eval_metric ="aic" # tmp
    for param in pdq :
        for param_seasonal in seasonal_pdq:
            try :
                # param = pdq[3] # tmp
                # param_seasonal = seasonal_pdq[3] # tmp
                counter += 1
                mod = sm.tsa.SARIMAX(train,
                                     order=param,
                                     seasonal_order=param_seasonal,
                                     enforce_stationarity=False,
                                     enforce_invertibility=False)
                result = mod.fit()
                myDict[counter] = [result.aic, result.bic, param, param_seasonal]

            except:
                continue
    dict_to_df = pd.DataFrame.from_dict(myDict, orient="index")

    if eval_metric =="aic":
        best_run = dict_to_df[dict_to_df[0] == dict_to_df[0].min()].index.values
        best_run = best_run[0]
    elif eval_metric == "bic":
        best_run = dict_to_df[dict_to_df[1] == dict_to_df[1].min()].index.values
        best_run = best_run[0]

    model = sm.tsa.SARIMAX(train,
                           order=myDict[best_run][2],
                           seasonal_order=myDict[best_run][3],
                           enforce_stationarity=False,
                           enforce_invertibility=False).fit()

    best_model = {"model" : model,
                  "aic" : model.aic,
                  "bic" : model.bic,
                  "order" : myDict[best_run][2],
                  "seasonal_order" : myDict[best_run][3]}

    return myDict, best_model

# train = train_df["log"]

eval_metric = "aic"
# p = d = q = range(0,2)
p = range(0,4)
d = range(1,2)
q = range(0,4)
pdq = list(itertools.product(p,d,q))
seasonal_pdq = [(x[0], x[1], x[2], 12) for x in pdq]

# p = range(0,5)
# d = range(0,1)
# q = range(0,5)
# a = list(itertools.product(p,d,q))
# seasonal_pdq = [(x[0], x[1], x[2], 4) for x in a]
train_df_log = np.log(train_df)
test_df_log = np.log(test_df)

# run code
myDict, best = find_best_sarima(train_df, eval_metric, pdq, seasonal_pdq)
best
myDict

aic_df = pd.DataFrame.from_dict(myDict, orient="index")
aic_df.columns = ["aic", "bic", "order", "s_order"]
aic_df["aic"].plot()
aic_df2 = aic_df[aic_df["aic"] < 335]
aic_df2["aic"].plot()

dir(best["model"])
best["model"].summary()
best["model"].plot_diagnostics()
(2,1,0,1,1,0)




m = tsa.SARIMAX(train_df_log,order=(1,1,1),seasonal_order=(1,1,1,12)).fit()
m.summary()
m.plot_diagnostics()

train_df_log
model_df = train_df_log.copy()
model_df["yhat"] = m.fittedvalues
model_df = model_df.iloc[1:,:]
model_df.iloc[:,:].plot()

m.fittedvalues
m_test_df = test_df_log.copy()

m_test_df["yhat"] = m.predict(start=test_df_log.index[0], end=test_df_log.index[-1])
m_test_df["resid"] = m_test_df["passengers"]-m_test_df["yhat"]
m_test_df["resid"].plot()
m_test_df.iloc[:,:2].plot()

m.predict(start=test_df_log.index[0], end=test_df_log.index[10])
m.fittedvalues
m.forecast(10)


######################################
# rolling window
df_log = np.log(df)
def rolling_window(s,w,n,df):
    """
    s : start num
    w : window size
    n : predict number
    """

    pred_df = pd.DataFrame(columns=["passengers"])
    for i in range(s,s+n) :
        print(i, " / " , s+n)
        train_df = df[i:i+w]
        if train_df.__len__() < w:
            df = df.append(pred_df.iloc[-1])
            train_df = df[i:i + w]

        m = tsa.SARIMAX(train_df,
                        order=(1,1,1),seasonal_order=(1,1,1,12),
                        enforce_stationarity=False, enforce_invertibility=False).fit()
        forecast_1 = pd.DataFrame({"passengers" : m.forecast(steps=1)})
        pred_df = pd.concat([pred_df,forecast_1], axis=0)

    return pred_df

pred_df = rolling_window(0,90,50,df_log)

# 시각화
fig = plt.figure(figsize=(15,5))
ax = plt.subplot()
ax.plot(pred_df)
ax.plot(df_log, color="red")


plt.subplot
help(plt.subplot)
ax1=plt.subplot()
ax2 = ax1.
df_merge = pd.merge(df_log, pred_df, left_index=True, right_index=True)
df_merge.columns = ["y", "yhat"]
df_merge["resid"] = df_merge["y"] - df_merge["yhat"]
df_merge[["y", "yhat"]].plot()
mse = pow(df_merge["resid"],2).sum()/df_merge["resid"].__len__()
rmse = np.sqrt(pow(df_merge["resid"],2).sum()/df_merge["resid"].__len__())

df_merge["resid"]
df_merge["x"] = np.exp(df_merge.iloc[:,0])
df_merge["xhat"] = np.exp(df_merge.iloc[:,1])
df_merge["x_resid"] = df_merge["x"] - df_merge["xhat"]
tsa.adfuller(df_merge["resid"])
df_merge["resid"].plot()
tsa.graphics.plot_acf(df_merge["resid"])
tsa.graphics.plot_pacf(df_merge["resid"])


# prediction
pred = best["model"].predict(start=test_df.index[0], end=test_df.index[-1], dynamic= True)
plt.figure(figsize=(22,10))
plt.plot(train_df.index, train_df, label="Train")
plt.plot(pred.index, pred, label="SARIMA", color="r")
plt.plot(test_df.index, test_df, label="Test", color="k")
plt.legend(loc="best", fontsize="xx-large")
plt.show()








