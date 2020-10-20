import pandas as pd
import requests, wget, os, json, folium
from urllib.parse import quote
from pymongo import MongoClient

class jobAPI:
    def __init__(self):
        self.KAKAOAPPKEY = 'e872972db3d44f41a166d59a90196511'
        self.client = MongoClient('mongodb://127.0.0.1:27017') 
        self.db = self.client.Jobdata

    def __del__(self):
        self.client.close()

    def scrapping_jobkorea(self):
        # {'company':company,'address':address,'title':title,'work':work_content}
        pass

    def insert_placeinfo(self):
        companylists = list(self.db.JobList.find())
        placelist = []
        print('Start placeinfo')
        n = 0
        for companylist in companylists:
            n = n + 1
            if n==61:
                print()
            keyword = quote(companylist['address'])
            curl = f"https://dapi.kakao.com/v2/local/search/address.json?page=1&size=10&query={keyword}"
            headers = {"Authorization" : f"KakaoAK {self.KAKAOAPPKEY}"}
            res = requests.get(curl, headers = headers)
            if res.status_code==200:
                documents = json.loads(res.text)['documents']
                companylist['x'] = documents['x']
                companylist['y'] = documents['y']
                placelist.append(companylist)

        if self.db.placelist.count() !=0:
            self.db.placelist.drop()
        print('Insert mongodb')
        self.db.placelist.insert_many(placelist)

    def update_mongodb(self):
        '''DB update'''
        self.scrapping_jobkorea()
        self.insert_placeinfo()

    def get_companyinfo(self, keyword={}):
        infolists = list(self.db.placelist.find(keyword))
        return infolists

    def get_map(self):
        ''' folium map에 DB정보를 기반으로 marker 추가후 지도 리턴'''
        lat_long = [36, 127.4]
        m = folium.Map(lat_long, zoom_start=7, tiles='stamenterrain')

        infolists = list(self.db.placelist.find())
        for infolist in infolists:
            coord = [infolist['y'], infolist['x']]
            info_mark = f'''<b>{infolist["title"]}</b><br>
                            회사이름: {infolist['company']}<br>
                            '''
            popText = folium.Html(info_mark, script=True)
            popup = folium.Popup(popText, max_width=2650)
            icon =  folium.Icon(icon='building', prefix='fa') 
            folium.Marker(location=coord, popup=popup, icon=icon).add_to(m)
        m = m._repr_html_()
        return m

if __name__ == "__main__":
    ''' mongodb 업데이트 '''
    print('start update mongodb')
    jm = jobAPI()
    jm.update_mongodb()