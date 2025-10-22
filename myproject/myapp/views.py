from django.shortcuts import render,redirect,HttpResponse
from .models import *
# Create your views here.
def root(request):
    
    return render(request,'main.html')

def registration(request):
    return render(request,'registration.html')


def login(request):
    user=get_user_by_id(request.POST['email'],request.POST['password'])
    request.session['id']=user.id
    return HttpResponse("ahalan wa saaahlaaan be a3az 7babenaa")
from django.shortcuts import render

def home(request):
    return render(request,'home.html') 
