import requests
from bs4 import BeautifulSoup

### 1. requests
"""
서버에 얻고자 하는 데이터를 요청할 수 있는 모듈
파이썬에서 동작하는 작고 빠른 브라우저 웹서버로부터 초기 HTML만 받을 뿐,
추가 CSS/JavaScript 처리 하지 못한다. 거의 모든 플랫폼에서 구동 가능
"""

### 2. BeautifulSoup
"""
서버에서 받아온 데이터에서 HTML, XML 등을 파싱하는 라이브러리
주로 Requests에 의해 많이 사용되지만, Selenium에서도 사용할 수 있다. 
"""

res = requests.get("http://v.media.daum.net/v/20170615203441266") # HTML 페이지 요청
soup = BeautifulSoup(res.content, "html.parser") # HTML 페이지 파싱
title = soup.find("title") # 필요한 데이터 검색
title.get_text() # 필요한 데이터 추출

## 2-1 find()
## 2-2 find_all()
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

### 3. Selenium
"""
브라우저(Chrome, Firefox, IE, PhantomJS 등)를 원격 컨트롤하는 라이브러리 
브라우저를 사용하므로, CSS/JavaScript 처리 지원
리소스를 많이 사용하고 느린 단점. 사이트에 따라 사용 못하기도 한다.
"""



