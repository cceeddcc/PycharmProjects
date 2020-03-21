import requests
from bs4 import BeautifulSoup
import selenium
import re

def init_ChromeDriver() :
    from selenium import webdriver
    options = webdriver.ChromeOptions() # Chromeoption 객체 생성
    options.add_argument('headless') # headless 모드 지정
    return webdriver.Chrome("c:/Users/S/Desktop/chromedriver_win32/chromedriver.exe",
                              chrome_options=options)

### requests
"""
서버에 얻고자 하는 데이터를 요청할 수 있는 모듈
파이썬에서 동작하는 작고 빠른 브라우저 웹서버로부터 초기 HTML만 받을 뿐,
추가 CSS/JavaScript 처리 하지 못한다. 거의 모든 플랫폼에서 구동 가능
"""

## session
"""
requests.session 메서드는 해당 reqeusts를 사용하는 동안 
cookie를 header에 유지하도록 하여 세션이 필요한 HTTP 요청(로그인 등 상태유지가 필요한 경우)
에 사용됩니다.
"""

## raise_for_status()
"""
응답코드가 200 즉, OK가 아닌 경우 에러를 발생시키는 메서드입니다.
"""

# 로그인이 필요한 사이트 크롤링 예제
"""
# 로그인 url
login_url = 'http://www.hanbit.co.kr/member/login_proc.php'
user = 'myid'
password = 'password'
session = requests.session()

# Form Data에 넘겨줄 파라미터 설정
params = dict()
params['m_id'] = user
params['m_passwd'] = password

# javascrit(jQuery) 코드를 분석(로그인 홈페이지에서 페이지소스 또는 개발자도구 Network를 확인)
# login_proc.php 를 m_id 와 m_passwd 값과 함께 POST로 호출하는 것을 확인
# 다음과 같이 requests.session.post() 메서드를 활용
res = session.post(login_url, data = params)
res

print(res.raise_for_status())

res.headers # 'Set-Cookie'로 PHPSESSID 라는 세션 ID 값이 넘어옴을 알 수 있다.

# cookie로 세션을 로그인 상태를 관리하는 상태를 확인해보기 위한 코드입니다.
session.cookies.get_dict()

# 여기서부터는 로그인이 된 세션이 유지됩니다.
# session 에 header에는 Cookie에 PHPSESSID가 들어갑니다.
mypage_url = 'http://www.hanbit.co.kr/myhanbit/myhanbit.html'
res = session.get(mypage_url)
res
soup = BeautifulSoup(res.text, 'html.parser')

# Chrome 개발자 도구에서 CSS SELECTOR를 통해 간단히 가져온 CSS SELECTOR 표현식을 사용
he_mileage = soup.select_one("#container > div > div.sm_mymileage > dl.mileage_section1 > dd > span")
# 다음과 같이 class를 .mileage_section2 로 그리고 그 하부 태그중에 span이 있다는 식으로 표현도 가능함
he_mileage = soup.select_one('.mileage_section1 span')

print ('mileage is', he_mileage.get_text())
"""

### BeautifulSoup
"""
서버에서 받아온 데이터에서 HTML, XML 등을 파싱하는 라이브러리
주로 Requests에 의해 많이 사용되지만, Selenium에서도 사용할 수 있다. 
"""

res = requests.get("http://v.media.daum.net/v/20170615203441266") # HTML 페이지 요청
soup = BeautifulSoup(res.content, "html.parser") # HTML 페이지 파싱
title = soup.find("title") # 필요한 데이터 검색
title.get_text() # 필요한 데이터 추출

## find()
## find_all()
"""
find() : 가장 먼저 검색되는 태그 반환
find_all() : 전체 태그 반환, 관련된 모든 데이터를 리스트 형태로 추출
"""

html = "<html> \
            <body> \
                <h1 id='title'>[1]크롤링이란?</h1> \
                <p class='cssstyle'>웹페이지에서 필요한 데이터를 추출하는 것</p> \
                <p id='body' align='center'>파이썬을 중심으로 다양한 웹크롤링 기술 발달</p> \
            </body> \
        </html>"

