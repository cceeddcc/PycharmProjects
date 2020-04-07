import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pandas_datareader.data as datareader
from scipy.stats import norm

ms = datareader.DataReader("MSFT","yahoo")
ms.head()

# Distribution of Log return
ms["LogReturn"] = np.log(ms["Adj Close"].shift(-1)) - np.log(ms["Adj Close"])
ms["LogReturn"].head(10)

mu = ms["LogReturn"].mean()
sigma = ms["LogReturn"].std(ddof=1) # sample

density = pd.DataFrame()
density['x'] = np.arange(ms['LogReturn'].min()-0.01, ms['LogReturn'].max()+0.01, 0.001)
density['pdf'] = norm.pdf(density['x'], mu, sigma)

ms['LogReturn'].hist(bins=50, figsize=(15, 8))
plt.plot(density['x'], density['pdf'], color='red')
plt.show()


# Calculate the probability of the stock price will drop
# over a certain percentage in a day
prob_return1 = norm.cdf(-0.05, mu, sigma) # prob of return less than -5%
print('The Probability is ', prob_return1)

prob_return1 = norm.cdf(-.1, mu, sigma)
print('The Probability is ', prob_return1)

# Calculate the probability of the stock price will drop over a certain percentage in a year

# drop over 40% in 220 days
mu220 = 220*mu
sigma220 = np.sqrt(220) * sigma
print('The probability of dropping over 40% in 220 days is ', norm.cdf(-0.4, mu220, sigma220))


# Calculate Value at risk (VaR)
VaR = norm.ppf(0.05, mu, sigma) # Percent point function (inverse of `cdf`)
print('Single day value at risk ', VaR)

# Quatile
# 5% quantile
print('5% quantile ', norm.ppf(0.05, mu, sigma))
# 95% quantile
print('95% quantile ', norm.ppf(0.95, mu, sigma))


