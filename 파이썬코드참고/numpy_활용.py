import numpy as np
""" N차원 array 객체 다루는데 powerful """

# numpy.random.randn(d0, d1, ..., dn)
""" 
표준정규분포로부터 random sample 반환 
d0, d1, …, dn : 반환 데이터에 대한 dimensions 지정
"""
np.random.randn()
np.random.randn(2,3) # 2행 3열 array 반환
np.random.randn(2,3,4) # 3행 4열 x 2 array 반환
3 + 2.5 * np.random.randn(2, 4) # N(3, 2.5^2) 분포에서 random sample 추출

# numpy.mat(data, dtype=None)
""" 
matrix 객체 생성
data : array 인풋 데이터 
dtype : 데이터 타입 지정 
"""
x = np.array([[1, 2], [3, 4]]) # 2행 2열 array 객체 생성
m = np.mat(x) # matrix 객체 생성
x[0,0] = 5 # 1행 1열 데이터 바꿈 (인덱스가 0부터 시작 유의)
m

# numpy.array(object, dtype=None, copy=True, order='K', subok=False, ndmin=0)
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


# numpy.random.randint(low, high=None, size=None, dtype='l')
"""
최소값과 최대값사이의 정수를 동일한 확률로 random 추출 (이산 일양분포)
size : 추출 데이터 수, 및 차원 지정 
"""
np.random.randint(2, size=10)
np.random.randint(5, size=(2, 4)) # 2행 4열 random 추출