soup = BeautifulSoup(html, "html.parser")
paragraph_data = soup.find('p') # 가장 먼저 검색되는 태그를 반환
paragraph_data.string # 텍스트만 추출
paragraph_data.get_text() # 텍스트만 추출

title_data = soup.find(id='title') # 태그 id로 검색
title_data

paragraph_data = soup.find('p', class_='cssstyle') # HTML태그와 CSS class로 검색
paragraph_data

paragraph_data = soup.find('p', 'cssstyle') # HTML태그와 CSS class로 검색
paragraph_data

# HTML 태그와 태그에 있는 속성:속성값을 활용해서 검색
paragraph_data = soup.find('p', attrs = {'align': 'center'})
paragraph_data

paragraph_data = soup.find_all('p') # 관련된 모든 데이터 리스트로 추출
paragraph_data
paragraph_data[0].get_text()
paragraph_data[1].get_text()

# String 활용 : html에서 찾고자 하는 문자열로 검색 가능
res = requests.get('http://v.media.daum.net/v/20170518153405933')
soup = BeautifulSoup(res.content, 'html5lib')
soup.find_all(string='오대석')
soup.find_all(string=['[이주의해시태그-#네이버-클로바]쑥쑥 크는 네이버 AI', '오대석'])
soup.find_all(string='AI')

## select()
"""
CSS Selector 문법을 이용해서 태그를 검색하는 메서드
CSS Selector 문법 관련 문서 :
https://saucelabs.com/resources/articles/selenium-tips-css-selectors
리스트 형태로 전체 반환 
"""

res = requests.get('http://v.media.daum.net/v/20170615203441266')
soup = BeautifulSoup(res.content, 'html.parser')
title = soup.select('title')[0] # title 태그 검색
title

# 띄어쓰기가 있다면 하위 태그를 검색
title = soup.select('html head title')[0]
title.get_text()

title = soup.select('html title')[0] # 직계자식이 아니어도 가능
title.get_text()

# > 를 사용하는 경우 바로 아래의 자식만 검색
title = soup.select('html > title')[0] # 바로 아래 자식이 아니기 때문에 에러 발생

# 바로 아래 자식을 검색
title = soup.select('head > title')[0]
title

# .은 태그의 클래스를 검색
body = soup.select('.article_view')[0] # class가 article_view인 태그 탐색
print (type(body), len(body))
for p in body.find_all('p'):
    print(p.get_text())

# div태그 중 class가 article_view인 태그 탐색
body = soup.select('div.article_view')[0]
print (type(body), len(body))
for p in body.find_all('p'):
    print(p.get_text())

# div 태그 중 id가 harmonyContainer인 태그 탐색
container = soup.select('div#harmonyContainer')
print(container)

# div태그 중 id가 mArticle 인 태그의 하위 태그 중 아이디가 article_title인 태그
title = soup.select('div#mArticle  div#harmonyContainer')[0]
print(title.get_text())

# a태그이면서 href 속성을 갖는 경우 탐색, 리스트 타입으로 links 변수에 저장됨
res = requests.get('http://media.daum.net/economic/')
soup = BeautifulSoup(res.content, 'html.parser')
links = soup.select('a[href]')

for link in links:
    if re.search('http://\w+', link['href']):  # http:// 문자열 이후에 숫자 또는 문자[a-zA-Z0-9_]가 한 개 이상 있는 데이터와 매치됨
        print(link['href'])


### Selenium
"""
웹을 테스트하기 위한 목적으로 만들어진 프레임워크
브라우저(Chrome, Firefox, IE, PhantomJS 등)를 원격 컨트롤하는 라이브러리 
브라우저를 사용하므로, CSS/JavaScript 처리 지원
리소스를 많이 사용하고 느린 단점. 사이트에 따라 사용 못하기도 한다.
https://selenium-python.readthedocs.io/index.html 참고
"""

## webdriver.Chrome("c:/...")
"""
chrome driver가 설치된 위치 지정하여 사용
"""

## implicitly_wait(3)
"""
암묵적으로 모든 웹 자원 로드를 위해 3초 기다림
"""

