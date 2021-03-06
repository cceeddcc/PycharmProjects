"""

doc : https://pandas.pydata.org/pandas-docs/stable/

navigator
# Theme  : ...
# Package : ...
# Module : ...
# Class : ...
# Method : ...
# : comments / examples

"""


import numpy as np
import pandas as pd

## Series
"""
1차원 벡터 생성 메서드
"""

# ex) List 데이터를 넘겨주면 자동으로 integer로 indexing
s = pd.Series([1, 3, 5, np.nan, 6, 8])
s

## Dataframe
"""
2차원 Dataframe 생성 메서드
"""

# ex) NumPy array를 넘겨서 Dataframe 생성
dates = pd.date_range('20130101', periods=6) # 인덱스용 날짜 생성
dates
df = pd.DataFrame(np.random.randn(6, 4), index=dates, columns=list('ABCD'))
df

# ex) dict 객체를 넘겨서 Dataframe 생성
df2 = pd.DataFrame({'A': 1.,
                    'B': pd.Timestamp('20130102'), # timestamp 반환
                    'C': pd.Series(1, index=list(range(4)), dtype='float32'),
                    'D': np.array([3] * 4, dtype='int32'),
                    'E': pd.Categorical(["test", "train", "test", "train"]), # 범주형 객체 생성
                    'F': 'foo'})
df2

## Dataframe.dtypes
"""
Dataframe 객체의 데이터 타입 속성
"""
df2.dtypes # 각 열은 서로 다른 데이터 타입을 가질 수 있음

## pandas.Categorical(values, categories=None, ordered=None, dtype=None, fastpath=False)
"""
범주형 객체 생성 메서드
values : 인풋 데이터
categories : 범주 지정 (범주에 없는 데이터는 NaN처리)
ordered : 서열 지정 (min, max 비교 가능)
"""
pd.Categorical([1, 2, 3, 1, 2, 3])
pd.Categorical(['a', 'b', 'c', 'a', 'b', 'c'])
pd.Categorical(['a', 'b', 'c', 'a', 'b', 'c'], ordered=True, categories=['b', 'a']) # 범주에 없는 데이터는 NaN처리

df = pd.DataFrame({"id": [1, 2, 3, 4, 5, 6],"raw_grade": ['a', 'b', 'b', 'a', 'a', 'e']})
df["grade"] = df["raw_grade"].astype("category") # 범주형 변수 열 추가
df["grade"]
df["grade"].cat.categories = ["very good", "good", "very bad"] # 범주형 변수명 재설정
df["grade"]

df["grade"] = df["grade"].cat.set_categories(["very bad", "bad", "medium","good", "very good"]) # 범주형 변수에 서열 지정
df["grade"]
df.sort_values(by="grade") # 서열이 지정됐기 때문에 순서 정렬 가능
df.groupby("grade").size() # 빈 카테고리도 확인가능

#### Viewing data
"""
데이터 특징 보기
"""

# Method : Dataframe.head()
df.head() # 상위 5개

## Dataframe.tail()
df.tail(3) # 하위 3개

## Dataframe.index
df.index # index 보기

# Attribute : Dataframe.shape
df.shape # dimension

# Attribute :  Dataframe.columns
df.columns # 칼럼명 보기

## Dataframe.describe()
df.describe() # 열 별로 간단한 통계 데이터 확인

## Dataframe.to_numpy()
df2.to_numpy() # dataframe 객체를 numpy 객체로 변환

## Dataframe.T
"""
Transpose
"""
df.T # 행과 열 바꾸기

## Dataframe.sort_index()
"""
인덱스 기준으로 정렬
"""
df.sort_index(axis=1, ascending=False) # 내림차순 정렬

## Dataframe.sort_values()
"""
특정 열 기준으로 정렬
"""
df.sort_values(by='B') # B열을 기준으로 오름차순 정렬

