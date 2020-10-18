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

    def __del__(self):
        self.client.close()

    def insert_mountainList(self):
        # 블랙 야크 100대 명산 리스트 url 
        if os.path.exists('./data/mt100.xlsx') == False:
            print('Download mountainList (mt100.xlsx)')
            url = 'http://bac.blackyak.com/data/mt100.xlsx'
            wget.download(url, out='./data/')

        if self.db.mountainList.count() !=0:
            self.db.mountainList.drop()
        mountainList = pd.read_excel('./data/mt100.xlsx', header = 2)
        mountainList = mountainList.fillna('')
        # 예외를 위한 조치
        mountainList.iloc[60,1] ='오서산'

        mountainList = mountainList.rename(columns={'번호':'no', '탐방지':'name', '인증봉우리':'peak' ,'높이(m)':'height', '지역':'area' ,'비고':'remarks'})
        print('Insert mongodb')
        self.db.mountainList.insert_many(mountainList.to_dict('records'))

    def insert_placeinfo(self):
        mountainList = list(self.db.mountainList.find({},{ "_id": 0, "name": 1}))
        placelist = []
        print('Start placeinfo')
        n = 0
        for mname in mountainList:
            n = n + 1
            if n==61:
                print()
            keyword = quote(mname['name'])
            curl = f"https://dapi.kakao.com/v2/local/search/keyword.json?page=1&size=15&sort=accuracy&query={keyword}"
            headers = {"Authorization" : f"KakaoAK {self.KAKAOAPPKEY}"}
            res = requests.get(curl, headers = headers)
            if res.status_code==200:
                documents = json.loads(res.text)['documents']
                for document in documents:
                    if document['place_name'][-1] in ['산', '봉']:
                        document['name'] = mname['name']
                        placelist.append(document)
                        break
            else:
                print()
        if self.db.placelist.count() !=0:
            self.db.placelist.drop()
        print('Insert mongodb')
        self.db.placelist.insert_many(placelist)

    def insert_weather(self):
        placelist = list(self.db.placelist.find({},{ "_id": 0, "place_name":1, "name":1 , "x": 1, "y":1}))
        weatherlist = []
        print('Start wheather')
        for place in placelist:
            curl = f"http://api.openweathermap.org/data/2.5/weather?lat={place['y']}&lon={place['x']}&appid={self.openweather_APPKEY}"
            res = requests.get(curl)
            if res.status_code==200:
                document = json.loads(res.text)
                document['name'] = place['name']
                document['place_name'] = place['place_name']
                weatherlist.append(document)
        if self.db.weatherlist.count() !=0:
            self.db.weatherlist.drop()
        print('Insert mongodb')
        self.db.weatherlist.insert_many(weatherlist)

    def get_mountinfo(self):
        pass

if __name__ == "__main__":
    print('start')
    mt = mountainAPI()
    # mt.insert_mountainList()
    # mt.insert_placeinfo()
    # mt.insert_weather()
    mt.get_mountinfo()