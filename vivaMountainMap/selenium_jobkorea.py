# 모듈 불러오기
from selenium import webdriver
from selenium.webdriver.common.by import By 
from pymongo import MongoClient
import sys
import time,random
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
        time.sleep(random.randint(2,5))
        company_link = tr.find_element_by_css_selector('td.tplCo > a')
        title = tr.find_element_by_css_selector('td.tplTit > div > strong > a').text
        company = company_link.text
        work_content = tr.find_element_by_css_selector('td.tplTit > div > p.dsc').text

        # 회사 주소를 얻기위한 링크 이동 
        company_link.click()
        close_tab(driver)

        address_table = driver.find_elements_by_class_name('field')
        for tr in address_table :
            if tr.find_element_by_tag_name('th').text == '주소' :
                address = tr.find_element_by_tag_name('td').text
        # 기존 링크로 복귀
        time.sleep(random.randint(1,2))
        driver.close()   
        first_tab = driver.window_handles[0]
        driver.switch_to.window(window_name=first_tab )

        data.append({'company':company,'address':address,'title':title,'work':work_content})
        #driver.implicitly_wait(2)
        

    return data

def read_jobkorea():

    options = webdriver.ChromeOptions()
    options.add_argument("--no-sandbox")
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--headless')
    options.add_argument('window-size=1920x1080')
    options.add_argument("disable-gpu")

    # 드라이버 불러오기
    path = '/home/sanghoon/Documents/Develop/chromedriver'
    #path for cho 
    cho_path = '/home/cho/Documents/Develop/web_config/driver/chromedriver_linux'

    driver = webdriver.Chrome(executable_path=cho_path,chrome_options=options)
    driver.implicitly_wait(3)

    # 드라이버 get 메서드 호출하기
    driver.get("http://www.jobkorea.co.kr/recruit/joblist?menucode=cotype1&cotype=1,2,3,4,5,6?")
    num_job = int(int(str(driver.find_element_by_css_selector('#anchorGICnt_1 > li.on > button > span > em').text[1:-2]).replace(',',''))/40)
    i = 1
    while  i < num_job :
        site_page = driver.find_elements_by_css_selector('#dvGIPaging > div > ul > li')
        next_page = driver.find_element_by_css_selector('#dvGIPaging > div > p > a')
        data = read_data(driver)
        print(data)

        for li in site_page[1:]:
            next_link = li.find_element_by_tag_name('a')   
            next_link.click()
            data = read_data(driver)
            print(data)
        site_page.click()
        i+=1



if __name__ == "__main__":    
    read_jobkorea()