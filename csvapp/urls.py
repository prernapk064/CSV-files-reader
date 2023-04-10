from django.contrib import admin
from django.urls import path
from csvapp import views

urlpatterns = [
    
    path("",views.upload_csv, name='upload_csv'),
    path('list/',views.list_csv_files, name='list_csv_files'),
    path("filter/",views.filter_the_column, name='filter_the_column'),
    path('filedetail/',views.fileInfo, name='fileinfo'),
    
]
