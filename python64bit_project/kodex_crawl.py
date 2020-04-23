from selenium import webdriver
import pandas as pd
from datetime import datetime
import time

# 객체 생성 및 option 지정
options = webdriver.ChromeOptions()
options.add_argument('headless') # headless 모드 지정
options.add_argument('window-size=1920x1080') # 크롬창의 크기 지정
options.add_argument("disable-gpu") # 그래픽카드 가속 사용 안함
driver = webdriver.Chrome("c:/Users/S/Desktop/chromedriver_win32/chromedriver.exe",
                          chrome_options=options)
url ="http://www.kodex.com/product_view.do?fId=2ETF72"
driver.get(url)

# 실행과정
driver.find_element_by_id("idSubTab3").click()

start = "20190401"
end = "20200423" # tmp
# end = "20200401"
Dates = pd.date_range(start,end)
# Date_data, cash, dollar, deposit, WTI1, WTI2, ETF = [], [], [], [], [], [], []

df_name = pd.DataFrame()
t=0
for Date in Dates :
    try :
        t+=1
        print(t, " / " , len(Dates))
        Date = datetime.strftime(Date,"%Y-%m-%d")
        time.sleep(0.1)
        driver.find_element_by_id("gijunYMD").clear()
        time.sleep(0.1)
        driver.find_element_by_id("gijunYMD").send_keys(Date)
        driver.find_element_by_xpath('//*[@id="frmPdf"]/p/button').click()
        time.sleep(0.1)

        table = driver.find_element_by_id("pdfResultList")
        time.sleep(0.1)

        # 종목명에 뭐가 있는지 테스트
        num = len(table.find_elements_by_tag_name("td"))
        name_list = []
        if num > 10:
            times = int(num/6)
            for i in range(0,times):
                line = table.find_elements_by_tag_name("td")[1 + 6 * i]
                name_list.append(line.text)
            df = pd.DataFrame({"%s" %Date: name_list})
            df_name= pd.concat([df_name,df],axis=1)
        else:
            continue
    except :
         continue

driver.close()
df_name.to_excel("C:/Users/S/Desktop/tmp_name.xlsx")


# 1 년치 데이터 모으기

from selenium import webdriver
import pandas as pd
from datetime import datetime
import time

# 객체 생성 및 option 지정
options = webdriver.ChromeOptions()
options.add_argument('headless') # headless 모드 지정
options.add_argument('window-size=1920x1080') # 크롬창의 크기 지정
options.add_argument("disable-gpu") # 그래픽카드 가속 사용 안함
driver = webdriver.Chrome("c:/Users/S/Desktop/chromedriver_win32/chromedriver.exe",
                          chrome_options=options)
url ="http://www.kodex.com/product_view.do?fId=2ETF72"
driver.get(url)

# 실행과정
driver.find_element_by_id("idSubTab3").click()

start = "20190101"
end = "20200423" # tmp
# end = "20200423"
Dates = pd.date_range(start,end)
Date_data, WTI1, WTI1_cont, WTI2, WTI2_cont, ETF, ETF_cont = [], [], [], [], [], [], []

