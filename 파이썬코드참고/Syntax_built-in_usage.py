"""
This documents has been writing to show
how to use python syntax and built-in module/function

navigator
# syn : ...
 : syntax

# bi : ...
 : built_in function or module

# method : ...

# : comments / examples
"""

# syn : is
"""
id object가 같은지 비교
id(a) == id(b) 비교와 같음
"""
a = [1,2,3]
b = [1,2,3]
a == b # True
a is b # False
print(id(a), id(b)) # id가 다름

b = a
print(id(a), id(b)) # id 같음
a is b

# bi : dir()
"""
return list of attributes and method which can be used 
"""
dir(str)

# bi : help()
"""
return documents about how to use 
"""
help(str)
help(str.lower) # 사용법, 도움말 확인

# bi : str()
"""
String Data
"""
dir(str)
help(str)

# str object indexing
m = "Hello World"
m[0]
m[-1]
m[:5]

# method : str.lower()
"""
Return a copy of the string converted to lowercase
"""
m = "Hello World"
m.lower()

# method : str.upper()
"""
Retunr a copy of the string converted to uppercase
"""
m = "Hello World"
m.upper()

# method : str.count()
"""
해당 character 개수 counting 
"""
m = "Hello World"
m.count("l")
m.count("rld")

# method : str.find()
"""
해당 character start index 반환
"""
m = "Hello World"
m.find("World")
m[m.find("World"):]
m.find("Univers") # 없는 단어는 -1 반환

# method : str.replace()
"""
replace the character 
"""
m = "Hello World"
m.replace("World","Universe")

# method : str.format()
# syn : f""
"""
string object formatting 
"""
greeting = "Hello"
name = "Michael"
m = "{}, {}. Welcome!".format(greeting, name)
m

# 위와 같은 표현
m = f"{greeting}, {name.upper()}. Welcome!"
m

# method : str.join()
"""
Concatenate any number of strings.
"""
help(str.join)
course = ["History", "Math", "Physics"]
course_str = ", ".join(course)
course_str

course_str = "-".join(course)
course_str

# method : str.split()
"""
Return a list of the words in the string, 
using sep as the delimiter string.
"""
help(str.split)
course = ["History", "Math", "Physics"]
course_str = "-".join(course)
course_str.split("-")

# bi : Dictionary(dict)
"""
Dictionary data 활용
"""
dir(dict)
help(dict)

# method : dict.get()
"""
Return the value for key
잘못된 key가 들어오면 error가 아닌 지정한 값 반환 
"""
help(dict.get)
student = {"name" : "john", "age" : 25, "courses" : ["Math","CompSci"]}
student.get("age")
student["Phone"] # 에러발생
print(student.get("Phone")) # None 반환
student.get("Phone", "Not found")

# method : dict.get()
"""
update data 
"""
help(dict.update)
student = {"name" : "john", "age" : 25, "courses" : ["Math","CompSci"]}
student.update({"name" : "Jane", "age" : 26,
                "Phone" : "555"})
student

# syn : del
"""
delete key:value 
"""
student = {"name" : "john", "age" : 25, "courses" : ["Math","CompSci"]}
del student["age"]
student

# method : dict.pop()
"""
remove specified key and return the corresponding valu
"""
help(dict.pop)
student = {"name" : "john", "age" : 25, "courses" : ["Math","CompSci"]}
student.pop("age")
student

# bi : List
dir(list)
help(list)

# Empty List
empty_list = []
empty_list = list()

# method : list.insert()
"""
Insert object before index
extend와 구별 
"""
help(list.insert)
courses = ["History", "Math", "Physics", "CompSci"]
courses.insert(3,"Act")
courses_2 = ["Art", "Education"]
courses.insert(0,courses_2)
courses

# method : list.extend()
"""
Extend list by appending elements from the iterable.
"""
help(list.extend)
courses = ["History", "Math", "Physics", "CompSci"]
courses_2 = ["Art", "Education"]
courses.extend(courses_2)
courses

# method : list.remove()
"""
Remove first occurrence of value.
"""
help(list.remove)
courses = ["History", "Math", "Physics", "CompSci"]
courses.remove('Math')
courses

# method : list.pop()
"""
Remove and return item at index (default last).
"""
help(list.pop)
courses = ["History", "Math", "Physics", "CompSci"]
courses.pop(1) # 1번째 데이터 삭제

# method : list.reverse()
"""
Reverse *IN PLACE*
"""
help(list.reverse)
courses = ["History", "Math", "Physics", "CompSci"]
courses.reverse()
courses

# method : list.sort()
"""
Stable sort *IN PLACE*
default ascending order 
"""
help(list.sort)
nums = [1,5,2,4,3]
nums.sort()
nums
nums.sort(reverse=True)
nums

# method : list.index()
"""
Return first index of value.
"""
help(list.index)
courses = ["History", "Math", "Physics", "CompSci"]
courses.index("Physics")

# bi : Tuple
dir(tuple)
help(tuple)

# Empty Tuple
empty_tuple = ()
empty_tuple = tuple()

# bi : Set
dir(set)
help(set)

# Empty Set
empty_set = set()

