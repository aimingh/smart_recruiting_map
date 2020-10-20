from django.shortcuts import render
from jobMap.jobAPI import jobAPI

# Create your views here.

def job_map_search(requests):
    if len(requests.GET) !=0:
        keyword = requests.GET['key']
    else:
        keyword = 'AI'
    job = jobAPI()
    m = job.get_searchmap(keyword)
    datas = {'mountain_map':m}
    return render(requests, 'jobMap/job_map_search.html', context=datas)
