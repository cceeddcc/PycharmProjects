import re
"""
정규표현식 regular expression
"""

"""
[자주 사용하는 문자 클래스]
[0-9] 또는 [a-zA-Z] 등은 무척 자주 사용하는 정규 표현식이다. 이렇게 자주 사용하는 정규식은 별도의 표기법으로 표현할 수 있다.

\d - 숫자와 매치, [0-9]와 동일한 표현식이다.
\D - 숫자가 아닌 것과 매치, [^0-9]와 동일한 표현식이다.
\s - whitespace 문자와 매치, [ \t\n\r\f\v]와 동일한 표현식이다. 맨 앞의 빈 칸은 공백문자(space)를 의미한다.
\S - whitespace 문자가 아닌 것과 매치, [^ \t\n\r\f\v]와 동일한 표현식이다.
\w - 문자+숫자(alphanumeric)와 매치, [a-zA-Z0-9_]와 동일한 표현식이다.
\W - 문자+숫자(alphanumeric)가 아닌 문자와 매치, [^a-zA-Z0-9_]와 동일한 표현식이다.
대문자로 사용된 것은 소문자의 반대임을 추측할 수 있다.
"""


# Dot(.) : 정규 표현식의 메타 문자는 줄바꿈 문자인 \n을 제외한 모든 문자와 매치됨
"""
a.b  :  "." 을 모든 문자에 대응해서 인식
a[.]b  : "." 문자그대로 인식
"""
# 반복 (*) : *은 * 바로 앞에 있는 문자가 0부터 무한대로 반복될 수 있다는 의미이다.
# 반복 (+) : +은 + 바로 앞에 있는 문자가 1부터 무한대로 반복될 수 있다는 의미이다.
# 반복 ({m,n}) : {}사이에 반복을 원하는 횟수 지정
"""
{ } 메타 문자를 사용하면 반복 횟수를 고정할 수 있다. 
{m, n} 정규식을 사용하면 반복 횟수가 m부터 n까지 매치할 수 있다. 또한 m 또는 n을 생략할 수도 있다. 
만약 {3,}처럼 사용하면 반복 횟수가 3 이상인 경우이고 {,3}처럼 사용하면 반복 횟수가 3 이하를 의미한다. 
생략된 m은 0과 동일하며, 생략된 n은 무한대(2억 개 미만)의 의미를 갖는다.

ca{2,5}t # "c + a(2~5회 반복) + t"
"""

# 반복 (?)
"""
반복은 아니지만 이와 비슷한 개념으로 ? 이 있다. ? 메타문자가 의미하는 것은 {0, 1} 이다.
ab?c # a + b(있어도 되고 없어도 된다) + c

"""

# ^, $
"""
^는 문자열의 처음을 의미하고, $는 문자열의 마지막을 의미한다. 
예를 들어 정규식이 ^python인 경우 문자열의 처음은 항상 python으로 시작해야 매치되고, 
만약 정규식이 python$이라면 문자열의 마지막은 항상 python으로 끝나야 매치된다는 의미이다.
"""

# 활용 메서드
"""
match()	    문자열의 처음부터 정규식과 매치되는지 조사한다.
search()	문자열 전체를 검색하여 정규식과 매치되는지 조사한다.
findall()	정규식과 매치되는 모든 문자열(substring)을 리스트로 돌려준다.
finditer()	정규식과 매치되는 모든 문자열(substring)을 반복 가능한 객체로 돌려준다.
"""
import re
p = re.compile('[a-z]+')

# match()
m = p.match("python")
print(m)

m = p.match("3 python")
print(m) # 처음 나오는 3이 조건에 부합하지 않아 None

# search()
m = p.search("python")
print(m)

m = p.search("3 python")
print(m) # match와 비교

# findall()
result = p.findall("life is too short")
print(result) # 리스트로 반환

# finditer()
result = p.finditer("life is too short")
print(result) # 매치된 단어들을 각각 매치타입으로 반복가능하게 반환
for r in result: print(r)


# 매치된 객체에 대한 메서드
"""
group()	매치된 문자열을 돌려준다.
start()	매치된 문자열의 시작 위치를 돌려준다.
end()	매치된 문자열의 끝 위치를 돌려준다.
span()	매치된 문자열의 (시작, 끝)에 해당하는 튜플을 돌려준다.
"""

m = p.match("python")
m.group()
m.start()
m.end()
m.span()

m = p.search("3 python")
m.group()
m.start()
m.end()
m.span()

# 축약형태
p = re.compile('[a-z]+')
m = p.match("python")

m = re.match('[a-z]+', "python") # 위와 같은 표현

# 컴파일 옵션
"""
DOTALL(S) - "."이 줄바꿈 문자를 포함하여 모든 문자와 매치할 수 있도록 한다.
IGNORECASE(I) - 대소문자에 관계없이 매치할 수 있도록 한다.
MULTILINE(M) - 여러줄과 매치할 수 있도록 한다. (^, $ 메타문자의 사용과 관계가 있는 옵션이다)
VERBOSE(X) - verbose 모드를 사용할 수 있도록 한다. (정규식을 보기 편하게 만들수 있고 주석등을 사용할 수 있게된다.)
"""

# DOTALL
p = re.compile('a.b')
m = p.match('a\nb')
print(m) # 원래 "."은 \n을 매치 못 시킴

p = re.compile('a.b', re.DOTALL)
m = p.match('a\nb')
print(m)

# IGNORECASE
p = re.compile('[a-z]', re.I) # 대소문자 구별 안함
p.match('python')
p.match('Python')
p.match('PYTHON')


# MULTILINE
p = re.compile("^python\s\w+")
data = """python one
life is too short
python two
you need python
python three"""
print(p.findall(data))

p = re.compile("^python\s\w+", re.MULTILINE)
data = """python one
life is too short
python two
you need python
python three"""
print(p.findall(data)) # ^, $ 메타 문자를 문자열의 각 줄마다 적용

# VERBOSE
charref = re.compile(r'&[#](0[0-7]+|[0-9]+|x[0-9a-fA-F]+);') # 이해하기 힘듦
# 정규식이 복잡할 경우 아래처럼 주석을 적고 여러 줄로 표현하는 것이 훨씬 가독성이 좋다
charref = re.compile(r"""
 &[#]                # end of a numeric entity reference
 (
     0[0-7]+         # Octal form
   | [0-9]+          # Decimal form
   | x[0-9a-fA-F]+   # Hexadecimal form
 )
 ;                   # Trailing semicolon
""", re.VERBOSE)

# 백슬래시(\) 문제
"""
\section 을 매칭시키려면 \s가 정규식에서 다른 의미를 가지고 있기 때문에 아래와 같이 적어야 한다.
\\section 즉 정규식에서 사용한 \ 문자가 문자열 자체임을 알려 주기 위해 백슬래시 2개를 사용하여 이스케이프 처리를 해야 한다.

Raw String 규칙
p = re.compile(r'\section')
정규식 문자열 앞에 r 문자를 삽입하면 이 정규식은 Raw String 규칙에 의하여 백슬래시 2개 대신 1개만 써도 2개를 쓴 것과 동일한 의미를 갖게 된다.
"""


