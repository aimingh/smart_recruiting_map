import pandas as pd
import requests, wget, os, json, folium
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
        '''블랙 야크 100대 명산 리스트 다운로드 후 mongodb에 삽입'''
        if os.path.exists('./data/mt100.xlsx') == False:
            print('Download mountainList (mt100.xlsx)')
            url = 'http://bac.blackyak.com/data/mt100.xlsx'
            wget.download(url, out='./data/')

        if self.db.mountainList.count() !=0:
            self.db.mountainList.drop()
        mountainList = pd.read_excel('./data/mt100.xlsx', header = 2)
        mountainList = mountainList.fillna('')
        # 예외를 위한 조치
        mountainList.iloc[60,1] ='오서산' # 오서산(보령)으로 kako 검색시 오서산 검색 안됨

        mountainList = mountainList.rename(columns={'번호':'no', '탐방지':'name', '인증봉우리':'peak' ,'높이(m)':'height', '지역':'area' ,'비고':'remarks'})
        print('Insert mongodb')
        self.db.mountainList.insert_many(mountainList.to_dict('records'))

    def insert_placeinfo(self):
        ''' 명산 리스트의 이름을 이용하여 장소 검색 (kakaoAPI) 후 mongodb 삽입 '''
        mountainList = list(self.db.mountainList.find({},{ "_id": 0, "no":1, "name": 1}))
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
                        document['no'] = mname['no']
                        placelist.append(document)
                        break
            else:
                print()
        if self.db.placelist.count() !=0:
            self.db.placelist.drop()
        print('Insert mongodb')
        self.db.placelist.insert_many(placelist)

    def insert_weather(self):
        ''' placeinfo 정보로 기상 정보 openweather API에서 검색 후 mongodb 삽입 '''
        placelist = list(self.db.placelist.find({},{ "_id": 0, "no":1 , "place_name":1, "name":1 , "x": 1, "y":1}))
        weatherlist = []
        print('Start wheather')
        for place in placelist:
            curl = f"http://api.openweathermap.org/data/2.5/weather?lat={place['y']}&lon={place['x']}&appid={self.openweather_APPKEY}"
            res = requests.get(curl)
            if res.status_code==200:
                document = json.loads(res.text)
                document['name'] = place['name']
                document['no'] = place['no']
                document['place_name'] = place['place_name']
                weatherlist.append(document)
        if self.db.weatherlist.count() !=0:
            self.db.weatherlist.drop()
        print('Insert mongodb')
        self.db.weatherlist.insert_many(weatherlist)

    def update_mongodb(self):
        '''DB update'''
        self.insert_mountainList()
        self.insert_placeinfo()
        self.insert_weather()

    def get_mountinfo(self):
        ''' 지도 mark에 입력할 명산 정보를 database에서 로드 '''
        infolists = list(self.db.weatherlist.find({},{ "_id": 0,"no":1, "place_name":1, "name":1, "weather":1, "main":{"temp":1}, "coord":1}))
        return infolists

    def get_map(self):
        ''' folium map에 DB정보를 기반으로 marker 추가후 지도 리턴'''
        lat_long = [36, 127.4]
        # m = folium.Map(lat_long, zoom_start=7)
        # m = folium.Map(lat_long, zoom_start=7, tiles='stamenterrain')
        m = folium.Map(lat_long, zoom_start=7, tiles='stamentoner')

        infolists = self.get_mountinfo()
        for infolist in infolists:
            coord = [infolist['coord']['lat'], infolist['coord']['lon']]
            # a tag target Attribute "https://www.w3schools.com/tags/att_a_target.asp" 참고
            info_mark = f'''<b>산이름: {infolist["name"]}</b><br>
                            좌표: {infolist['coord']['lat']:04f}, {infolist['coord']['lon']:04f}<br>
                            날씨: {infolist['weather'][0]['main']}<br>
                            기온: {infolist['main']['temp']}<br>
                            링크 : <a href=info/{infolist["name"]} target="_top">마우스 휠로 클릭</a>
                            '''
            popText = folium.Html(info_mark, script=True)
            popup = folium.Popup(popText, max_width=2650)
            # fontawsome에서 버전 4까지만 사용된다는 말이 있음, mountain은 나중에 추가됨
            # icon =  folium.Icon(icon='mountain', prefix='fa')
            icon_img = folium.features.CustomIcon('./data/greenmounticon.png', icon_size=(30,30))
            folium.Marker(location=coord, popup=popup, icon=icon_img).add_to(m)
        # folium 한글 깨짐 현상 발생시 아래 패키지 설치
        # pip install git+https://github.com/python-visualization/branca.git@master
        m = m._repr_html_()
        return m

if __name__ == "__main__":
    ''' mongodb 업데이트 '''
    print('start update mongodb')
    mt = mountainAPI()
    mt.update_mongodb()