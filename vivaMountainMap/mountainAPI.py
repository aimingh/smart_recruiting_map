import pandas as pd
import requests, wget, os, json
from urllib.parse import quote
from pymongo import MongoClient


class mountainAPI:
    def __init__(self):
        self.KAKAOAPPKEY = 'e872972db3d44f41a166d59a90196511'
        self.openweather_APPKEY = '62bc63d111fc64124ac69bf2ad6b36f8'
        self.client = MongoClient('mongodb://127.0.0.1:27017') 
        self.db = self.client.Mountain
        self.insert_mountainList()
        print()

    def __del__(self):
        self.client.close()

    def insert_mountainList(self):
        # 블랙 야크 100대 명산 리스트 url 
        if os.path.exists('./data/mt100.xlsx') == False:
            url = 'http://bac.blackyak.com/data/mt100.xlsx'
            wget.download(url, out='./data/')

        if self.db.mountainList.count()==0:
            mountainList = pd.read_excel('./data/mt100.xlsx', header = 2)
            mountainList = mountainList.fillna('')
            self.db.mountainList.insert_many(mountainList.to_dict('records'))

    def get_placeinfo(self):
        mountainList = list(self.db.mountainList.find({},{ "_id": 0, "탐방지": 1}))
        placelist = []
        for mname in mountainList:
            keyword = quote(mname['탐방지'])
            curl = f"https://dapi.kakao.com/v2/local/search/keyword.json?page=1&size=15&sort=accuracy&query={keyword}"
            headers = {"Authorization" : f"KakaoAK {self.KAKAOAPPKEY}"}
            res = requests.get(curl, headers = headers)
            if res.status_code==200:
                documents = json.loads(res.text)['documents']
                for document in documents:
                    if document['place_name'][-1] in ['산', '봉']:
                        placelist.append(document)
                        break
        if self.db.placelist.count() !=0:
            self.db.placelist.drop()
        self.db.placelist.insert_many(placelist)

    def get_weather(self):
        placelist = list(self.db.placelist.find({},{ "_id": 0, "place_name":1, "x": 1, "y":1}))
        weatherlist = []
        for place in placelist:
            curl = f"http://api.openweathermap.org/data/2.5/weather?lat={place['y']}&lon={place['x']}&appid={self.openweather_APPKEY}"
            res = requests.get(curl)
            if res.status_code==200:
                document = json.loads(res.text)
                weatherlist.append(document)
        self.db.weatherlist.insert_many(weatherlist)

if __name__ == "__main__":
    mt = mountainAPI()
    mt.get_weather()