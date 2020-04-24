import numpy as np
""" 
https://numpy.org/devdocs/user/index.html
N차원 array 객체 다루는데 powerful 
numpy는 과학 계산을 위한 라이브러리로서 다차원 배열을 처리하는데 필요한 여러 유용한 기능을 제공
"""

### Array Creation
"""
Numpy Array 생성방법
"""
# 1차원 데이터 Array 생성
a = np.array([2,3,4]) # list형 데이터 넘겨주기
a
a.dtype
b = np.array([1, 3.5, 5.1]) # 모두 같은 데이터 형
b.dtype

# 2차원 데이터 Array 생성
b = np.array([(1.5, 2, 3), (4, 5, 6)])
b

c = np.array([[1, 2], [3, 4]], dtype=complex) # 데이터 타입 지정
c

## zeros(), ones()
"""
0으로 구성된 array 생성
"""
np.zeros((3, 4)) # 3행 4열, 0으로 구성된 array 생성
np.ones((2, 3, 4), dtype=np.int16) # 2개의 3행 4열, 1로만 구성된 3차원 array


## np.random.randn(d0, d1, ..., dn)
""" 
표준정규분포로부터 random sample 반환 
d0, d1, …, dn : 반환 데이터에 대한 dimensions 지정
"""
np.random.randn()
np.random.randn(2,3) # 2행 3열 array 반환
np.random.randn(2,3,4) # 2 array, 3행,4열 반환
3 + 2.5 * np.random.randn(2, 4) # N(3, 2.5^2) 분포에서 random sample 추출

## np.mat(data, dtype=None)
""" 
matrix 객체 생성
data : array 인풋 데이터 
dtype : 데이터 타입 지정 
"""
x = np.array([[1, 2], [3, 4]]) # 2행 2열 array 객체 생성
m = np.mat(x) # matrix 객체 생성
x[0,0] = 5 # 1행 1열 데이터 바꿈 (인덱스가 0부터 시작 유의)
m

## np.array(object, dtype=None, copy=True, order='K', subok=False, ndmin=0)
""" 
array 객체 생성
object : array 생성 데이터  
dtype : 데이터 타입 지정
ndmin : 최소 차원수
subok : sub 데이터 객체 그대로 남겨둠 만약 matrix데이터가 넘어오면 array로 바꾸지 않고 matrix그대로 유지한다는 의미
"""
np.array([1, 2, 3]) # array 객체 반환
np.array([1, 2, 3], ndmin=2) #  최소 2차원 array 객체 생성
np.array([1, 2, 3], dtype=complex) # data타입 = 복소수 지정
np.array(np.mat('1 2; 3 4'), subok=True) # matrix 객체를 그대로 넘김


## np.random.randint(low, high=None, size=None, dtype='l')
"""
최소값과 최대값사이의 정수를 동일한 확률로 random 추출 (이산 일양분포)
size : 추출 데이터 수, 및 차원 지정 
"""
np.random.randint(2, size=10)
np.random.randint(5, size=(2, 4)) # 2행 4열 random 추출

## np.arrange()
"""
create sequences of numbers
"""
np.arange(10, 30, 5) # 10부터 최대 30까지 5씩 증가시켜 array생성
np.arange(0, 2, 0.3)

## np.linspace()
"""
동일한 간격으로 등분하여 원하는 개수의 숫자를 반환 
"""
np.linspace(0, 2, 9) # 9 numbers from 0 to 2
np.linspace(0, 2*np.pi, 100) # 0부터 2*pi 사이의 수를 등분하여 100개 뽑음

# ndarray
"""
같은 종류의 데이터를 담을 수 있는 포괄적인 다차원 배열
"""
a = np.arange(15).reshape(3,5) # 3행 5열, 2차원 ndarray객체 생성
a
type(a)

## ndarray.ndim
"""
the number of axes (dimensions) of the array.
대괄호 쌍의 개수와 같다고 보면 됨
"""
a.ndim

## ndarray.shape
"""
the dimensions of the array. 
차원 수를 튜플로 반환 
"""
a.shape

## ndarray.size
"""
the total number of elements of the array. 
This is equal to the product of the elements of shape.
"""
a.size

## ndarray.dtype
"""
an object describing the type of the elements in the array. 
One can create or specify dtype’s using standard Python types. 
Additionally NumPy provides types of its own. numpy.int32, numpy.int16, 
and numpy.float64 are some examples.
"""
a.dtype
type(a[0][0]) # 데이터 타입 앞에 numpy 단어가 붙음

### Basic Operations
"""
Array의 기본적인 연산
"""
a = np.array([20, 30, 40, 50]) ;a
b = np.arange(4) ;b
a-b
b**2
10*np.sin(a)
a < 35 # 각 스칼라값에 condition 적용 가능

A = np.array([[1, 1],
              [0, 1]]) ;A
B = np.array([[2, 0],
              [3, 4]]) ;B
A * B  # 각 요소 끼리 곱함 (elementwise product)
A @ B  # 행렬 곱셈 (matrix product)
A.dot(B) # 행렬 곱셈 다른 표현

