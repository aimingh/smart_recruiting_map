
from django.shortcuts import render
from pymongo import MongoClient
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from vivaMountainMap.mountainAPI import mountainAPI
from django.core.paginator import Paginator
import folium

url ='https://naveropenapi.apigw.ntruss.com/map-static/v2/raster'
headers={"X-NCP-APIGW-API-KEY-ID":"pyqaswux4u","X-NCP-APIGW-API-KEY":"BHD3BVoKqXuDP5TFujb0zxJIfeAU5YXy5fpCeSXk"}

# Create your views here.

def paging(request, datalist, num=10):
    page = request.GET.get('page', '1')
    paginator = Paginator(datalist, num)
    page_obj = paginator.get_page(page)
    page = int(page)
    maxpage = num*((page-1)//num)+10
    minpage = num*((page-1)//num)+1
    return page_obj, maxpage, minpage

def mountain_map(requests):
    mt = mountainAPI()
    m = mt.get_map()
    with MongoClient("mongodb://127.0.0.1:27017") as client:
        db = client.Mountain
        mountain_info = list(db.mountain_info.find())
        mountainList = list(db.mountainList.find())
        for i in range(len(mountain_info)):
            mountainList[i]['img'] =  mountain_info[i]['img']
    page_obj, maxpage, minpage = paging(requests, mountainList)  
    datas = {'mountain_map':m, 'page_obj':page_obj, 'maxpage':maxpage, 'minpage':minpage}
    return render(requests, 'vivaMountainMap/mountain_map.html', context=datas)

@csrf_exempt
def view_info(request,no):
    # if request.method == 'GET' :
    #     name = request.GET.get()

    with MongoClient("mongodb://127.0.0.1:27017") as my_client:
        data = dict()
        mountain = list(my_client.my_db.mountain_info.find({'no':no}))
        mt = mountainAPI()
        m = mt.get_one_map(no)
        data['mountain'] = mountain
        data['mountain_map'] = m
        if data['mountain'] == None:
            return HttpResponse("<h1> 해당되는 산의 이름이 없습니다 </h1>")
        return render(request,'vivaMountainMap/moun_info.html',context=data)
        