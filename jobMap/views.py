from django.shortcuts import render
from jobMap.jobAPI import jobAPI
from pymongo import MongoClient
from django.core.paginator import Paginator

# Create your views here.
def get_form(requests):
    if len(requests.GET) !=0:
        keyword = requests.GET['key']
        max_page = requests.GET['max_page']
        flag = True
    else:
        keyword = ''
        max_page = ''
        flag = False
    return keyword, max_page, flag

def job_map_search(requests):
    keyword, max_page, flag = get_form(requests)
    job = jobAPI()
    m = job.get_searchmap(keyword=keyword, max_page=max_page, search_flag=flag)
    datas = {'mountain_map':m, 'keyword':keyword, 'max_page':max_page}
    return render(requests, 'jobMap/job_map_search.html', context=datas)

def job_map_search_cluster(requests):
    keyword, max_page, flag = get_form(requests)
    job = jobAPI()
    m = job.get_searchmap_cluster(keyword=keyword, max_page=max_page, search_flag=flag)
    datas = {'mountain_map':m, 'keyword':keyword, 'max_page':max_page}
    return render(requests, 'jobMap/job_map_search.html', context=datas)

def job_map_search_heat(requests):
    keyword, max_page, flag = get_form(requests)
    job = jobAPI()
    m = job.get_searchmap_heat(keyword=keyword, max_page=max_page, search_flag=flag)
    datas = {'mountain_map':m, 'keyword':keyword, 'max_page':max_page}
    return render(requests, 'jobMap/job_map_search.html', context=datas)

def listwithmongowithpaginator(request):
    data = request.GET.copy()
    with MongoClient('mongodb://127.0.0.1:27017/')  as client:
        my_db = client.my_db
        contact_list = list(my_db.job_list.find())			# get Collection with find()
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