## get(http://url.com’)
"""
url에 접근
"""

## page_source
"""
현재 렌더링 된 페이지의 Elements를 모두 가져오기
"""

## find_element_by_name('...’)
## find_elements_by_name('...’)
"""
페이지의 단일 element중 name으로 접근 (최초 발견한 태그만)
페이지의 단일 element중 name으로 접근 (모든 태그 리스트로 가져오기)
"""

## find_element_by_id('HTML_id’)
## find_elements_by_id('HTML_id’)
"""
id로 접근
"""
driver = webdriver.PhantomJS("C:/Users/S/Desktop/phantomjs-2.1.1-windows/bin/phantomjs")
driver.get('http://v.media.daum.net/v/20170202185812986')

body = driver.find_element_by_id('harmonyContainer')
print(body.text)

driver.quit()

## find_element_by_xpath(‘xpath’)
## find_elements_by_xpath(‘xpath’)
"""
xpath로 접근
"""

## find_element_by_css_selector(‘...’)
## find_elements_by_css_selector(‘...’)
"""
css selector로 접근
"""
driver = init_ChromeDriver()
driver.get('http://v.media.daum.net/v/20170202180355822')

# 클래스가 tit_view인 h3태그
title = driver.find_element_by_css_selector("h3.tit_view")
print (title.text)
driver.quit()

## find_element_by_class_name('...’)
## find_elements_by_class_name('...’)
"""
class 이름으로 접근
"""

## find_element_by_tag_name('...’)
## find_elements_by_tag_name('...’)
"""
tag name으로 접근
"""
driver = webdriver.PhantomJS("C:/Users/S/Desktop/phantomjs-2.1.1-windows/bin/phantomjs")
driver.get('http://v.media.daum.net/v/20170202185812986')

title = driver.find_element_by_tag_name('h3') # 최초 발견한 태그만 검색
print(title.text)

h3s = driver.find_elements_by_tag_name('h3') # 모든 태그 검색
for h3 in h3s:
    print(h3.text)

driver.quit()

## execute_script("...")
"""
Java script문을 활용해서 driver을 제어할 수 있음
"""

## WebDriverWait()
"""
페이지 로딩 시간을 기다린 후, 크롤링
몇몇 페이지의 경우, 페이지 로딩 지연이 발생하여(여러 요청이 병합하여 페이지 결과를 생성) 
tag를 못읽어오는 경우가 발생할 수 있음
이때, 아래의 코드를 이용하여 해결 가능
"""
# e.g) 10초내에 해당 tag를 찾으면 반환, 그렇지 않으면 timeout 발생!
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = init_ChromeDriver()
driver.get('http://v.media.daum.net/v/20170202180355822')
try:
    # id가 cMain인 tag를 10초 내에 검색, 그렇지 않으면 timeoutexception 발생
    element = WebDriverWait(driver, 10).until(
        # By.ID 는 ID로 검색, By.CSS_SELECTOR 는 CSS Selector 로 검색한다는 의미
        EC.presence_of_element_located((By.ID, "cMain"))
    )
    print(element.text)

except TimeoutException:
    print("해당 페이지에 cMain 을 ID 로 가진 태그가 존재하지 않거나, 해당 페이지가 10초 안에 열리지 않았습니다.")

finally:
    driver.quit()


## element.click()
"""
element 클릭
"""


## element.double_click()
"""
element 더블 클릭
"""


## element.send_keys()
"""
element 키보드 입력 전송
"""
driver = init_ChromeDriver()
driver.get("http://pythonscraping.com/pages/files/form.html")
firstnameField = driver.find_element_by_name("firstname")
lastnameField = driver.find_element_by_name("lastname")
submitButton = driver.find_element_by_id("submit")
firstnameField.send_keys("Doky")
lastnameField.send_keys("Kim")
submitButton.click()
print(driver.find_element_by_tag_name("body").text)
driver.close()

## element.move_to_element()
"""
element 로 마우스 이동
"""