#### Getting data
"""
Dataframe 객체 다루기, 선택, 추출, 슬라이스
"""
df["A"] # 열 이름으로 데이터 선택
df.loc[dates[0]] # 행 이름으로 데이터 선택
df[0:3] # 행 슬라이스 0,1,2행 선택
df['20130102':'20130104'] # 행 이름으로 선택 가능

## Dataframe.loc
## Dataframe.at
"""
Dataframe 객체 슬라이스, 선택, 추출
"""
df.loc[:, ['A', 'B']] # [행, 열] 형태로 선택
df.loc['20130102':'20130104', ['A', 'B']] # [행, 열] 형태로 일부분 선택
df.at[dates[0], 'A'] # 데이터 위치 지정해서 바로 선택

## Dataframe.iloc
## Dataframe.iat
"""
정수(integer) 값으로 데이터 슬라이스, 선택, 추출
"""
df.iloc[3] # integer 값으로 데이터 바로 선택
df.iloc[3:5, 0:2] # [3~4행, 0~1열] 일부분 선택
df.iloc[[1, 2, 4], [0, 2]]
df.iloc[1:3, :]
df.iloc[:, 1:3]
df.iat[1, 1] # 데이터 위치 지정해서 바로 선택

## 조건으로 데이터 추출
df[df.A > 0] # A열 값이 0보다 큰 데이터만 추출
df[df > 0] # 각 값이 0보다 큰값만 추출하고, 조건을 만족하지 않으면 NaN지정

## Dataframe.copy()
"""
Dataframe객체 복사 
"""
df2 = df.copy() # df를 복사해서 df2객체 생성

## Dataframe.isin()
"""
특정 데이터가 있는지 확인 -> 각 열에 boolean으로 반환 -> 데이터 필터링 가능
"""
df2['E'] = ['one', 'one', 'two', 'three', 'four', 'three']
df2['E'].isin(['two', 'four']) # "해당 데이터가 있는지 boolean 반환
df2[df2['E'].isin(['two', 'four'])] # 이와같은 형태로 필터링 가능

#### Setting data
"""
데이터 지정, 할당
"""
s1 = pd.Series([1, 2, 3, 4, 5, 6], index=pd.date_range('20130102', periods=6))
s1
df['F'] = s1 # 인덱스에 없는 데이터는 NaN으로 자동 삽입
df.at[dates[0], 'A'] = 0
df.iat[0, 1] = 0
df.loc[:, 'D'] = np.array([5] * len(df))
df

df2 = df.copy() # 객체 복사
df2[df2 > 0] = -df2 # 조건식 활용한 데이터 할당
df2

# Method : pd.DataFrame.drop()
"""
Remove rows or columns by specifying label names and corresponding
axis, or by specifying directly index or column names
"""
help(pd.DataFrame.drop)
df = pd.DataFrame(np.arange(12).reshape(3, 4),columns=['A', 'B', 'C', 'D'])
df.drop(columns=['B', 'C'], axis=1)
df.drop(index=[0, 1])


#### Missing data
"""
NaN, Na 등 missing data 처리
"""

## Dataframe.dropna()
"""
missing data를 갖고 있는 행은 모두 drop
"""
df1 = pd.DataFrame({"A" : [1,np.NaN,np.NaN,2]})
df1.dropna(how='any') # missing data를 갖고 있는 행은 모두 drop

## Dataframe.fillna()
"""
missing data를 다른 값으로 채워줌
"""
df1.fillna(value=5) # NaN 값을 해당 value로 바꿔줌
df1.fillna(method="pad") # missing data를 forward 방식(가장 가까운 낮은 index의 값을 가지고) 유효한 값 채움
df1.fillna(method="bfill") # missing data를 backward 방식(가장 가까운 높은 index의 값을 가지고) 유효한 값 채움

## Dataframe.isna()
"""
Dataframe value에 대해 missing data가 있는지 검정 -> boolean 반환
"""
df1.isna() # NaN값에 대해 T/F 검정

# Method : Dataframe.isnull()
"""
Dataframe value에 대해 missing data가 있는지 검정 -> boolean 반환
"""
df1.isnull().sum() # nan 값 개수 체크

