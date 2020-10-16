from django.shortcuts import render
from pymongo import MongoClient
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse

import folium

# Create your views here.

def main(requests):
    pass

def mountain_map(requests):
    lat_long = [35.3369, 127.7306]
    m = folium.Map(lat_long, zoom_start=10)
    popText = folium.Html('<b>Jirisan</b><br>' + str(lat_long), script=True)
    popup = folium.Popup(popText, max_width=2650)
    folium.RegularPolygonMarker(location=lat_long, popup=popup).add_to(m)
    m = m._repr_html_()
    datas = {'mountain_map':m}
    return render(requests, 'vivaMountainMap/mountain_map.html', context=datas)

@csrf_exempt
def view_info(request,name):
    # if request.method == 'GET' :
    #     name = request.GET.get()

    with MongoClient("mongodb://172.17.0.3:27017") as my_client:
        data = dict()
        mountain = list(my_client.my_db.mountain_info.find({'name':name}))
        data['mountain'] = mountain

        if data['mountain'] == None:
            return HttpResponse("<h1> 해당되는 산의 이름이 없습니다 </h1>")
        
        return render(request,'vivaMountainMap/moun_info.html',context=data)
        