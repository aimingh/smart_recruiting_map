from django.shortcuts import render
from jobMap.jobAPI import jobAPI
from pymongo import MongoClient
from django.core.paginator import Paginator

# Create your views here.
def get_form(requests):
    data = dict()
    if len(requests.GET) >=3:
        data['keyword'] = requests.GET['key']
        data['max_page'] = requests.GET['max_page']
        data['careerType'] = requests.GET['careerType']
        data['flag'] = True
    else:
        # with MongoClient('mongodb://127.0.0.1:27017') as client:
            # data = list(client.Jobdata.keyword.find())[0]
        with MongoClient('mongodb://192.168.0.225:27017') as client:
            data = list(client.Jobinfo.keyword.find())[0]
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

def paging(request, datalist, num=10):
    page = request.GET.get('page', '1')
    paginator = Paginator(datalist, num)
    page_obj = paginator.get_page(page)
    page = int(page)
    maxpage = num*((page-1)//num)+10
    minpage = num*((page-1)//num)+1
    return page_obj, maxpage, minpage

def job_map_search_list(requests):
    data = get_form(requests)
    job = jobAPI()
    if data['flag']==True:
        job.scrapping_jobkorea_search(data)
        if job.db.keyword.count()!=0:
            job.db.keyword.drop()
        job.db.keyword.insert_one(data)

    with MongoClient('mongodb://192.168.0.225:27017')  as client:
        Jobdata = client.Jobinfo
        contact_list = list(Jobdata.Joblist2.find())			# get Collection with find()

    page_obj, maxpage, minpage = paging(requests, contact_list)    
    data['page_obj'] = page_obj
    data['maxpage'] = maxpage
    data['minpage'] = minpage

    return render(requests, 'jobMap/job_map_search_list.html', context=data)

def job_map_all(requests):
    data = get_form(requests)
    job = jobAPI()
    m = job.get_allmap_heat(data)
    datas = {'mountain_map':m, 'data':data}
    return render(requests, 'jobMap/job_map_all.html', context=datas)

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
