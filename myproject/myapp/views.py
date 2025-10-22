from django.shortcuts import render,redirect

# Create your views here.
def root(request):
    return render(request,'registration.html')

def registration(request):
    return render(request,'registration.html')