a = np.ones((2,3), dtype=int) ;a
b = np.random.random((2,3)) ;b
a *= 3 ;a # a = a*3과 같은 표현
b += a ;b # b = b+a와 같은 표현

a = np.random.random((2,3)) ;a
a.sum() # 모든 elements 합
a.min() # 최소값
a.max() # 최대값

b = np.arange(12).reshape(3,4)
b
# 축 지정해서 함수적용 가능
"""
axis = 0 : 열방향
axis = 1 : 행방향
"""
b.sum(axis=0)  # sum of each column
b.min(axis=1)  # min of each row
b.cumsum(axis=1)  # 누적합 cumulative sum along each row


### Universal Functions
"""
NumPy provides familiar mathematical functions such as sin, cos, and exp.
In NumPy, these are called “universal functions”(ufunc).
"""
B = np.arange(3) ;B
np.exp(B) # exponetial
np.sqrt(B) # 루트 값
C = np.array([2., -1., 4.])
np.add(B, C) # B+C와 같음

### Indexing, Slicing and Iterating
"""
Numpy 데이터 다루기 
"""
# 1차원 
a = np.arange(10)**3 ;a
a[2]
a[2:5]
a[:6:2] = -1000 # 0부터 시작해서 6전까지, 2번째 숫자마다 -1000넣음
a
a[ : :-1]  # reversed a

for i in a:
    print(i**(1/3.))
    
# n차원
# 함수를 활용한 array 생성
def f(a,b):
    return 10*a+b
b = np.fromfunction(f, (5, 4), dtype=int) # 5행 4열의 각 위치 값이 함수에 들어감
b
b[2, 3] # 행 열 위치값으로 데이터 추출
b[0:5, 1]  # each row in the second column of b
b[:, 1]  # equivalent to the previous example
b[1:3, :] # each column in the second and third row of b
b[-1] # 마지막 행
b[-2]

# dots(...) 활용
"""
다차원 Array에서 많은 콜론을 써야할 때 생략해주는 기능
x[1,2,...] is equivalent to x[1,2,:,:,:]
x[...,3] to x[:,:,:,:,3] and
x[4,...,5,:] to x[4,:,:,5,:]
"""
c = np.array([[[  0,  1,  2],
               [ 10, 12, 13]],
              [[100,101,102],
               [110,112,113]]])
c
c.shape # 2개의 2행, 3열
c[1,...]  # same as c[1,:,:] or c[1]
c[...,2]  # same as c[:,:,2]

# flat
"""
Array를 반복시킬때, elements를 반환하도록 함 
"""
for row in b :
    print(row)
for element in b.flat:
    print(element)


### Shape Manipulation
"""
Array의 Shape 조작
"""
a = np.floor(10*np.random.random((3,4)))
a.shape
a

## ravel()
"""
array의 shape를 1차원으로 바꿔줌
returns the array, flattened
"""
a.ravel()

## reshape()
"""
array의 shape를 다시 지정
"""
a.reshape(6,2)  # returns the array with a modified shape
a

## resize()
"""
reshape와 기능은 같지만, resize는 a자체를 바꿔서 새로 변수지정 안해도 됨
"""
a
a.resize((2,6))
a
a.reshape(3,-1) # -1 은 데이터 수에 맞게 차원을 자동으로 계산해 넣음


# T (transposed)
"""
array의 행과 열을 바꿈
"""
a.T  # returns the array, transposed
a
a.T.shape
a.shape


### Stacking together different arrays
"""
Array 객체 합치기(merging)
"""
a = np.floor(10*np.random.random((2,2)))
a
b = np.floor(10*np.random.random((2,2)))
b

## np.vstack(), np.hstack()
## np.row_stack(), np.column_stack()
"""
vertical, row 방향으로 데이터 연결, 쌓기
horizontal, column 방향으로 데이터 연결, 쌓기
"""
np.vstack((a,b))
np.row_stack((a,b))     # 위와 같은 기능

np.hstack((a,b))
np.column_stack((a,b))     # 위와 같은 기능

# 다른차원의 Array Stack
np.column_stack((a,b))     # with 2D arrays
a = np.array([4.,2.])
b = np.array([3.,8.])
np.column_stack((a,b))     # returns a 2D array
np.hstack((a,b))           # the result is different

# np.newaxis
"""
새로운 차원 추가 
"""
a[:, np.newaxis]         # this allows to have a 2D columns vector
np.column_stack((a[:, np.newaxis], b[:, np.newaxis]))
np.hstack((a[:, np.newaxis], b[:, np.newaxis]))   # the result is the same

### Splitting one array into several smaller ones
"""
Array를 분할하기
"""
a = np.floor(10*np.random.random((2,12)))
a

## np.hsplit
"""
horizontal 방향으로 split
"""
np.hsplit(a, 3)   # Split a into 3
np.hsplit(a,(3,4))   # 0~3까지 끊고, 3~4, 4~ 끝 까지 Split

