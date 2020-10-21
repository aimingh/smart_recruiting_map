"""smart_recruiting_map URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from . import views

app_name = 'job'

urlpatterns = [
    path('job_map_search/', views.job_map_search, name ='job_map_search'),
    path('job_map_search_cluster/', views.job_map_search_cluster, name ='job_map_search_cluster'),
    path('job_map_search_heat/', views.job_map_search_heat, name ='job_map_search_heat'),
    path("job_map_search_list/", views.job_map_search_list, name ='job_map_search_list'),
]