# method : set.intersection()
"""
Return the intersection of two sets as a new set.
"""
help(set.intersection)
cs_courses = {"History", "Math", "Physics", "CompSci"}
art_courses = {"History", "Math", "Art", "Design"}
cs_courses.intersection(art_courses)

# method : set.difference()
"""
Return the difference of two or more sets as a new set.
"""
help(set.difference)
cs_courses = {"History", "Math", "Physics", "CompSci"}
art_courses = {"History", "Math", "Art", "Design"}
cs_courses.difference(art_courses)

# method : set.union()
"""
Return the union of sets as a new set.
"""
help(set.union)
cs_courses = {"History", "Math", "Physics", "CompSci"}
art_courses = {"History", "Math", "Art", "Design"}
cs_courses.union(art_courses)

# bi : sorted()
"""
sorting method
"""
help(sorted)
nums = [5, 3, 1, 2, 6]
sorted(nums)

# bi : min()
help(min)
nums = [5, 3, 1, 2, 6]
min(nums)

# bi : max()
help(max)
nums = [5, 3, 1, 2, 6]
max(nums)

# bi : sum()
help(sum)
nums = [5, 3, 1, 2, 6]
sum(nums)

# syn : in
"""
해당 data가 interable data에 있는지 확인 
"""
courses = ["History", "Math", "Physics", "CompSci"]
"Math" in courses
"math" in courses # 대소문자 구분

# syn : Arithmetic Operators
# Floor Division
3 // 2
# Exponent
3 ** 2
# Modulus
"""
Return remainder 
"""
3 % 2
5 % 3

# bi : abs()
"""
convert the number to absolute value
"""
abs(-3)

# bi : round()
help(round)
round(3.75)
round(3.3)
round(3.75, 1) # decimal digits
round(43.75, -1)

# syn : def
"""
define function
반복되는 코드는 함수로 만들어서 사용하면 나중에 수정할 때 편리
"""

# set default parameter value
def hello_func(greeting, name="You") : # name의 default 값 설정
    return "{}, {}".format(greeting,name)
print(hello_func("Hi"))
print(hello_func("Hi", name = "Corey"))

# positional arguments have to come before keyword arguments
print(hello_func(name = "Corey", "Hi")) # error

# syn : *args **kwargs
"""
Using this, when we don't know how many positional arguments and 
keword arguments are used 

args : positional argument, 함수 괄호안에 들어가는 일반적인 parameter
       list형으로 unpacking하여 넘겨주면 tuple형으로 return
kwargs : keyword argument, 함수 괄호안에 keyword = value로 들어가는 parameter
         dictionary형으로 unpacking하여 넘겨준다.
"""
def student_info(*args, **kwargs):
    print(args)
    print(kwargs)

student_info("Math", "Art", name="John", age=22)

# packing
courses = ["Math", "Art"]
info = {"name":"John", "age":22}

# unpacking
"""
use * or ** to unpacking
"""
student_info(courses,info) # not unpacking
student_info(*courses,**info) # unpacking


# syn : Module
"""
python module file is .py
packing modules is Package
"""

# path which modules are imported from
"""
Modules can be imported when the module's path is included in the sys.path
find the module in current dir and next sys.path's order 
"""
import sys
sys.path

# Adding path
"""
1. sys.path.add("C:/모듈위치")
2. add windows environment variable 
: 제어판 -> 시스템 및 보안 -> 시스템 -> 설정변경 -> 고급 -> 환경변수 -> 사용자변수 새로만들기
-> 변수명 = PYTHONPATH, 변수값 = "C:/모듈위치"
"""

# import module methods
"""
how to import module 
"""
import pandas
import pandas as pd
from pandas import DataFrame
from pandas import Series, DataFrame
from pandas import Series as SR, DataFrame as DF
from pandas import * # import all method

# find module's location
"""
use __file__(Dunder file) to find module's location
"""
import random
random
random.__file__

import time
time # built-in module
time.__file__

# bi : enumerate()
"""
열거하다
순서와 값을 각각 저장해서 enumerate object 생성
"""
help(enumerate)
courses = ["History", "Math", "Physics", "CompSci"]
data = enumerate(courses, start=1)
type(data) # enumerate 타입
for i, value in data :
    print(i, value)

# syn : for
"""
loop code finite times 
"""

# for문, if문 리스트 내포(List comprehension)
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

# list comprehenstion muliti for loop
result = [x*y for x in range(2,10)
          for y in range(1,10)]
print(result)

# syn : break
"""
break out loop
"""
nums = [1,2,3,4,5]
for num in nums :
    if num == 3:
        print("Found!")
        break
    print(num)

# syn : continue
"""
skip next iteration
"""
nums = [1,2,3,4,5]
for num in nums :
    if num == 3:
        print("Found!")
        continue
    print(num)

# syn : while
"""
조건 만족할 때 까지 무한 루프
"""
x = 0
while x < 5 :
    print(x)
    x += 1

x = 0
while x < 10 :
    if x == 5 :
        break
    print(x)
    x+=1

x = 0
while True : # 무한 루프 실행
    if x == 5:
        break
    print(x)
    x+=1









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