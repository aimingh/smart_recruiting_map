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
        self.client = MongoClient('mongodb://127.0.0.1:27017') 
        self.db = self.client.Jobdata

    def __del__(self):
        self.client.close()

    # jobkorea scrapping using searching keyword    
    def scrapping_jobkorea_search(self, max_page='10', keyword='AI'):
        if self.db.Joblist2.count()!=0:
            self.db.Joblist2.drop()
        for page in range(int(max_page)):
            res = requests.get(f'http://www.jobkorea.co.kr/Search/?stext={keyword}&tabType=recruit&Page_No={page}')
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

    def get_searchmap(self, keyword = 'AI', max_page='10', search_flag=False):
        if search_flag==True:
            self.scrapping_jobkorea_search(max_page=max_page, keyword=keyword)
        infolists = list(self.db.Joblist2.find())

        lat_long = [36, 127.4]
        m = folium.Map(lat_long, zoom_start=7, tiles='stamenterrain')

        for infolist in infolists:
            coord = [float(infolist['y']), float(infolist['x'])]
            info_mark = f'''<a href="{infolist["link"]}" target="_top"><b>{infolist["title"]}</b></a><br>
                            회사이름: {infolist['company']}<br>
                            '''
            popText = folium.Html(info_mark, script=True)
            popup = folium.Popup(popText, max_width=2650)
            icon =  folium.Icon(icon='building', prefix='fa') 
            folium.Marker(location=coord, popup=popup, icon=icon).add_to(m)
        m = m._repr_html_()
        return m

    def get_searchmap_cluster(self, keyword = 'AI', max_page='10', search_flag=False):
        if search_flag==True:
            self.scrapping_jobkorea_search(max_page=max_page, keyword=keyword)
        infolists = list(self.db.Joblist2.find())

        lat_long = [36, 127.4]
        m = folium.Map(lat_long, zoom_start=7, tiles='stamenterrain')

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
        m = m._repr_html_()
        return m

    def get_searchmap_heat(self, keyword = 'AI', max_page='10', search_flag=False):
        if search_flag==True:
            self.scrapping_jobkorea_search(max_page=max_page, keyword=keyword)
        infolists = list(self.db.Joblist2.find())

        lat_long = [36, 127.4]
        m = folium.Map(lat_long, zoom_start=7, tiles='stamentoner')

        data = []
        for infolist in infolists:
            data.append([float(infolist['y']), float(infolist['x'])])

        plugins.HeatMap(data).add_to(m)
        m = m._repr_html_()
        return m



    # def scrapping_jobkorea(self):
    #     # {'company':company,'address':address,'title':title,'work':work_content}
    #     pass

    # def insert_placeinfo(self):
    #     companylists = list(self.db.Joblist.find())
    #     placelist = []
    #     print('Start placeinfo')
    #     n = 0
    #     for companylist in companylists:
    #         n = n + 1
    #         if n==61:
    #             print()
    #         keyword = quote(companylist['address'])
    #         try:
    #             curl = f"https://dapi.kakao.com/v2/local/search/keyword.json?page=1&size=15&sort=accuracy&query={keyword}"
    #             res = requests.get(curl, headers = self.headers)
    #             if res.status_code==200:
    #                 documents = json.loads(res.text)['documents']
    #                 companylist['x'] = documents[0]['x']
    #                 companylist['y'] = documents[0]['y']
    #                 placelist.append(companylist)
    #         except Exception:
    #             curl = f"https://dapi.kakao.com/v2/local/search/address.json?page=1&size=10&query={keyword}"
    #             res = requests.get(curl, headers = self.headers)
    #             if res.status_code==200:
    #                 documents = json.loads(res.text)['documents']
    #                 companylist['x'] = documents[0]['x']
    #                 companylist['y'] = documents[0]['y']
    #                 placelist.append(companylist)

    #     if self.db.placelist.count() !=0:
    #         self.db.placelist.drop()
    #     print('Insert mongodb')
    #     self.db.placelist.insert_many(placelist)

    # def update_mongodb(self):
    #     '''DB update'''
    #     # self.scrapping_jobkorea()
    #     self.insert_placeinfo()

    # def get_companyinfo(self, keyword={}):
    #     infolists = list(self.db.placelist.find(keyword))
    #     return infolists

    # def get_map(self):
    #     ''' folium map에 DB정보를 기반으로 marker 추가후 지도 리턴'''
    #     lat_long = [36, 127.4]
    #     m = folium.Map(lat_long, zoom_start=7, tiles='stamenterrain')

    #     infolists = list(self.db.placelist.find())
    #     for infolist in infolists:
    #         coord = [float(infolist['y']), float(infolist['x'])]
    #         info_mark = f'''<a href='"{infolist["link"]}"'><b>{infolist["title"]}</b></a><br>
    #                         회사이름: {infolist['company']}<br>
    #                         '''
    #         popText = folium.Html(info_mark, script=True)
    #         popup = folium.Popup(popText, max_width=2650)
    #         icon =  folium.Icon(icon='building', prefix='fa') 
    #         folium.Marker(location=coord, popup=popup, icon=icon).add_to(m)
    #     m = m._repr_html_()
    #     return m

if __name__ == "__main__":
    ''' mongodb 업데이트 '''
    print('start update mongodb')
    jm = jobAPI()
    # jm.update_mongodb()
    jm.scrapping_jobkorea_search()