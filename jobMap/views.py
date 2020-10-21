from django.shortcuts import render
from jobMap.jobAPI import jobAPI
from pymongo import MongoClient
from django.core.paginator import Paginator

# Create your views here.
def get_form(requests):
    data = dict()
    if len(requests.GET) !=0:
        data['keyword'] = requests.GET['key']
        data['max_page'] = requests.GET['max_page']
        data['careerType'] = requests.GET['careerType']
        data['flag'] = True
    else:
        with MongoClient('mongodb://127.0.0.1:27017') as client:
            data = list(client.Jobdata.keyword.find())[0]
            data['flag'] = False
    return data

def job_map_search(requests):
    data = get_form(requests)
    job = jobAPI()
    m = job.get_searchmap(data)
    datas = {'mountain_map':m, 'data':data}
    return render(requests, 'jobMap/job_map_search.html', context=datas)

def job_map_search_cluster(requests):
    data = get_form(requests)
    job = jobAPI()
    m = job.get_searchmap_cluster(data)
    datas = {'mountain_map':m, 'data':data}
    return render(requests, 'jobMap/job_map_search.html', context=datas)

def job_map_search_heat(requests):
    data = get_form(requests)
    job = jobAPI()
    m = job.get_searchmap_heat(data)
    datas = {'mountain_map':m, 'data':data}
    return render(requests, 'jobMap/job_map_search.html', context=datas)

def listwithmongowithpaginator(request):
    data = request.GET.copy()
    with MongoClient('mongodb://127.0.0.1:27017/')  as client:
        Jobdata = client.Jobdata
        contact_list = list(Jobdata.Joblist2.find())			# get Collection with find()
        data['page_obj'] = contact_list
        for info in contact_list:
            print(info)
    paginator = Paginator(contact_list, 10) # Show 15 contacts per page.

    page_number = request.GET.get('page', 1)
    # page_number = page_number if page_number else 1 
    data['page_obj'] = paginator.get_page(page_number)

    for _ in data['page_obj']:
        print("{row['company']}, {row['title']}, {row['address']}")

    return render(request, 'jobMap/listwithmongowithpaginator.html', context=data)