## DataFrame.reindex(self, labels=None, index=None, columns=None, axis=None, method=None, copy=True, level=None, fill_value=nan, limit=None, tolerance=None)
"""
새로운 인덱스를 지정할 수 있다.
기존 인덱스에 없는 새로운 인덱스의 값들은 기본으로 NaN으로 지정됨
fill_value : missing value를 NaN 값 대신 다른 값으로 지정
columns : 칼럼도 reindex 지정 가능 
axis : 축 지정 (예제확인)
"""
index = ['Firefox', 'Chrome', 'Safari', 'IE10', 'Konqueror']
df = pd.DataFrame({'http_status': [200,200,404,404,301],
                   'response_time': [0.04, 0.02, 0.07, 0.08, 1.0]},
                  index=index); df
new_index= ['Safari', 'Iceweasel', 'Comodo Dragon', 'IE10','Chrome']
df.reindex(new_index) # NaN값이 기본으로 채워짐
df.reindex(new_index, fill_value=0) # missing value는 0으로 채움
df.reindex(new_index, fill_value='missing')
df.reindex(columns=['http_status', 'user_agent']) # colums도 reindex 가능
df.reindex(['http_status', 'user_agent'], axis="columns") # axis로 축 지정
df.reindex(['Safari', 'Chrome'], axis="rows")

# ex) index를 날짜로 사용하는데 기간을 늘리고 싶은경우 활용
date_index = pd.date_range('1/1/2010', periods=6, freq='D')
df2 = pd.DataFrame({"prices": [999, 101, np.nan, 100, 89, 88]},index=date_index); df2
date_index2 = pd.date_range('12/29/2009', periods=10, freq='D') # 기간확장
df2.reindex(date_index2)
df2.reindex(date_index2, method='bfill') # missing data에 가장 이전의 유효한 값을 넣음 back fill


#### Operations
"""
기본적으로 missing data는 제외하고 계산, 함수 등 수행 
"""

## 통계 메서드
df.mean()
df.mean(1) # 열 지정해서 통계량 구할 수 있음

## DataFrame.shift(self, periods=1, freq=None, axis=0, fill_value=None)
"""
데이터를 앞, 뒤 방향으로 이동시키는 메서드
이동해서 생기는 missing data는 NaN처리 
"""
df = pd.DataFrame({'Col1': [10, 20, 15, 30, 45],
                   'Col2': [13, 23, 18, 33, 48],
                   'Col3': [17, 27, 22, 37, 52]}) ;df

df.shift(periods=3) # 행 기준으로 3칸 이동
df.shift(periods=1, axis='columns') # 열 기준으로 1칸 이동
df.shift(periods=3, fill_value=0) # missing value 지정

## DataFrame.sub(self, other, axis='columns', level=None, fill_value=None)
"""
Dataframe data 뺄셈, 빼기(subtract) 메서드
DataFrame 객체의 각 데이터의 뺄셈 실행
add, sub, mul, div, truediv, floordiv, mod, pow 모두 사용법 동일 
"""
df = pd.DataFrame({'angles': [0, 3, 4],
                   'degrees': [360, 180, 360]},
                  index=['circle', 'triangle', 'rectangle']) ;df
df + 1 # 모든 데이터에 적용
df.add(1) # 위와 동일
df.div(10) # 나눗셈, 나누기
df - [1, 2] # 각 열 별로 적용
df.sub([1, 2], axis='columns') # 나눗셈, 나누기
df.sub(pd.Series([1, 1, 1], index=['circle', 'triangle', 'rectangle']),axis='index') # Series객체 사용
other = pd.DataFrame({'angles': [0, 3, 4]}, index=['circle', 'triangle', 'rectangle']); other
df * other # 곱셈, 곱하기
df.mul(other, fill_value=0) # 곱셈, 곱하기

