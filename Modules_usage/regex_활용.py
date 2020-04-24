import re
"""
정규표현식 regular expression
https://devanix.tistory.com/296 참고

"""

### 반복 메타 문자
"""
*  :  0회 이상 반복 
+  :  1회 이상 반복 
?  :  0회 or 1회
{m}  :  m회 반복
{m, n}  :  m회부터 n회까지 반복 
"""

### 매칭 메타 문자
"""
.  :  줄바꿈 문자(\n)를 제외한 모든 문자와 매치됨
^  :  문자열의 시작과 매치됨, [^패턴]은 해당 패턴이외의 모든 것을 의미함
$  :  문자열의 마지막과 매치됨
[ ]  :  여러 문자 중 각각 한 문자를 의미
|  :  또는(or)를 의미
{ }  :  정규식을 그룹으로 묶음
"""

### 이스케이프 기호
"""
\\  :  역슬래쉬 문자 자체
\d  :  모든 숫자와 매치됨 [0-9]
\D  :  숫자가 아닌 문자와 매치됨 [^0-9]
\s  :  화이트 스페이스 문자와 매치됨 [ \t\n\r\f\v]
\S  :  화이트 스페이스가 아닌 것과 매치됨 [^ \t\n\r\f\v]
\w  :  숫자 또는 문자와 매치됨 [a-zA-Z0-9_]
\W  :  숫자 또는 문자가 아닌 것과 매치됨 [^a-zA-Z0-9_]
\b  :  단어의 경계를 나타냄. 단어는 영문자 혹은 숫자의 연속 문자열
\B  :  단어의 경계가 아님을 나타냄
\A  :  문자열의 처음에만 일치
\Z  :  문자열의 끝에만 일치
"""

### 최소 매칭을 위한 정규식
"""
*?  :  *와 같으나 문자열을 최소로 매치함
+?  :  +와 같으나 문자열을 최소로 매치함
??  :  ?와 같으나 문자열을 최소로 매치함
{m,n}?  :  {m,n}과 같으나 문자열을 최소로 매치함
"""

### 정규 표현식에서 가용 가능한 플래그
"""
I, IGNORECASE	:  대, 소문자를 구별하지 않는다
L, LOCATE	    :  \w, \W, \b, \B를 현재의 로케일에 영향을 받게 한다
M, MULTILINE	:  ^가 문자열의 맨 처음, 각 라인의 맨 처음과 매치 된다 
	               $는 문자열의 맨 끝, 각 라인의 맨 끝과 매치
S, DOTALL	    :  .을 줄바꾸기 문자도 포함하여 매치하게 한다
U, UNICODE	    :  \w, \W, \b, \B가 유니코드 문자 특성에 의존하게 한다
X, VERBOSE    	:  정규식 안의 공백은 무시된다
"""

## IGNORECASE
s = "Apple is a big company and apple is very delicious"
c = re.compile("apple", re.I) # Ignorecase 대소문자 구분 안함
c.findall(s)


## MULTILINE
s = """window
unix
linux
solaris
"""
c = re.compile("^.+") # 첫 라인만 매칭
c.findall(s)
c = re.compile("^.+", re.M) # Multiline 설정
c.findall(s)

## DOTALL
p = re.compile('a.b')
m = p.match('a\nb')
print(m) # 원래 "."은 \n을 매치 못 시킴

p = re.compile('a.b', re.DOTALL)
m = p.match('a\nb')
print(m)

## VERBOSE
"""
정규식이 복잡할 경우 아래처럼 주석을 적고 여러 줄로 표현하는 것이 훨씬 가독성이 좋다
"""
charref = re.compile(r'&[#](0[0-7]+|[0-9]+|x[0-9a-fA-F]+);') # 이해하기 힘듦
charref = re.compile(r"""
 &[#]                # end of a numeric entity reference
 (
     0[0-7]+         # Octal form
   | [0-9]+          # Decimal form
   | x[0-9a-fA-F]+   # Hexadecimal form
 )
 ;                   # Trailing semicolon
""", re.VERBOSE)


### re모듈의 주요 메소드
## compile(pattern[, flags])
"""
pattern을 컴파일하여 정규식 객체를 반환
"""
p = re.compile('a.b')
re.match(p, "asb")

## match(pattern, string[,flags])
"""
string의 시작부분부터 pattern이 존재하는지 검사하여 
MatchObject 인스턴스를 반환
"""
bool(re.match("[0-9]*th", "   35th"))
bool(re.match("ap", "This is an apple"))

## search(pattern, string[,flags])
"""
string의 전체에 대해서 pattern이 존재하는지 검사하여 
MatchObject 인스턴스를 반환
"""
bool(re.search("[0-9]*th", "   35th")) # 문자열 전체에서 검색하기 때문에 Match와 차이
bool(re.search("ap", "This is an apple"))

## split(pattern, string[, maxplit=0])
"""
pattern을 구분자로 string을 분리하여 리스트로 반환
"""
# ':', '.', ' ' 문자를 구분자로 사용
re.split("[:. ]+", "apple Orange:banana.tomato")
re.split("([:. ])+", "apple Orange:banana.tomato") # 소괄호 사용시 분리 문자도 결과에 포함
re.split("[:. ]+", "apple Orange:banana.tomato",maxsplit=2 ) # 최대 분리 횟수 지정

## findall(pattern, string[, flags])
"""
string에서 pattern을 만족하는 문자열을 리스트로 반환
"""
re.findall(r"app\w*", "application orange apple banana app")

p = re.compile(r"app\w*") # 정규식을 객체에 저장해서 활용
p.findall("application orange apple banana app")

