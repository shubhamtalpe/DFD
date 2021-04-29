from django.shortcuts import render,redirect
from django.http import HttpResponse

# Create your views here.

def home(request):
    return render(request, 'home.html', {'name': 'Shubham'})

def predict(request):
    if 'file_name' not in request.session:
        return redirect('/')

def mission(request):
    return render(request, 'mission.html')

def aboutus(request):
    return render(request, 'aboutus.html')