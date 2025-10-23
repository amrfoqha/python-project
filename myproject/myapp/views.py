from django.shortcuts import render,redirect,HttpResponse
from .models import *
# Create your views here.
def root(request):
    return render(request,'home.html')

def view_register(request):
    return render(request,'registration.html')
def view_login(request):
    return render(request,'login.html')




def register(request):
    if create_new_user(request):
        return redirect('/view_login')



def login(request):
    if login_user(request):
        return redirect('/view_quze')
    return redirect('/view_login')


def view_quze(request):
    return render(request,'quize.html')


def submit_quze(request):
    if submit_form(request):
        return redirect('/reslt')
    return redirect('/view_quze')