## finditer(pattern, string[, flags])
"""
string에서 pattern을 만족하는 문자열을 반복자로 반환
"""
p = re.compile("\w+")
result = p.finditer("life is too short")
print(result) # 매치된 단어들을 각각 매치타입으로 반복가능하게 반환
for r in result: print(r)


## sub(pattern, repl, string[, count=0])
"""
string에서 pattern과 일치하는 부분에 대하여 repl(replace)로 
교체하여 결과 문자열을 반환
"""
re.sub("-","@", "901225-1234567")
re.sub(r"[:,|\s]", ", ", "Apple:Orange Banana|Tomato,Grape") # 필드 구분자 통일
re.sub(r"[:,|\s]", ", ", "Apple:Orange Banana|Tomato,Grape", count=2) # 횟수 제한

# 변경할 문자열을 패턴으로 매칭시켜 찾아서 변경
# 매칭시킬 패턴 중 변경할 문자열에 사용할 부분에 대해 소괄호로 감싸준다.
re.sub(r"\b(\d{4}-\d{4})\b", r"<I>\1</I>","Copyright Derick 1990-2009")

# 매칭시킬 패턴에 명시적으로 이름을 지정(?P<패턴이름>패턴)
# 변경할 문자열에서 패턴이름 사용 \g<패턴이름>
re.sub(r"(?P<year>\d{4}-\d{4})\b",r"<I>\g<year></I>", "Copyright Derick 1990-2009")

## subn(pattern, repl, string[, count=0])
"""
sub와 동일하나, 결과로(결과문자열, 매칭횟수)를 튜플로 반환
"""

## escape(string)
"""
영문자 숫자가 아닌 문자들을 백슬래쉬 처리해서 리턴. 
(임의의 문자열을 정규식 패턴으로 사용할 경우 유용)
"""

### Match 객체
"""
Match객체는 match(), search()의 수행 결과로 생성되며, 
검색된 결과를 효율적으로 처리할 수 있는 기능 제공.
"""

## group([group1, ...])
"""
입력받은 인덱스에 해당하는 매칭된 문자열 결과의 부분 집합을 반환합니다. 
인덱스가 '0'이거나 입력되지 않은 경우 전체 매칭 문자열을 반환합니다.
"""

telChecker = re.compile(r"(\d{2,3})-(\d{3,4})-(\d{4})")
m = telChecker.match("02-123-4597")
m.group() # 매칭된 전체 문자열을 반환
m.group(1) # 첫 번째로 매칭된 문자열
m.group(2,3) # 해당 번째로 매칭된 문자열 튜플로 반환


## groups()
"""
매칭된 결과를 튜플 형태로 반환
"""
m.groups() # 매칭된 문자열 집합을 튜플로 반환

## start([group])
"""
매칭된 결과 문자열의 시작 인덱스를 반환. (인자로 부분 집합의 번호나 
명시된 이름이 전달된 경우, 그에 해당하는 시작 인덱스를 반환)
"""
m.start() # 매칭된 전체 문자열의 시작 인덱스
m.start(2) # 두번째 매칭된 문자열의 시작 인덱스


## end([group])
"""
매칭된 결과 문자열의 종료 인덱스를 반환. (인자로 부분 집합의 번호나 
명시된 이름이 전달된 경우, 그에 해당하는 종료 인덱스를 반환)
"""
m.end() # 매칭된 전체 문자열의 종료 인덱스
m.end(2) # 두번째 매칭된 문자열의 종료 인덱스

## span()
"""
매치된 문자열의 (시작, 끝)에 해당하는 튜플을 돌려준다.
"""
m.span()

## string
"""
매칭의 대상이 되는 원본 문자열입니다.
"""
m.string
m.string[m.start(2):m.end(3)]

## groupdict()
"""
이름이 붙여진 매칭 결과를 사전 형태로 반환
"""
# 매칭 결과에 각각 이름 부여
c = re.compile(r"(?P<area>\d+)-(?P<exchange>\d+)-(?P<user>\d+)")
m = c.match("02-123-4567")
m.group("area") # 이름으로 매칭된 값 가져오기
m.start("user")
m.groupdict() # 사전형태로 반환

## pos
"""
원본 문자열에서 검색을 시작하는 위치입니다.
"""

## endpos
"""
원본 문자열에서 검색을 종료하는 위치입니다.
"""

## lastindex
"""
매칭된 결과 집합에서 마지막 인덱스 번호를 반환. (일치된 결과가 없는 경우 
에는 None을 반환)
"""

## lastgroup
"""
매칭된 결과 집합에서 마지막으로 일치한 이름을 반환. (정규식의 매칭 조건에 
이름이 지정되지 않았거나 일치된 결과가 없는 경우 None 반환)
"""

### 로우 문자열 표기법 (Raw string notation)

"""
백슬래시(\) 문제
\section 을 매칭시키려면 \s가 정규식에서 다른 의미를 가지고 있기 때문에 
아래와 같이 적어야 한다.
\\section 즉 정규식에서 사용한 \ 문자가 문자열 자체임을 알려 주기 위해 
백슬래시 2개를 사용하여 이스케이프 처리를 해야 한다.

Raw String 규칙
p = re.compile(r'\section')
정규식 문자열 앞에 r 문자를 삽입하면 이 정규식은 Raw String 규칙에 의하여 
백슬래시 2개 대신 1개만 써도 2개를 쓴 것과 동일한 의미를 갖게 된다.
"""
bool(re.search("\\\\\w","\\apple"))
bool(re.search(r"\\\w",r"\apple"))


