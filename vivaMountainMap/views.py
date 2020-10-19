from . import mountainAPI
from django.shortcuts import render
from pymongo import MongoClient
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse

import folium


# Create your views here.

def main(requests):
    pass

def mountain_map(requests):
    #mt = mountainAPI.mountainAPI()
    #m = mt.get_map()
    datas = {'mountain_map':m}
    return render(requests, 'vivaMountainMap/mountain_map.html', context=datas)

@csrf_exempt
def view_info(request,name):
    # if request.method == 'GET' :
    #     name = request.GET.get()

    with MongoClient("mongodb://127.0.0.1:27017") as my_client:
        data = dict()
        mountain = list(my_client.my_db.mountain_info.find({'name':name}))
        data['mountain'] = mountain

        if data['mountain'] == None:
            return HttpResponse("<h1> 해당되는 산의 이름이 없습니다 </h1>")
        
        return render(request,'vivaMountainMap/moun_info.html',context=data)
        