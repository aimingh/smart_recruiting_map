from django.shortcuts import render
from pymongo import MongoClient

# Create your views here.
def listwithmongowithpaginator(request):
    data = request.GET.copy()
    with MongoClient('mongodb://127.0.0.1:27017/')  as client:
        my_db = client.my_db
        contact_list = list(my_db.job_list.find())			# get Collection with find()
        data['page_obj'] = contact_list
    # paginator = Paginator(contact_list, 10) # Show 15 contacts per page.

    # page_number = request.GET.get('page', 1)
    # # page_number = page_number if page_number else 1 
    # data['page_obj'] = paginator.get_page(page_number)

    # for row in data['page_obj']:
    #     print(f"{row['name'], {row['title']}, {row['link']}")

    return render(request, 'jobMap/listwithmongowithpaginator.html', context=data)