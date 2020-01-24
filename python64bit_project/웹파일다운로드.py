from selenium import webdriver
from bs4 import BeautifulSoup as bs
import time

driver = webdriver.Chrome("c:/Users/S/Desktop/chromedriver_win32/chromedriver.exe")
login_url = "https://www.fnguide.com/home/login"
driver.get(login_url)


driver.find_element_by_id("txtID").send_keys(myid)  # id 넣기
driver.find_element_by_id("txtPW").send_keys(password)  # password 넣기
driver.find_element_by_xpath('//*[@id="container"]/div/div/div[2]/div[2]/form/div/fieldset/button').click()

try :
    driver.find_element_by_xpath('//*[@id="divLogin"]/div[3]/form/button[1]').click()
except : pass



code = "A000020"
url = "http://www.fnguide.com/Fgdd/FinIndivCompTrend#gicode=%s&conyn=1&termgb=D&acntcode=10" %code
driver.get(url)
driver.find_element_by_xpath('//*[@id="TERM"]/button[3]').click()
driver.find_element_by_xpath('//*[@id="btnSubmit"]').click()


time.sleep(2)
driver.find_element_by_xpath('//*[@id="btnExcel"]').click()

# time.sleep(2)
# driver.close()


################################

import requests
url = "http://www.fnguide.com/api/fgdd/GetFinByIndiv?IN_GICODE=A005930&IN_GS_GB=D&IN_ACCT_STD=I&IN_CONSOLIDATED=1&IN_ACNT_CODE=10&IN_DETAIL=10&IN_MAXYEAR=10&_=1579870086525"
request_headers = {'UUser-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36',
                   "Referer" : "http://www.fnguide.com/Fgdd/FinIndivCompTrend",
                   }

r = requests.get(url, headers = request_headers)
html = r.content

soup = bs(html, "html.parser")
print(r)
r.text
