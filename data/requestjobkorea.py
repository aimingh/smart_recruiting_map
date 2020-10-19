import requests
from bs4 import BeautifulSoup

header = {'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36'}
url_true='http://www.jobkorea.co.kr/recruit/joblist?menucode=cotype1&cotype=1,2,3,4,5'
res = requests.get(url=url_true,headers=header)

# print(res.status_code)
# print(res.content)
soup = BeautifulSoup(res.content,'html5lib')


cpnames = soup.select(selector='#dev-gi-list > div > div.tplList.tplJobList > table > tbody > tr')
#dev-gi-list > div > div.tplList.tplJobList > table > tbody > tr:nth-child(1)

for cpname in cpnames:
    name = (cpname.select('td.tplCo > a')[0].get_text())
    #dev-gi-list > div > div.tplList.tplJobList.smTableList > table > tbody > tr:nth-child(3) > td.tplCo > a
    #dev-gi-list > div > div.tplList.tplJobList.smTableList > table > tbody > tr:nth-child(4) > td.tplCo > a
    title = (cpname.select('td.tplTit > div > strong > a')[0].get_text())
    #dev-gi-list > div > div.tplList.tplJobList > table > tbody > tr:nth-child(1) > td.tplTit > div > strong > a
    link = 'http://www.jobkorea.co.kr/'+(cpname.select('td.tplTit > div > strong > a')[0]['href'])
    #dev-gi-list > div > div.tplList.tplJobList.smTableList > table > tbody > tr:nth-child(7) > td.tplTit > div > strong > a
    print(name,title,link)

    # <a href="/Recruit/Co_Read/C/dmi161207" class="link normalLog" data-clickctgrcode="B01" target="_blank">두산 모빌리티 이노베이션</a>
    # <a href="/Recruit/Co_Read/C/koreaaero1" class="link normalLog" data-clickctgrcode="B01" target="_blank">한국항공우주산업㈜</a>
    