t=0
for Date in Dates :
    try :
        # Date = "2020-04-17" # tmp
        t+=1
        print(t, " / " , len(Dates))
        Date = datetime.strftime(Date,"%Y-%m-%d")
        time.sleep(0.1)
        driver.find_element_by_id("gijunYMD").clear()
        time.sleep(0.1)
        driver.find_element_by_id("gijunYMD").send_keys(Date)
        driver.find_element_by_xpath('//*[@id="frmPdf"]/p/button').click()
        time.sleep(0.1)

        table = driver.find_element_by_id("pdfResultList")
        time.sleep(0.1)

        # WTI 선물계약수, 금액
        # ETF 계약수, 금액 데이터
        num = len(table.find_elements_by_tag_name("td"))
        if num > 10:
            times = num/6

            if times == 5 :
                Date_data.append(Date)
                WTI1_cont.append(table.find_elements_by_tag_name("td")[int((times - 2) * 6 + 3)].text)
                WTI1.append(table.find_elements_by_tag_name("td")[int((times - 2) * 6 + 5)].text)
                ETF_cont.append(table.find_elements_by_tag_name("td")[int((times - 1) * 6 + 3)].text)
                ETF.append(table.find_elements_by_tag_name("td")[int((times - 1) * 6 + 5)].text)
                WTI2_cont.append(None)
                WTI2.append(None)

            else :
                comp1 = table.find_elements_by_tag_name("td")[int((times - 3) * 6 + 1)].text[-1]
                comp2 = table.find_elements_by_tag_name("td")[int((times - 2) * 6 + 1)].text[-1]

                if comp1 == "금" :
                    Date_data.append(Date)
                    WTI1_cont.append(table.find_elements_by_tag_name("td")[int((times - 2) * 6 + 3)].text)
                    WTI1.append(table.find_elements_by_tag_name("td")[int((times - 2) * 6 + 5)].text)
                    ETF_cont.append(table.find_elements_by_tag_name("td")[int((times - 1) * 6 + 3)].text)
                    ETF.append(table.find_elements_by_tag_name("td")[int((times - 1) * 6 + 5)].text)
                    WTI2_cont.append(None)
                    WTI2.append(None)

                elif comp1 > comp2:
                    Date_data.append(Date)
                    WTI1_cont.append(table.find_elements_by_tag_name("td")[int((times - 2) * 6 + 3)].text)
                    WTI1.append(table.find_elements_by_tag_name("td")[int((times - 2) * 6 + 5)].text)
                    WTI2_cont.append(table.find_elements_by_tag_name("td")[int((times - 3) * 6 + 3)].text)
                    WTI2.append(table.find_elements_by_tag_name("td")[int((times - 3) * 6 + 5)].text)
                    ETF_cont.append(table.find_elements_by_tag_name("td")[int((times - 1) * 6 + 3)].text)
                    ETF.append(table.find_elements_by_tag_name("td")[int((times - 1) * 6 + 5)].text)
                else:
                    Date_data.append(Date)
                    WTI2_cont.append(table.find_elements_by_tag_name("td")[int((times - 2) * 6 + 3)].text)
                    WTI2.append(table.find_elements_by_tag_name("td")[int((times - 2) * 6 + 5)].text)
                    WTI1_cont.append(table.find_elements_by_tag_name("td")[int((times - 3) * 6 + 3)].text)
                    WTI1.append(table.find_elements_by_tag_name("td")[int((times - 3) * 6 + 5)].text)
                    ETF_cont.append(table.find_elements_by_tag_name("td")[int((times - 1) * 6 + 3)].text)
                    ETF.append(table.find_elements_by_tag_name("td")[int((times - 1) * 6 + 5)].text)

        else : continue
    except : continue

driver.close()

my_df = pd.DataFrame({"Date" : Date_data,
                      "WTI1" : WTI1,
                      "WTI1_cont" : WTI1_cont,
                      "WTI2" : WTI2,
                      "WTI2_cont" : WTI2_cont,
                      "ETF" : ETF,
                      "ETF_cont" : ETF_cont})

# 데이터 정제
my_df = my_df.fillna("0")

for j in range(len(my_df.columns)):
    try :
        my_df.iloc[:,j] = [my_df.iloc[i,j].replace(",","") for i in range(len(my_df.index))]
        my_df.iloc[:,j]= pd.to_numeric(my_df.iloc[:, j])
    except : continue
my_df.to_excel("C:/Users/S/Desktop/KODEX_WTI.xlsx")


df_kodex = pd.read_excel("C:/Users/S/Desktop/my_df.xlsx", index_col=None)
df_kodex=df_kodex.iloc[:,1:]
df_kodex

# 회귀분석으로 WTI선물 계약 당 NAV 영향력 측정
import statsmodels.api as stm
df_kodex.columns
m = stm.formula.ols("NAV~WTI1_cont+WTI2_cont+ETF_cont", data=df_kodex)
r = m.fit()
r.summary()