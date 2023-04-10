from django.shortcuts import render, redirect,reverse
from django.http import HttpResponseRedirect

import csv
from django.shortcuts import render, redirect
from .forms import CSVUploadForm
from .models import CSVFile
from os import listdir
from os.path import isfile, join

from csvreader_pro import settings
from django.views.generic.base import TemplateView

# Create your views here



def list_csv_files(request):
    data = []
    csv_files = CSVFile.objects.all()
    for csv_file in csv_files:
        file_data = {"header": [], "main": []}
        file_path = csv_file.csv_file.path
        with open(file_path, 'r') as f:
            rows_split = []
            csv_data = csv.reader(f)
            for column_name in csv_data:
                rows_split.append(column_name)
            print(rows_split)
            
            file_data["header"] = rows_split[0]
            for i in range(1, len(rows_split)):
                file_data["main"].append(rows_split[i])
        data.append(file_data)
    print("data", data)
    return render(request, 'list.html', {'csv_files': csv_files, 'data': data})


def upload_csv(request):
    # print(request)
    if request.method == 'POST':
        form = CSVUploadForm(request.POST, request.FILES)
        if form.is_valid():
            for csv_file in request.FILES.getlist('csv_files'):
                CSVFile.objects.create(csv_file=csv_file)
            return redirect('list_csv_files')
    else:
        form = CSVUploadForm()
    return render(request, 'upload.html', {'form': form})




def fileInfo(request):
    print(request.POST)
    if request.method == "POST":
            data = []
            file_data = {"header": [], "main": []}
            file_path = settings.MEDIA_ROOT + "/csv_files" + "/" + request.POST["filename"]
            user_column = request.POST.get("column").split(",")
            with open(file_path, 'r') as f:
                rows_split = []
                csv_data = csv.reader(f)
                for column_name in csv_data:
                    rows_split.append(column_name)
                file_data["header"] = rows_split[0]
                for i in range(1, len(rows_split)):
                    file_data["main"].append(rows_split[i])
            indx = []
            rows = []
            cols = []
            for i in file_data["header"]:
                if i in user_column:
                    indx.append(file_data["header"].index(i))
            for i in file_data["main"]:
                r = []
                for j in indx:
                    r.append(i[j])
                rows.append(r)
            file_data["header"] = user_column
            file_data["main"] = rows
            data.append(file_data)
    return render(request, "filedetail.html",{'data': data} )

def filter_the_column(request):
    context = {"myfiles": []}
    if request.method == "GET" : 
        media_path = settings.MEDIA_ROOT + "/csv_files"
        print(media_path)
        myfiles = [f for f in listdir(media_path) if isfile(join(media_path, f))]
        for f in myfiles:
            c = {}
            file_data = {"header": [], "main": []}
            file_path = media_path + "/" + f
            with open(file_path, 'r') as f:
                rows_split = []
                csv_data = csv.reader(f)
                for column_name in csv_data:
                    rows_split.append(column_name)
                file_data["header"] = rows_split[0]
                for i in range(1, len(rows_split)):
                    file_data["main"].append(rows_split[i])
            c[f.name.split("/")[-1]] = file_data
            context["myfiles"].append(c)
           
    return render(request, "filter_col.html",context)


