import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm
import scipy.stats as stats

# Method : norm.pdf()
"""
Probability Density function
"""
# ex) 표준정규분포 그리기
mu = 0
sigma = 1
density = pd.DataFrame()

density['x'] = np.arange(-4, 4, 0.01)
density['pdf'] = norm.pdf(density['x'], mu, sigma)
plt.plot(density['x'], density['pdf'], color='red')

# Method : norm.cdf()
"""
Cumulative function
"""
mu = 0
sigma = 1
norm.cdf(1.96, mu, sigma)

# Method : norm.ppf()
"""
Quantile function
Q(prob) = critical value 
"""
mu = 0
sigma = 1
norm.ppf(0.05, mu, sigma)

VaR = norm.ppf(0.05, mu, sigma) # Percent point function (inverse of `cdf`)

# Method : stats.probplot()
"""
QQ-plot, QQ-line
"""
z = np.random.normal(10,4,100)
stats.probplot(z, dist="norm", plot=plt)