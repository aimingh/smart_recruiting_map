from django.shortcuts import render
import folium
from pymongo import MongoClient

# Create your views here.


def job_map(requests):
    return render(requests, 'jobMap/job_map.html', context=datas)

