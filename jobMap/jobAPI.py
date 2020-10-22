import pandas as pd
import requests, wget, os, json, folium, datetime
from urllib.parse import quote
from pymongo import MongoClient
from bs4 import BeautifulSoup
from folium import plugins

class jobAPI:
    def __init__(self):
        KAKAOAPPKEY = 'e872972db3d44f41a166d59a90196511'
        self.headers = {"Authorization" : f"KakaoAK {KAKAOAPPKEY}"}
        # self.client = MongoClient('mongodb://127.0.0.1:27017') # localhost
        self.client = MongoClient('mongodb://192.168.0.134:8088')
        self.db = self.client.Jobinfo

    def __del__(self):
        self.client.close()

    # jobkorea scrapping using searching keyword    
    def scrapping_jobkorea_search(self, searchdata):
        if self.db.Joblist2.count()!=0:
            self.db.Joblist2.drop()
        for page in range(1,int(searchdata['max_page'])+1):
            res = requests.get(f'''http://www.jobkorea.co.kr/Search/?stext={searchdata['keyword']}&tabType=recruit&careerType={searchdata['careerType']}&Page_No={page}''')
            if res.status_code == 200:
                soup = BeautifulSoup(res.content, 'lxml')
                links = soup.find_all('a', class_='title dev_view')
                companies = soup.find_all('a', class_='name dev_view')
                data = []
                for link, company in zip(links, companies):
                    title = link.get_text()
                    title = title.strip('\r\n').strip().replace("`", "")
                    link = 'http://www.jobkorea.co.kr' + link.get('href')
                    company_name = company.get_text()
                    address, x, y = self.get_place(company_name)
                    if address!=None:
                        dic = {"title": title, "link": link, "company":company_name, "address":address, "x":x, "y":y, "create_date": datetime.datetime.now()}
                        data.append(dic)
            self.db.Joblist2.insert_many(data)

    # get coordination of point and address
    def get_place(self, keyword):
        keyword2 = quote(keyword)
        curl = f"https://dapi.kakao.com/v2/local/search/keyword.json?page=1&size=1&sort=accuracy&query={keyword2}"
        res = requests.get(curl, headers = self.headers)
        if res.status_code==200:
            documents = json.loads(res.text)['documents']
            if documents==[]:
                return None, None, None
            x = documents[0]['x']
            y = documents[0]['y']
            if documents[0]['road_address_name'] !="":
                address = documents[0]['road_address_name']
            else:
                address = documents[0]['address_name']
            return address, x, y
        else:
            return None, None, None

    def get_searchmap(self, data):
        if data['flag']==True:
            self.scrapping_jobkorea_search(data)
            if self.db.keyword.count()!=0:
                self.db.keyword.drop()
            self.db.keyword.insert_one(data)
        infolists = list(self.db.Joblist2.find())

        lat_long = [36, 127.4]
        m = folium.Map(lat_long, zoom_start=7, tiles='openstreetmap')

        for infolist in infolists:
            coord = [float(infolist['y']), float(infolist['x'])]
            info_mark = f'''<a href="{infolist["link"]}" target="_top"><b>{infolist["title"]}</b></a><br>
                            회사이름: {infolist['company']}<br>
                            '''
            popText = folium.Html(info_mark, script=True)
            popup = folium.Popup(popText, max_width=2650)
            icon =  folium.Icon(icon='building', prefix='fa') 
            folium.Marker(location=coord, popup=popup, icon=icon).add_to(m)
        
        folium.TileLayer('openstreetmap').add_to(m)
        folium.TileLayer('Stamenterrain').add_to(m)
        folium.TileLayer('stamentoner').add_to(m)
        folium.TileLayer('Stamenwatercolor').add_to(m)
        folium.TileLayer('cartodbpositron').add_to(m)
        folium.TileLayer('cartodbdark_matter').add_to(m)
        folium.LayerControl().add_to(m)
        
        m = m._repr_html_()
        return m

    def get_searchmap_cluster(self, data):
        if data['flag']==True:
            self.scrapping_jobkorea_search(data)
            if self.db.keyword.count()!=0:
                self.db.keyword.drop()
            self.db.keyword.insert_one(data)
        infolists = list(self.db.Joblist2.find())

        lat_long = [36, 127.4]
        m = folium.Map(lat_long, zoom_start=7, tiles='openstreetmap')

        marker_cluster = plugins.MarkerCluster().add_to(m)
        for infolist in infolists:
            coord = [float(infolist['y']), float(infolist['x'])]
            info_mark = f'''<a href="{infolist["link"]}" target="_top"><b>{infolist["title"]}</b></a><br>
                            회사이름: {infolist['company']}<br>
                            '''
            popText = folium.Html(info_mark, script=True)
            popup = folium.Popup(popText, max_width=2650)
            icon =  folium.Icon(icon='building', prefix='fa') 
            folium.Marker(location=coord, popup=popup, icon=icon,).add_to(marker_cluster)
        
        folium.TileLayer('openstreetmap').add_to(m)
        folium.TileLayer('Stamenterrain').add_to(m)
        folium.TileLayer('stamentoner').add_to(m)
        folium.TileLayer('Stamenwatercolor').add_to(m)
        folium.TileLayer('cartodbpositron').add_to(m)
        folium.TileLayer('cartodbdark_matter').add_to(m)
        folium.LayerControl().add_to(m)
        
        m = m._repr_html_()
        return m

    def get_searchmap_heat(self, data):
        if data['flag']==True:
            self.scrapping_jobkorea_search(data)
            if self.db.keyword.count()!=0:
                self.db.keyword.drop()
            self.db.keyword.insert_one(data)
        infolists = list(self.db.Joblist2.find())

        lat_long = [36, 127.4]
        m = folium.Map(lat_long, zoom_start=7, tiles='stamentoner')

        data = []
        for infolist in infolists:
            data.append([float(infolist['y']), float(infolist['x'])])

        plugins.HeatMap(data).add_to(m)

        folium.TileLayer('openstreetmap').add_to(m)
        folium.TileLayer('Stamenterrain').add_to(m)
        folium.TileLayer('stamentoner').add_to(m)
        folium.TileLayer('Stamenwatercolor').add_to(m)
        folium.TileLayer('cartodbpositron').add_to(m)
        folium.TileLayer('cartodbdark_matter').add_to(m)
        folium.LayerControl().add_to(m)
        
        m = m._repr_html_()
        return m

    def get_allplace(self):
        infolists = list(self.db.Joblist.find())
        data = []
        for infolist in infolists:
            print(infolist['address'])
            address = quote(infolist['address'])
            if len(infolist['address'].split(' '))>3:
                curl = f"https://dapi.kakao.com/v2/local/search/address.json?page=1&size=10&query={address}"
                res = requests.get(curl, headers = self.headers)
                if res.status_code==200:
                    try:
                        documents = json.loads(res.text)['documents']
                        infolist['x'] = documents[0]['x']
                        infolist['y'] = documents[0]['y']
                        data.append(infolist)
                    except Exception:
                        pass
            else:
                keyword = quote(infolist['company'])
                curl = f"https://dapi.kakao.com/v2/local/search/keyword.json?page=1&size=1&sort=accuracy&query={keyword}"
                res = requests.get(curl, headers = self.headers)
                if res.status_code==200:
                    try:
                        documents = json.loads(res.text)['documents']
                        infolist['x'] = documents[0]['x']
                        infolist['y'] = documents[0]['y']
                        data.append(infolist)
                    except Exception:
                        pass
        self.db.alljob.insert_many(data)

    def get_allmap_heat(self, data):
        infolists = list(self.db.alljob.find())

        lat_long = [36, 127.4]
        m = folium.Map(lat_long, zoom_start=7, tiles='stamentoner')

        data = []
        for infolist in infolists:
            data.append([float(infolist['y']), float(infolist['x'])])

        plugins.HeatMap(data, max_val=5.0, radius=18, blur=15).add_to(m)

        folium.TileLayer('openstreetmap').add_to(m)
        folium.TileLayer('Stamenterrain').add_to(m)
        folium.TileLayer('stamentoner').add_to(m)
        folium.TileLayer('Stamenwatercolor').add_to(m)
        folium.TileLayer('cartodbpositron').add_to(m)
        folium.TileLayer('cartodbdark_matter').add_to(m)
        folium.LayerControl().add_to(m)
        
        m = m._repr_html_()
        return m

if __name__ == "__main__":
    ''' mongodb 업데이트 '''
    print('start update mongodb')
    jm = jobAPI()
    # jm.update_mongodb()
    #jm.scrapping_jobkorea_search()
    # jm.get_allplace()