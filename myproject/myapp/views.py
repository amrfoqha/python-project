from django.shortcuts import render,redirect,HttpResponse
from .models import *
# Create your views here.
def root(request):
    return render(request,'home.html')

def view_register(request):
    return render(request,'registration.html')
def view_login(request):
    return render(request,'login.html')



def login(request):
    user=get_user_by_id(request.POST['email'],request.POST['password'])
    request.session['id']=user.id
    return HttpResponse("ahalan wa saaahlaaan be a3az 7babenaa")

def register(request):
    if create_new_user(request):
        return redirect('/quiz')