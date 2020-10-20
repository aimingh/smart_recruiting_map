
from django.shortcuts import render
from pymongo import MongoClient
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from vivaMountainMap.mountainAPI import mountainAPI

import folium

url ='https://naveropenapi.apigw.ntruss.com/map-static/v2/raster'
headers={"X-NCP-APIGW-API-KEY-ID":"pyqaswux4u","X-NCP-APIGW-API-KEY":"BHD3BVoKqXuDP5TFujb0zxJIfeAU5YXy5fpCeSXk"}

# Create your views here.

def main(requests):
    pass

def mountain_map(requests):
    mt = mountainAPI()
    m = mt.get_map()
    datas = {'mountain_map':m}
    print('im in')
    return render(requests, 'vivaMountainMap/mountain_map.html', context=datas)

@csrf_exempt
def view_info(request,no):
    # if request.method == 'GET' :
    #     name = request.GET.get()

    with MongoClient("mongodb://127.0.0.1:27017") as my_client:
        data = dict()
        mountain = list(my_client.my_db.mountain_info.find({'no':no}))
        data['mountain'] = mountain

        if data['mountain'] == None:
            return HttpResponse("<h1> 해당되는 산의 이름이 없습니다 </h1>")
        
        return render(request,'vivaMountainMap/moun_info.html',context=data)
        