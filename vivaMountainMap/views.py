from django.shortcuts import render
from bs4 import BeautifulSoup
import requests
from pymongo import MongoClient

mountain_url = "https://www.forest.go.kr/kfsweb/kfi/kfs/foreston/main/contents/FmmntSrch/selectFmmntSrchList.do?mntIndex={0}&searchMnt=&searchCnd=&mn=NKFS_03_01_12&orgId=&mntUnit=10"
header = {'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36'} 
# Create your views here.

def main(requests):
    pass

def mountain_map(requests):
    pass

def info(request):
    mountain_list = dict()
    for i in range(1,11):
        res = requests.get(url=(mountain_url.format(i)),headers=header)
        soup = BeautifulSoup(res.content,features='lxml')
        lists = soup.find_all("#txt > ul li")
        