## ActionChains()
"""
행동 여러 개를 체인 으로 묶어서 저장하고 원하는 만큼 실행
"""
## perform()
"""
메서드 실행시 전체 행동을 실행함
"""
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
driver = init_ChromeDriver()
driver.get("http://pythonscraping.com/pages/files/form.html")

firstnameField = driver.find_element_by_name("firstname")
lastnameField = driver.find_element_by_name("lastname")
submitButton = driver.find_element_by_id("submit")

# 일련의 행동 객체를 생성
actions = ActionChains(driver).click(firstnameField).send_keys("Doky").click(lastnameField).send_keys("Kim").send_keys(Keys.RETURN)
actions.perform() # 실행

print(driver.find_element_by_tag_name("body").text)
driver.close()

## close
"""
사용했던 chrome driver 닫기
"""

# 일반적인 로그인 예시
"""
from selenium import webdriver
import time

# 드라이버 생성
driver = webdriver.Chrome("c:/Users/S/Desktop/chromedriver_win32/chromedriver.exe")
login_url = "https://nid.naver.com/nidlogin.login"
driver.get(login_url)
driver.find_element_by_id("id").send_keys("myid")  # id 넣기
driver.find_element_by_id("pw").send_keys("password")  # password 넣기
# 네이버가 막아서 접근 불가

# 로그인 클릭
driver.find_element_by_xpath('//*[@id="frmNIDLogin"]/fieldset/input').click()
time.sleep(2)
"""

# 네이버 로그인 우회접근 예시
"""
from selenium import webdriver
import time

driver = webdriver.Chrome("c:/Users/S/Desktop/chromedriver_win32/chromedriver.exe")
login_url = "https://nid.naver.com/nidlogin.login"
driver.get(login_url)

## 네이버 로그인 우회
id = "id"
pw = "password"

# execute_script 함수 사용 (자바스크립트로 아이디, 패스워드를 직접 타이핑쳐서 넘겨주는 형태)
driver.execute_script("document.getElementsByName('id')[0].value=\'" + id + "\'")
driver.execute_script("document.getElementsByName('pw')[0].value=\'" + pw + "\'")

driver.find_element_by_xpath('//*[@id="frmNIDLogin"]/fieldset/input').click()

time.sleep(2)
driver.close()
"""

# PhantomJS
"""
WebTesting을 위해 나온 화면이 존재하지 않는 브라우저
터미널환경에서 동작하는 크롤러의 경우 PhantomJS 브라우저 사용 권장
https://phantomjs.org/download.html
"""

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

# phantomJS 드라이버 생성
driver = webdriver.PhantomJS("C:/Users/S/Desktop/phantomjs-2.1.1-windows/bin/phantomjs")
driver.get("http://www.python.org") # 화면은 안보여도 background에서 돌아가는중
print(driver.current_url)
print(driver.title)
elem = driver.find_element_by_name("q") # python 홈페이지의 Search box에 해당함
elem.clear() # 현재 input box에 있는 텍스트 초기화
elem.send_keys("python") # 키 이벤트 전송
elem.send_keys(Keys.RETURN) # 엔터 입력

# 스크린샷
driver.set_window_size(1400, 1000)
elem.screenshot("C:/Users/S/Desktop/pycon_event.png")
assert "No results found." not in driver.page_source

driver.quit()

# Chrome headless mode 사용하기
"""
크롬도 headless 모드로 브라우저를 띄우지 않고 사용 가능
phantomJS보다 성능이 우수함
"""
from selenium import webdriver

options = webdriver.ChromeOptions() # Chromeoption 객체 생성
options.add_argument('headless') # headless 모드 지정
options.add_argument('window-size=1920x1080') # 크롬창의 크기 지정
options.add_argument("disable-gpu") # 그래픽카드 가속 사용 안함
# 혹은 options.add_argument("--disable-gpu")

driver = webdriver.Chrome("c:/Users/S/Desktop/chromedriver_win32/chromedriver.exe",
                          chrome_options=options)

driver.get('http://naver.com')
driver.implicitly_wait(3)
# 스크린샷 촬영
driver.get_screenshot_as_file('c:/Users/S/Desktop/naver_main_headless.png')
driver.quit()

