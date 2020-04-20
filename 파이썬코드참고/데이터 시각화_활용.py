"""
Python 시각화 라이브러리
1. matplotlib
2. seaborn
3. plotnine
4. folium
5. plot.ly
6. pyecharts
"""

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

# 2. seaborn
"""
seaborn은 matplotlib을 기반으로 다양한 색 테마, 차트 기능을 추가한 라이브러리
matplotlib에 의존성을 가지고 있음
matplotlib에 없는 그래프(히트맵, 카운트플랏 등)을 가지고 있습니다
"""
import seaborn as sns
print("Seaborn version : ", sns.__version__) # 버전 확인
dir(sns) # 사용 가능한 메서드
sns.set(style="whitegrid") # 여러 미적인 parameter setting
# sns.set_color_codes()

current_palette = sns.color_palette() # 사용 가능한 컬러 팔레트
sns.palplot(current_palette) # 컬러 팔레트 시각화

# relational plot 관계형 분포도 그리기
tips = sns.load_dataset("tips") # 예시용 데이터 세트
sns.relplot(x="total_bill", y="tip", hue="smoker", style="smoker",
            data=tips)

df = pd.DataFrame(dict(time=np.arange(500),
                       value=np.random.randn(500).cumsum()))
g = sns.relplot(x="time", y="value", kind="line", data=df)
g.fig.autofmt_xdate()

# cat plot
sns.catplot(x="day", y="total_bill", hue="smoker",
            col="time", aspect=.6,
            kind="swarm", data=tips)

titanic = sns.load_dataset("titanic")
g = sns.catplot(x="fare", y="survived", row="class",
                kind="box", orient="h", height=1.5, aspect=4,
                data=titanic.query("fare > 0"))
g.set(xscale="log");

# pairplot
iris = sns.load_dataset("iris")
sns.pairplot(iris)

g = sns.PairGrid(iris)
g.map_diag(sns.kdeplot)
g.map_offdiag(sns.kdeplot, n_levels=6);

# Heatmap
flights = sns.load_dataset("flights")
flights = flights.pivot("month", "year", "passengers")
plt.figure(figsize=(10, 10))
ax = sns.heatmap(flights, annot=True, fmt="d")

# 3. plotnine
"""
plotnine은 R의 ggplot2에 기반해 그래프를 그려주는 라이브러리입니다
"""

# 4. folium
"""
folium은 지도 데이터(Open Street Map)에 leaflet.js를 이용해 위치정보를 시각화하는 라이브러리입니다
자바스크립트 기반이라 interactive하게 그래프를 그릴 수 있습니다
한국 GeoJSON 데이터는 southkorea-maps에서 확인할 수 있습니다
"""
# pip install folium
import folium
print("folium version is", folium.__version__)

m = folium.Map(location=[37.5502, 126.982], zoom_start=12)
folium.Marker(location=[37.5502, 126.982], popup="Marker A",
             icon=folium.Icon(icon='cloud')).add_to(m)
folium.Marker(location=[37.5411, 127.0107], popup="한남동",
             icon=folium.Icon(color='red')).add_to(m)
m

# 5. plot.ly
"""
plotly는 Interactive 그래프를 그려주는 라이브러리입니다
Scala, R, Python, Javascript, MATLAB 등에서 사용할 수 있습니다
시각화를 위해 D3.js를 사용하고 있습니다
사용해보면 사용이 쉽고, 세련된 느낌을 받습니다
Online과 offline이 따로 존재합니다(온라인시 api key 필요)
plotly cloud라는 유료 모델도 있습니다
"""
# pip install plotly
import plotly
print("plotly version :", plotly.__version__)
plotly.offline.iplot({
"data": [{
    "x": [1, 2, 3],
    "y": [4, 2, 5]
}],
"layout": {
    "title": "hello world"
}
})


import plotly.figure_factory as ff
import plotly.plotly as py
import plotly.graph_objs as go

df = pd.read_csv("https://raw.githubusercontent.com/plotly/datasets/master/school_earnings.csv")

table = ff.create_table(df)
plotly.offline.iplot(table, filename='jupyter-table1')


# 6. pyecharts
"""
Baidu에서 데이터 시각화를 위해 만든 Echarts.js의 파이썬 버전입니다
정말 다양한 그래프들이 내장되어 있어 레포트를 작성할 때 좋습니다!
자바스크립트 기반이기 때문에 Interactive한 그래프를 그려줍니다
"""
pip install pyecharts
import pyecharts
print("pyecharts version : ", pyecharts.__version__)
