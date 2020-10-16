from bs4 import BeautifulSoup
import requests
from pymongo import MongoClient

header = {'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36'} 

mountain_url = "http://bac.blackyak.com/V5_challenge/default_ajax.asp?para1=114&para2=&para3=&para4=&para5=1&para6=all&_=1602831529924"
header = {'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36'} 
# Create your views here.  

res = requests.get(url=mountain_url,headers=header)
soup = BeautifulSoup(res.content,features='lxml')    
div_point = soup.find_all('div',{'class':'text'})
with  MongoClient("mongodb://172.17.0.3:27017") as my_client:
    for point in div_point:
        # get mountain name,cordinate,link from ajax page 
        p = point.find_all('a')
        name = p[0].text[1:]
        link = link = p[0].attrs['href']
        (x,y) = p[1].text.split(",")
        
        # get mountain information from link
        res_link = requests.get(url='http://bac.blackyak.com'+link)
        soup_link = BeautifulSoup(res_link.content,features='lxml')
        div_info = soup_link.find('div',{'class':'mgb20'})
        info_text = str(div_info.p.text).replace('\t','').replace('\r','').replace('\n','') 
        my_client.my_db.mountain_info.insert_one({'name':name,'info':info_text,'x':x,'y':y})
