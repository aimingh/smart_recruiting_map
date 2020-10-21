# 모듈 불러오기
from selenium import webdriver
from selenium.webdriver.common.by import By 
from pymongo import MongoClient
import sys
import time,random
from bs4 import BeautifulSoup
import requests
from pymongo import MongoClient

header = {'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36'}

 # 옵션 주기
def close_tab(driver):
    if len(driver.window_handles) >= 3 :
        driver.switch_to.window(driver.window_handles[-1])
        driver.close()

        driver.switch_to.window(driver.window_handles[-1])
        driver.close()

        last_tab = driver.window_handles[-1]
        driver.switch_to.window(window_name=last_tab)
    else : 
        last_tab = driver.window_handles[-1]
        driver.switch_to.window(window_name=last_tab)

def read_data(driver):
    table = driver.find_elements_by_css_selector('#dev-gi-list > div > div.tplList.tplJobList > table > tbody > tr')
    data = list()
    for tr in table:     
        time.sleep(random.uniform(0.5,1.2))   
        company_link = tr.find_element_by_css_selector('td.tplCo > a')
        title = tr.find_element_by_css_selector('td.tplTit > div > strong > a').text
        company = company_link.text
        work_content = tr.find_element_by_css_selector('td.tplTit > div > p.dsc').text

        # 회사 주소를 얻기위한 링크 이동 
        res = requests.get(url=company_link.get_attribute('href'),headers=header)
        bts = BeautifulSoup(res.content,'html5lib')       

        address_table = bts.find_all('th',{'class':'field-label'})
        for th in address_table :
            #print(th.text)
            if th.text == "주소 " or th.text =='주소':
                address = th.parent.find('div',{'class':'value'}).text
            
        #time.sleep(random.randint(1,2))
        data.append({'company':company,'address':address,'title':title,'work':work_content})
        print({'company':company,'address':address,'title':title})
        #driver.implicitly_wait(2)       

    return data

def read_jobkorea():

    options = webdriver.ChromeOptions()
    options.add_argument("--no-sandbox")
    options.add_argument('--disable-dev-shm-usage')
    # options.add_argument('--headless')
    options.add_argument('window-size=1920x1080')
    options.add_argument("disable-gpu")

    # 드라이버 불러오기
    # path = '/home/sanghoon/Documents/Develop/chromedriver'
    #path for cho 
    cho_path = '/home/cho/Documents/Develop/web_config/driver/chromedriver_linux'

    driver = webdriver.Chrome(executable_path=cho_path,chrome_options=options)
    driver.implicitly_wait(3)

    # 드라이버 get 메서드 호출하기
    driver.get("http://www.jobkorea.co.kr/recruit/joblist?menucode=cotype1&cotype=1,2,3,4,5,6?")
    num_job = int(int(str(driver.find_element_by_xpath('//*[@id="anchorGICnt_1"]/li[1]/button/span/em').text[1:-2]).replace(',',''))/40)
    i = 1
    while  i < num_job :
        with MongoClient("mongodb://127.0.0.1:27017/") as myclient :
            if myclient.Jobdata.Joblist.count()!=0:
                myclient.Jobdata.Joblist.drop()
            site_page = driver.find_elements_by_css_selector('#dvGIPaging > div > ul > li')
            _ = driver.find_element_by_css_selector('#dvGIPaging > div > p > a')
            data = read_data(driver)
            #print(data)
            myclient.Jobdata.Joblist.insert_many(data)
            for li in site_page[1:]:
                next_link = li.find_element_by_tag_name('a')   
                time.sleep(random.uniform(5,10))
                next_link.click()
                data = read_data(driver)
                myclient.Jobdata.Joblist.insert_many(data)
                #print(data)
            site_page.click()
            i+=1



if __name__ == "__main__":    
    read_jobkorea()