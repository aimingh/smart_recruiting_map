from bs4 import BeautifulSoup
import requests
from pymongo import MongoClient


# --------------------------------------- for 100 mountain in Korea -----------------------------------------------------------------
mountain_url = "http://bac.blackyak.com/V5_challenge/default_ajax.asp?para1=114&para2=&para3=&para4=&para5=1&para6=all&_=1602831529924"
header = {'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36'} 
# Create your views here.  

res = requests.get(url=mountain_url,headers=header)

soup = BeautifulSoup(res.content,features='lxml')    
div_point = soup.find_all('div',{'class':'text'})

with  MongoClient("mongodb://127.0.0.1:27017") as my_client:
    my_client.Mountain.mountain_info.drop()
    id = 1
    for point in div_point:
        # get mountain name,cordinate,link from ajax page 
        p = point.find_all('a')
        name = p[0].text[1:]        
        link = link = p[0].attrs['href']
        (x,y) = p[1].text.split(",")
        res_img = requests.get(url="http://bac.blackyak.com/"+p[0]['href'])
        soup_img = BeautifulSoup(res_img.content,features='lxml') 
        img = soup_img.select('#swipers_gap > div.swiper-wrapper > div > img')
        img_link = img[0]['src']
        
        # get mountain information from link
        #swipers_gap > div.swiper-wrapper > div > img

        res_link = requests.get(url='http://bac.blackyak.com'+link)
        soup_link = BeautifulSoup(res_link.content,features='lxml')
        div_info = soup_link.find('div',{'class':'mgb20'})
        info_text = str(div_info.p.text).replace('\t','').replace('\r','').replace('\n','') 
        my_client.Mountain.mountain_info.insert_one({'no':id,'name':name,'img':img_link,'info':info_text,'x':x,'y':y})
        print(id)
        id+=1

## ------------------------------------------------- for read map from naver API ---------------------------------------------------------------------

# url ='https://naveropenapi.apigw.ntruss.com/map-static/v2/raster'
# headers={"X-NCP-APIGW-API-KEY-ID":"pyqaswux4u","X-NCP-APIGW-API-KEY":"BHD3BVoKqXuDP5TFujb0zxJIfeAU5YXy5fpCeSXk"}