## multi index
"""
Dataframe의 인덱스를 여러개로 사용할 수 있다.
"""
df_multindex = pd.DataFrame({'angles': [0, 3, 4, 4, 5, 6],
                             'degrees': [360, 180, 360, 360, 540, 720]},
                            index=[['A', 'A', 'A', 'B', 'B', 'B'], ['circle', 'triangle', 'rectangle', 'square', 'pentagon', 'hexagon']])
df_multindex
df.div(df_multindex, level=1, fill_value=0)

## Dataframe.apply()
"""
Dataframe객체에 특정 함수 적용
"""
df = pd.DataFrame({'angles': [0, 3, 4],
                   'degrees': [360, 180, 360]},
                  index=['circle', 'triangle', 'rectangle']) ;df
df.apply(np.cumsum) # 누적합 함수 적용
df.apply(lambda x: x.max() - x.min()) # 사용자 생성함수 적용

## pd.str.lower()
"""
string 데이터에 적용하는 함수
글자를 소문자로 변환 
"""
s = pd.Series(['A', 'B', 'C', 'Aaba', 'Baca', np.nan, 'CABA', 'dog', 'cat']);s
s.str.lower() # 글자 소문자 변환

# Method : Series.value_counts()
"""
중복데이터 개수 세기
히스토그램 그리기와 동일한 개념 
"""
s = pd.Series(np.random.randint(0, 7, size=10));s # 지정 숫자 사이의 정수를 같은 동일확률(일양분포)로 random 추출
s.value_counts() # value 개수 세기 (series형 객체 에서만 사용 가능)

## DataFrame.merge(self, right, how='inner', on=None, left_on=None, right_on=None, left_index=False, right_index=False, sort=False, suffixes=('_x', '_y'), copy=True, indicator=False, validate=None)
"""
데이터프레임 합치기
"""
df1 = pd.DataFrame({
    '고객번호': [1001, 1002, 1003, 1004, 1005, 1006, 1007],
    '이름': ['둘리', '도우너', '또치', '길동', '희동', '마이콜', '영희']
}) ; df1

df2 = pd.DataFrame({
    '고객번호': [1001, 1001, 1005, 1006, 1008, 1001],
    '금액': [10000, 20000, 15000, 5000, 100000, 30000]
}) ; df2

pd.merge(df1, df2) # 공통된 열을 기준으로 inner join이 기본값
"""
inner join : 양쪽 데이터 프레임에 모두 키가 종재하는 데이터만 보여줌
"""
pd.merge(df1, df2, how='outer') # outer join (상대방에 없는 값이면 NaN)
pd.merge(df1, df2, how='left') # df1을 기준으로 지정
pd.merge(df1, df2, how='right') # df2를 기준으로 지정

df1 = pd.DataFrame({
    '고객명': ['춘향', '춘향', '몽룡'],
    '날짜': ['2018-01-01', '2018-01-02', '2018-01-01'],
    '데이터': ['20000', '30000', '100000']}) ; df1
df2 = pd.DataFrame({
    '고객명': ['춘향', '몽룡'],
    '데이터': ['여자', '남자']}) ; df2
pd.merge(df1, df2, on='고객명') # 기준 Key(열) 지정

left = pd.DataFrame({'key': ['foo', 'foo'], 'lval': [1, 2]}) ;left
right = pd.DataFrame({'key': ['foo', 'foo'], 'rval': [4, 5]}) ;right
pd.merge(left, right, on='key') # key열을 기준으로 데이터 합치기

## DataFrame.concat()
"""
Dataframe 객체를 단순 이어붙이는 메서드
"""
df = pd.DataFrame(np.random.randn(10, 4)) ; df # 10행 4열 DataFrame객체 생성
pieces = [df[:3], df[3:7], df[7:]] # list객체 생성
pd.concat(pieces) # 이어 붙이는 기능

## DataFrame.transpose(self, *args, **kwargs)
"""
행과 열 방향 바꾸기 Transpose
"""
d2 = {'name': ['Alice', 'Bob'],
      'score': [9.5, 8],
      'employed': [False, True],
      'kids': [0, 0]}
