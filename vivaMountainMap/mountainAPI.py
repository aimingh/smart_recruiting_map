import pandas as pd
import requests, wget, os, json
from urllib.parse import quote
from pymongo import MongoClient


class mountainAPI:
    def __init__(self):
        self.APPKEY = 'e872972db3d44f41a166d59a90196511'
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
        df = pd.DataFrame()
        for mname in mountainList:
            keyword = quote(mname['탐방지'])
            curl = f"https://dapi.kakao.com/v2/local/search/keyword.json?page=1&size=15&sort=accuracy&query={keyword}"
            headers = {"Authorization" : f"KakaoAK {self.APPKEY}"}
            res = requests.get(curl, headers = headers)
            result = json.loads(res.text)['documents'][0]

            print()

if __name__ == "__main__":
    mt = mountainAPI()
    mt.get_placeinfo()