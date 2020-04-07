#### 함수
"""
반복되는 코드는 함수로 만들어서 사용하면 나중에 수정할 때 편리
"""

# ex) 함수 문법 예시
def cal_upper(price):
    upper_price = price *1.3
    return upper_price
cal_upper(10000)

# ex) 함수에서 두 개 이상의 값 반환하기
def cal_upper_lower(price):
    upper_price = price * 1.3
    lower_price = price * 0.7
    return (upper_price,lower_price)

cal_upper_lower(10000)
(up_price, lo_price) = cal_upper_lower(10000)

#### 모듈
"""
파이썬 모듈은 파일(.py)로 관리된다.
모듈 속에는 함수, 클래스, 변수 등이 올 수 있다.
여러 모듈을 패키지(Packages)로 묶을 수 있다.
현재폴더, PYTHONPATH(환경변수), 파이썬 설치 경로 순으로 모듈을 검색하여 사용한다.
PYTHONPATH 환경변수는 sys.path로 확인할 수 있다.
"""
import sys
sys.path

type(_) # _ 는 가장최근 반환된 값을 의미한다.

# ex) import한 모듈의 위치확인
import time
time # 빌트인 모듈
import random
random # 라이브러리에 위치

# ex) 모듈안의 함수나 변수이름 확인
dir(time)

# ex) 다양한 모듈 import 방법
import time
from time import sleep
import time as ti

#### Class
"""
"""
class BusinessCard :
    def set_info(self, name, email, addr): # method 정의 , self는 후에 생성하게 될 instance명을 의미한다고 보면 된다.
        self.name = name
        self.email = email
        self.addr = addr

    def print_info(self):
        print("------------------------")
        print("Name : ", self.name)
        print("Email : ", self.email)
        print("Address : ", self.addr)
        print("------------------------")

member1 = BusinessCard()
member1.set_info("Harim","cceeddcc@naver.com","서울시 동대문구")
member1.print_info()

## 생성자 __init__ (initialize)
"""
class의 객체를 생성했을 때, 실행되는 함수를 정의하는 것
이를 활용해서 초기값을 넣을 수 있다.
"""
class BusinessCard2() :
    def __init__(self, name, email, addr):
        self.name = name
        self.email = email
        self.addr = addr

    def print_info(self):
        print("------------------------")
        print("Name : ", self.name)
        print("Email : ", self.email)
        print("Address : ", self.addr)
        print("------------------------")

member2 = BusinessCard2("하림","cceedd", "전주시")
member2.print_info()

## class 변수, instance 변수 구분
class Account :
    accountnum = 0 # class 변수에 해당
    def __init__(self, name):
        self.name = name # instance 변수에 해당
        Account.accountnum += 1
    def __del__(self):
        Account.accountnum -= 1

# 각 종류의 변수는 해당 namespace에 값을 저장함
Kim = Account("Kim")
Lee = Account("Lee")

Kim.__dict__
Lee.__dict__
Account.__dict__
Kim.accountnum # instance 네임스페이스에 없기때문에 class 네임스페이스에서 값을 찾아옴

## Class 상속
"""
부모 Class에서 정의된 method들을 상속받아 수정, 관리가 쉽고 업그레이드가 가능해짐
"""

class parent :
    def singing(self):
        print("sing a song")

father = parent()
father.singing()

# 상속
class lucky_child(parent):
    def dancing(self):
        print("play dance")

child1 = lucky_child()
child1.singing()
child1.dancing()


## enumerate()
"""
열거하다
순서와 값을 각각 저장해서 enumerate object 생성
"""
data = enumerate((4,5,6))
type(data) # enumerate 타입
for i, value in data :
    print(i, ":", value)

## for문, if문 리스트 내포(List comprehension)하기
"""
[표현식 for 항목 in 반복가능객체 if 조건문 else 표현식]
"""
a = [1,2,3,4]
result = [num * 3 for num in a]
print(result)

a = [1,2,3,4]
result = [num * 3 for num in a if num % 2 == 0]
print(result)
"""
위와 같은 표현
a = [1,2,3,4]
result = []
for num in a:
    result.append(num*3)
"""

## for문 여러줄 사용
result = [x*y for x in range(2,10)
          for y in range(1,10)]
print(result)


#### *args **kwargs 이해
#### packing , Unpacking 이해
def sum(a,b) :
    return a+b

sum(1,2)
p = (1,2)
sum(p) # 오류 : 인자 수를 지켜야함
sum(*p) # unpacking

def sum2(*args) : # packing : 들어오는 인자를 하나의 튜플로 묶어줌
    for arg in args :
        arg += arg
    return(arg)
sum2(1,2,3) # 인자 수에 상관 없음

def sum(a,b) :
    return a+b
d = {"a":3,"b":4}
sum(**d) # unpacking

def person(**kwargs) :
    for k,v in kwargs.items():
        print(k,v)

person(name ="python", age=38, weight=70)
d= {"name" : "python", "age" : 38, "weight" : 70}
person(d) # 오류 : dict 데이터를 바로 넘겨주면 안됨 , unpacking 필요
person(**d) # unpacking

## formatting
"""
소수점, 문자열 등 포멧 지정 
"""
"My name is %s" %"하림"
"My name is {}".format("하림")
"{} x {} = {}".format(2,3,2*3)
"{2} x {0} = {1}".format(3,2*3,2) # 순서 지정 가능
"{0:.4f}".format(0.12345) # 소수점 4째자리 까지 나타냄 

#### PEP8
"""
일관된 코딩작성방법과 관련된 문서 
https://b.luavis.kr/python/python-convention  한글버전 
"""

## assert
"""
코드를 점검하는데 사용된다.
assert 조건문
만약 조건문이 True이면 아무런 행동을 하지 않고
False이면 assertion error를 발생시킨다.
"""
assert 1==1
assert 1==2