df2 = pd.DataFrame(data=d2)
df2
df2_transposed = df2.T # or df2.transpose()
df2_transposed

## DataFrame.corr()
"""
DataFrame객체 각 열 별로 correlation matrix 생성
"""
df = pd.DataFrame(np.random.randn(10, 4), columns=list("ABCD")) ; df
df.corr()

df = pd.DataFrame({"A" : [1,2,3,4,5,6,7],
                   "B" : [7,6,5,4,3,2,1],
                   "C" : [np.NaN,np.NaN,1,2,3,4,5]})
df.corr() # NaN값으로 열마다 데이터 개수가 달라도 서로 있는 데이터끼리 계산해줌

## DataFrame.cov()
"""
DataFrame의 각 열 별로 covariance matrix 생성
"""
df = pd.DataFrame(np.random.randn(10, 4), columns=list("ABCD")) ; df
df.cov()

## DataFrame.append()
"""
Dataframe 객체에 행추가 메서드
insert row 
"""
df = pd.DataFrame(np.random.randn(8, 4), columns=['A', 'B', 'C', 'D']) ; df
s = df.iloc[3] ; s
df.append(s, ignore_index=True) # 가장 아래에 행추가


#### Grouping
"""
Data를 특정 기준으로 Group으로 만들기 
"""

## DataFrame.groupby()
"""
특정 열의 범주형 데이터 기준으로 묶어서 각각 계산을 수행하는 메서드
"""
df = pd.DataFrame({'A': ['foo', 'bar', 'foo', 'bar', 'foo', 'bar', 'foo', 'foo'],
                   'B': ['one', 'one', 'two', 'three', 'two', 'two', 'one', 'three'],
                   'C': np.random.randn(8),
                   'D': np.random.randn(8)})
df
df.groupby('A').sum() # A열의 데이터를 기준으로 묶어서 각각 계산수행
df.groupby(['A', 'B']).sum() # 기준을 여러 개 지정 가능 - multi index


## Pandas.MultiIndex.from_tuples(tuples, sortorder=None, names=None)
"""
tuple로 구성된 list에서 다중인덱스로 변환
"""
tuples = [(1, 'red'), (1, 'blue'),(2, 'red'), (2, 'blue')]
tuples = list(zip([1]*2 + [2]*2,['red','blue'] *2)) # 상동 (zip 활용)
pd.MultiIndex.from_tuples(tuples, names=('number', 'color'))

tuples = list(zip(*[['bar', 'bar', 'baz', 'baz', 'foo', 'foo', 'qux', 'qux'],
                    ['one', 'two', 'one', 'two', 'one', 'two', 'one', 'two']])) # zip : iterable한 객체를 하나씩 묶어주는 내장함수
index = pd.MultiIndex.from_tuples(tuples, names=['first', 'second']) # index 객체 생성
df = pd.DataFrame(np.random.randn(8, 2), index=index, columns=['A', 'B']) # DataFrame 객체 생성
df2 = df[:4] ; df2

## DataFrame.stack()
## DataFrame.unstack()
"""
행과 열 인덱스들을 서로 변환하는 메서드
"""
stacked = df2.stack() # columns index를 rows index로 변환하여 쌓기
stacked
stacked.unstack() # 가장 최근에 stack된 index를 다시 columns 인덱스로 변환
stacked.unstack(1) # 변환하고자 하는 index의 열(0,1,2 중에 1번째 열)을 지정 가능
stacked.unstack(0)

## Pandas.Pivot tables()
"""
DataFrame객체를 row index, column index를 지정하여 피벗테이블로 생성 
"""
df = pd.DataFrame({'A': ['one', 'one', 'two', 'three'] * 3,
                   'B': ['A', 'B', 'C'] * 4,
                   'C': ['foo', 'foo', 'foo', 'bar', 'bar', 'bar'] * 2,
                   'D': np.random.randn(12),
                   'E': np.random.randn(12)})
df
pd.pivot_table(df, values='D', index=['A', 'B'], columns=['C'])

