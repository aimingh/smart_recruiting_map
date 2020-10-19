import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
import time
from urllib.parse import quote
header = {'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36'}
url_true='http://www.jobkorea.co.kr/recruit/joblist?menucode=cotype1&cotype=1,2,3,4,5?Page='
i = 1
with MongoClient("mongodb://127.0.0.1:27017") as my_client:        
    while True:
        print(i)
        res = requests.get(url=(url_true+str(i)),headers=header)
        print(res.url)
        soup = BeautifulSoup(res.content,'html5lib')

        if soup == None :
            break

        cpnames = soup.select(selector='#dev-gi-list > div > div.tplList.tplJobList > table > tbody > tr')

    
        for cpname in cpnames:
            name = (cpname.select('td.tplCo > a')[0].get_text())
            title = (cpname.select('td.tplTit > div > strong > a')[0].get_text())
            
            link = 'http://www.jobkorea.co.kr/'+(cpname.select('td.tplTit > div > strong > a')[0]['href'])
            res_company = requests.get(url=link,headers=header)
            soup_tmp = BeautifulSoup(res_company.content,'html5lib')
            try :
                strong_add = soup_tmp.select("#mapDtl")
                address = strong_add[0].text
            except Exception :
                address = "홈페이지 지원"      
            print(name,title,address,link)
            time.sleep(0.4)

        i = i+1
        
            #my_client.my_db.job_list.insert_one({"company":name,"title":title,"address":address,"link":link})

