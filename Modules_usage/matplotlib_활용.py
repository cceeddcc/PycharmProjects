import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt

# 1. matplotlib
"""
https://matplotlib.org/index.html
"""
print("Matplotlib version", matplotlib.__version__) # 버전확인

# plt.figure
"""
그래프 그리기 전 도화지
"""
plt.figure(figsize=(10,5)) # 그래프 그리기 전 도화지
fig = plt.figure()

fig.suptitle('figure sample plots') # 제목
fig.set_size_inches(10,10) # 가로 10 iniches, 세로 10 inches

# plt.rcParams
"""
Parameter 
"""
plt.rcParams['figure.figsize'] = (10,5) # parameter로 지정해서 넘길 수 있음

# plt.subplots()
"""
(행,열,번호)
도화지 분할 개념
"""
plt.subplot(2,2,1)
plt.hist(pd.DataFrame(np.random.random(100))[0])
plt.subplot(2,2,4)
plt.hist(pd.DataFrame(np.random.random(100))[0])


# Axes
" plot이 그려지는 공간 "
# Axis
" plot의 축 "
fig = plt.figure()
fig, axes_list = plt.subplots(2, 2, figsize=(8,5)) # 각 객체를 변수로 담을 수 있음
# plotting
axes_list[0][0].plot([1,2,3,4], 'ro-')
axes_list[0][1].plot(np.random.randn(4, 10), np.random.randn(4,10), 'bo--')
axes_list[1][0].plot(np.linspace(0.0, 5.0), np.cos(2 * np.pi * np.linspace(0.0, 5.0)))
axes_list[1][1].plot([3,5], [3,5], 'bo:')
axes_list[1][1].plot([3,7], [5,4], 'kx')
plt.show()

df = pd.DataFrame(np.random.randn(4,4))
df.plot(kind='barh')
plt.style.use('ggplot') # ggplot style로 그리기
df.plot(kind='barh')
plt.style.use('default') # 기본값으로 다시 전환  그리기