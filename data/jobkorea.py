# 모듈 불러오기
from selenium import webdriver
from selenium.webdriver.common.by import By 

from pymongo import MongoClient
import sys
import time


def ConnectSeleniumDB():
    """
    pymongo 연결하기
    리턴값 : MongoCLient 객체
    """
    str_server = "mongodb://192.168.219.128:27017/"
    client = MongoClient(str_server)
    return client

def InsertSeleniumDB( client, dataList ):
    """
    WORKGOKR 테이블에 데이터를 추가한다.
    client : MongoClient 객체
    dataList : WORKGOKR 정보를 담고 있는 리스트 변수 ( CPNAME, JOB, URL)
    """
    # DB 선택하기
    db = client['mydb']

    # dict 데이터 객체 생성하기
    data = dict()
    data['CPNAME'] = dataList[0]
    data['JOB'] = dataList[1]
    data['URL'] = dataList[2]

    db.JOBKOREA.insert(data)

def ShowSeleniumDB( client ):
    """
    jobkorea 테이블의 내용을 출력한다.
    client : MongoClient 객체
    """

    # DB 선택하기
    db = client['mydb']

    # cursor 얻기
    cursor = db.JOBKOREA.find()

    nCount = 1
    for row in cursor:
        print("%d" %nCount)
        print("회사 이름 : %s" %row['CPNAME'])
        print("직업 소개 : %s" %row['JOB'])
        print("상세 주소 : %s" %row['URL'])
        print("-"*20)
        nCount = nCount + 1


# work.go.kr 읽어오기
def ReadJOBKOREA():
    # 옵션 주기
    options = webdriver.ChromeOptions()
    options.add_argument("--no-sandbox")
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--headless')

    # 드라이버 불러오기
    path = '/home/sanghoon/Documents/Develop/chromedriver'

    driver = webdriver.Chrome(executable_path=path)
    driver.implicitly_wait(3)

    # 드라이버 get 메서드 호출하기
    driver.get("http://www.jobkorea.co.kr/recruit/joblist?menucode=search")

    # 회사명 (company name)
    cp_list = [ elem.text for elem in driver.find_elements_by_xpath('''//*[@id="dev-gi-list"]/div/div[5]/table/tbody/tr[1]/td[1]/a''') ]
    # //*[@id="dev-gi-list"]/div/div[5]/table/tbody/tr[3]/td[1]/a

    # 직업 소개
    job_list = [ elem.text for elem in driver.find_elements_by_xpath('''//*[@id="dev-gi-list"]/div/div[5]/table/tbody/tr[1]/td[2]/div/strong/a''') ]

    # 상세 주소
    url_list = [ elem.text for elem in driver.find_elements_by_xpath('''//*[@id="dev-gi-list"]/div/div[5]/table/tbody/tr[1]/td[3]/button/span''') ]
    # //*[@id="dev-gi-list"]/div/div[5]/table/tbody/tr[1]/td[2]/div/strong/a
    # //*[@id="dev-gi-list"]/div/div[5]/table/tbody/tr[3]/td[2]/div/strong/a


    # 결과 리스트
    item_list = list(zip(cp_list, job_list, url_list))

    # DB 저장하기
    client = ConnectSeleniumDB()
    for item in item_list:
        InsertSeleniumDB(client, item)
    client.close()

    # 종료하기
    driver.quit()

# main 함수 호출하기
if __name__ == "__main__":
    ReadJOBKOREA()