## Pandas.date_range()
"""
날짜 데이터 생성 메서드
특정 기간, 주기 등을 지정해서 날짜 인덱스를 만들 수 있다. 
"""
rng = pd.date_range('1/1/2012', periods=100, freq='S')
ts = pd.Series(np.random.randint(0, 500, len(rng)), index=rng) ;ts
ts.resample('5S').sum() # 주기를 변경해서 다시 생성

rng = pd.date_range('3/6/2012 00:00', periods=5, freq='D')
ts = pd.Series(np.random.randn(len(rng)), rng) ;ts
ts.resample('5Min').sum() # 주기를 변경해서 다시 생성

pd.date_range(start="19490101", end="19601201", freq="MS", closed=None) # MS

# Method : pd.DataFrame.sample()
"""
Return a random sample of items from an axis of object
use to split the data into train and test
"""
help(pd.DataFrame.sample)
df = pd.DataFrame({'num_legs': [2, 4, 8, 0],
                   'num_wings': [2, 0, 0, 0],
                   'num_specimen_seen': [10, 2, 1, 8]},
                  index=['falcon', 'dog', 'spider', 'fish']); df
df.sample(frac=0.5, replace=False, random_state=1) # 50% samples
df.sample(n=3, replace=True) # 3 samples



## DataFrame.tz_localize(self, tz, axis=0, level=None, copy=True, ambiguous='raise', nonexistent='raise')
"""
시간 데이터를 현지화 시킴
"""
s = pd.Series([1],index=pd.DatetimeIndex(['2018-09-15 01:30:00']))
s.tz_localize('CET') # 중부유럽 표준시

ts_utc = ts.tz_localize('UTC')
ts_utc

ts_utc.tz_convert('US/Eastern') # time zone convert

## DataFrame.to_period(self, freq=None, axis=0, copy=True)
"""
Datetime 인덱스를 Period 인덱스로 변환
"""
rng = pd.date_range('1/1/2012', periods=5, freq='M')
ts = pd.Series(np.random.randn(len(rng)), index=rng); ts
ps = ts.to_period() ;ps # 월단위로 period index로 변환
ps.index # dtype이 period[M]
ts.index # dtype이 datetime

## DataFrame.to_timestamp(self, freq=None, how='start', axis=0, copy=True)
"""
해당기간의 처음날짜로 index 변환
"""
ps.to_timestamp() # 해당 기간의 첫날짜로 모두 변환
ps.to_timestamp().index # dtype이 datetime


## PeriodIndex.asfreq(self, *args, **kwargs)
"""
Period Array/Index를 특정 frequency의 데이터로 변환 
E : END , S : START를 의미 
"""
pidx = pd.period_range('2010-01-01', '2015-01-01', freq='A') ; pidx # 연간 Preriod index
pidx.asfreq('M') # 월단위
pidx.asfreq('M', how='S') # Start

prng = pd.period_range('1990Q1', '2000Q4', freq='Q-NOV') ;prng # 쿼터 데이터 생성 (11월을 4쿼터로 지정한 것임)
type(prng)
ts = pd.Series(np.random.randn(len(prng)), prng);ts
ts.index = (prng.asfreq('M', 'e') + 1).asfreq('H', 's') + 9 # 월단위(end)로 변환 후 시간단위(start)로 변환, 숫자 계산으로 편리하게 계산
ts.head()

## DataFrame.plot()
"""
Dataframe객체 plotting, 그래프 그리기 
"""
ts = pd.Series(np.random.randn(1000),index=pd.date_range('1/1/2000', periods=1000))
ts = ts.cumsum()
ts.plot() # 그래프 그리기

df = pd.DataFrame(np.random.randn(1000, 4), index=ts.index, columns=['A', 'B', 'C', 'D'])
df = df.cumsum()
df.plot() # 모든 열의 데이터 plotting
plt.legend(loc='best') # 범례표시

s = pd.Series(np.random.random_integers(0, 7, size=200));s
s = s.value_counts()
s.plot(kind="bar") # bar chart

