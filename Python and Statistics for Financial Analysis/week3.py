import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pandas_datareader.data as datareader
from scipy.stats import norm

# Population
population = pd.DataFrame(np.random.rand(1000))
pop_mean = population[0].mean()
pop_std = population[0].std(ddof=0)

# LLN test
"""
sample_Size는 일정수준 (n>=30)보다만 크면 다 똑같음
결국 sample trial이 증가함에 따라 수렴함  
"""
df_LLN = pd.DataFrame()
for sam_size in [5,10,50,100,500] :
    LLN = []
    sample_mean = []
    for trial in range(1000):
        sample_mean.append(population.sample(sam_size, replace=False)[0].mean())
        LLN.append(pd.Series(sample_mean).mean())
    df_LLN["LLN_%s" %str(sam_size),] = LLN

df_LLN
df_LLN.iloc[:,0].plot()
df_LLN.iloc[:,1].plot()
df_LLN.iloc[:,2].plot()
df_LLN.iloc[:,3].plot()
df_LLN.iloc[:,4].plot()
plt.legend()
plt.axhline(pop_mean)

# LLN sample size와 관계
"""
결과적으로 sample size가 일정 수준 이상 가면 별로 차이없다. 
"""
# Population
population = pd.DataFrame(np.random.rand(1000))
pop_mean = population[0].mean()
pop_std = population[0].std(ddof=0)

# LLN
df_LLN = pd.DataFrame()
LLN_num=[]
for sam_size in range(1,500) :
    sample_mean = []
    LLN = []

    for trial in range(200):
        sample_mean.append(population.sample(sam_size, replace=False)[0].mean())
        LLN.append(pd.Series(sample_mean).mean())
    LLN_num.append(LLN[-1])
df_LLN["LLN"] = LLN_num
df_LLN["LLN"].plot()
plt.axhline(pop_mean)


# CLT
"""
sample_size (n) 의 증가로 인한 효과 확인 
"""
# population
population = pd.DataFrame(np.random.rand(5000))
pop_mean = population[0].mean()
pop_std = population[0].std(ddof=0)

# sample mean(x_bar)이 n증가에 따라 정규분포에 수렴하는가 ?
# sampling
sample_mean_df = pd.DataFrame()
sample_std_df = pd.DataFrame()
for sample_size in [10,50,100,300] :
    sample_mean_list = []
    sample_std_list = []

    for t in range(2000) : # sampling trials
        sample_data = population.sample(sample_size,replace=False)
        sample_mean_list.append(sample_data[0].mean())
        sample_std_list.append(sample_data[0].std(ddof=1))

    sample_mean_df["X_bar_%s" %str(sample_size)] = sample_mean_list
    sample_std_df["sigma_%s" %str(sample_size)] = sample_std_list

# n증가에 따라 표준편차 감소
sample_mean_df
sample_mean_df.iloc[:,0].hist(bins=200)
sample_mean_df.iloc[:,1].hist(bins=200)
sample_mean_df.iloc[:,2].hist(bins=200)
sample_mean_df.iloc[:,3].hist(bins=200)

sample_std_df.iloc[:,0].hist(bins=200)
sample_std_df.iloc[:,1].hist(bins=200)
sample_std_df.iloc[:,2].hist(bins=200)
sample_std_df.iloc[:,3].hist(bins=200)

#높은 trial횟수로 pop mean, pop_std에 가까움
pop_mean
sample_mean_df.iloc[:,0].mean() - pop_mean
sample_mean_df.iloc[:,1].mean() - pop_mean
sample_mean_df.iloc[:,2].mean() - pop_mean
sample_mean_df.iloc[:,3].mean() - pop_mean

pop_std
sample_std_df.iloc[:,0].mean()
sample_std_df.iloc[:,1].mean()
sample_std_df.iloc[:,2].mean()
sample_std_df.iloc[:,3].mean()


# 모두 정규분포를 따르는 것을 확인할 수 있음
import scipy
scipy.stats.jarque_bera(sample_mean_df.iloc[:,0])
scipy.stats.jarque_bera(sample_mean_df.iloc[:,1])
scipy.stats.jarque_bera(sample_mean_df.iloc[:,2])
scipy.stats.jarque_bera(sample_mean_df.iloc[:,3])

# sample_mean의 std가 sigma/n**0.5와 일치하는 것 확인
(pop_std/10**0.5,sample_mean_df.iloc[:,0].std())
(pop_std/50**0.5,sample_mean_df.iloc[:,1].std())
(pop_std/100**0.5,sample_mean_df.iloc[:,2].std())
(pop_std/300**0.5,sample_mean_df.iloc[:,3].std())


# Hypothesis testing
# import microsoft.csv, and add a new feature - logreturn
ms = datareader.DataReader("MSFT","yahoo")
ms['logReturn'] = np.log(ms['Close'].shift(-1)) - np.log(ms['Close'])

# Log return goes up and down during the period
ms['logReturn'].plot(figsize=(20, 8))
plt.axhline(0, color='red')
plt.show()

# Calculate test statistic
sample_mean = ms['logReturn'].mean()
sample_std = ms['logReturn'].std(ddof=1)
n = ms['logReturn'].shape[0]

# if sample size n is large enough, we can use z-distribution, instead of t-distribtuion
# mu = 0 under the null hypothesis
zhat = (sample_mean - 0)/(sample_std/n**0.5)
print(zhat)

# Set desicion criteria
alpha = 0.05
zleft = norm.ppf(alpha/2, 0, 1)
zright = -zleft  # z-distribution is symmetric
print(zleft, zright)

print('At significant level of {}, shall we reject: {}'.format(alpha, zhat>zright or zhat<zleft))

# p-value
p = 1 - norm.cdf(zhat, 0, 1)
print(p)