#### Getting data in/out
"""
Dataframe 데이터 저장하기 
"""

## DataFrame.to_csv()
## DataFrame.read_csv()
"""
csv 파일로 저장 및 불러오기, 읽기
"""
df.to_csv('foo.csv') # csv 파일 쓰기
pd.read_csv('foo.csv', encoding="euc-kr") # csv 파일 읽기, 한국어가 들어간 파일은 인코딩 필수

## DataFrame.to_excel()
## DataFrame.read_excel()
"""
Excel 파일로 저장 및 불러오기, 읽기
"""
df.to_excel('foo.xlsx', sheet_name='Sheet1') # Excel 쓰기
pd.read_excel('foo.xlsx', 'Sheet1', index_col=None, na_values=['NA']) # Excel 읽기


## DataFrame.ExcelWriter()
"""
Excel 여러 sheet에 저장시키는 메서드
"""
df1 = pd.DataFrame([['a', 'b'],
                    ['c', 'd']],
                   index=['row 1', 'row 2'],
                   columns=['col 1', 'col 2'])

df1.to_excel("C:/Users/S/Desktop/output.xlsx",
             sheet_name='Sheet_name_1') # sheet 이름 지정

df2 = df1.copy()
with pd.ExcelWriter('output.xlsx') as writer: # engine이 필요한 경우 engine="xlsxwriter"
    df1.to_excel(writer, sheet_name='Sheet_name_1')
    df2.to_excel(writer, sheet_name='Sheet_name_2')

with pd.ExcelWriter('output.xlsx', mode='a') as writer: # append 모드
    df.to_excel(writer, sheet_name='Sheet_name_3')


### Pandas_datareader
"""
야후, 구글에서 데이터 주식 데이터 파싱하는 모듈
"""

## Pandas_datareader.data.DataReader()
"""
야후, 구글에서 데이터 주식 데이터 파싱하는 메서드
"""
import pandas_datareader.data as web
start = '2000-02-19'
end = '2016-03-04'
gs = web.DataReader("078930.KS", "yahoo", start, end) # 날짜 지정안하면 최근 5개년치 데이터 불러옴
gs  # gs 종목의 데이터를 DataFrame 형태로 가져옴
gs.info() # DataFrame 정보 확인

import matplotlib.pyplot as plt
plt.plot(gs['Adj Close']) # 그래프로 표현
plt.show()
pd.DataFrame


## DataFrame.rolling(self, window, min_periods=None, center=False, win_type=None, on=None, axis=0, closed=None)
"""
갯수지정해서 묶어주는 역할 rolling type 데이터 생성후, 함수사용해서 이동평균선처럼 동적인 계산가능
"""
df = pd.DataFrame({'B': [0, 1, 2, np.nan, 4]}); df
df.rolling(2).sum()
df.rolling(2, min_periods=1).sum() # window의 최소 단위 지정

gs["Adj Close"]
rollingdata = gs["Adj Close"].rolling(window=3) # 1,2,3 번째 값을 묶어서 3번째 값 자리에 값을 제시
type(rollingdata) # rolling type 데이터
rollingdata.sum()

ma5 = gs['Adj Close'].rolling(window=5).mean() # 5개 지정, 이동평균선
ma5.tail(10)

## DataFrame.insert(self, loc, column, value, allow_duplicates=False)
"""
특정위치에 열 추가
"""
gs.insert(len(gs.columns),"MA5",ma5) # (열 순서, 열 이름, 데이터)
gs.head()

# Method : pd.DataFrame.diff()
"""
Calculates the difference of a DataFrame element compared with another
element in the DataFrame (default is the element in the same column
of the previous row).    
"""
help(pd.DataFrame.diff)
df = pd.DataFrame({'a': [1, 2, 3, 4, 5, 6], 'b': [1, 1, 2, 3, 5, 8], 'c': [1, 4, 9, 16, 25, 36]})
df.diff(periods=3)
df-df.shift(3) # 상동
