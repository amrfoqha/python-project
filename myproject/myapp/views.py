from django.shortcuts import render,redirect,HttpResponse
from .models import *
from .integration import analyze_user_data
from django.contrib import messages
import os
from django.core.files.storage import default_storage
from django.conf import settings
import json
import requests
from .models import User, Result
from docx import Document
import PyPDF2
from myproject import settings


def root(request):
    if 'logged_in' not in request.session:
        request.session['logged_in']=False
    if 'user_id' not in request.session:
        request.session['user_id']=None
    elif request.session['user_id'] :    
        context={
            'user':get_user_by_id(request.session['user_id'])
        }        
        return render(request,'home.html',context)
    return render(request,'home.html')
    
    

def view_register(request):
    
    return render(request,'registration.html')
def view_login(request):
    if request.session['logged_in']:
        return redirect('/view_quze')
    return render(request,'login.html')




def register(request):
    if create_new_user(request):
        return redirect('/view_login')
    return redirect('/view_register')



def login(request):
    if login_user(request):
        return redirect('/view_quze')
    return redirect('/view_login')


def view_quze(request):
    
    if request.session['logged_in'] :    
        context = {
            "user":get_user_by_id(request.session['user_id'])
        }
        return render(request,'quize.html',context)
    return redirect('/view_login')


def submit_quze(request):
    if submit_form(request):
        return redirect('/view_result')
    return redirect('/view_quze')

def result_view(request):
    
    if request.session['logged_in']:
        user=get_user_by_id(request.session['user_id'])
        result = Result.objects.filter(user=user).last()

        context = {
            "user": user,
            "result": result,
            "confidence_percentage":int(result.confidence_level*100),
            'companies':get_companies()
        }
        return render(request, "result.html", context) 
    return redirect('/')  






def submit_form(request):
    if request.method == "POST":
        
        user_id = request.session.get('user_id')
        if not user_id:
            messages.error(request, "User session expired. Please try again.")
            return redirect("/view_quze")

        quiz_data = request.POST.dict()  
        cv_summary = ""

        # قراءة ملف CV إذا موجود
        if "cv_file" in request.FILES:
            cv_file = request.FILES["cv_file"]
            if cv_file.name.endswith(".pdf"):
                reader = PyPDF2.PdfReader(cv_file)
                for page in reader.pages:
                    cv_summary += page.extract_text() + "\n"

        if not quiz_data and not cv_summary:
            messages.error(request, "Please fill the form or upload a CV.")
            return redirect("/view_quze")


        result = analyze_user_data(user_id, quiz_data if quiz_data else {}, cv_summary)

        try:
            full_data = json.loads(result.full_json)
        except:
            full_data = {}

        return redirect('/view_result')

    return redirect('/view_quze')



def view_cv_form(request):
    if request.session['logged_in'] :    
        context = {
            "user":get_user_by_id(request.session['user_id'])
        }
        return render(request,'cv_form.html',context)
    return redirect('/view_login')
    
def logout(request):
    del request.session['user_id']
    del request.session['logged_in']
    
    
    return redirect('/')

def profile(request):
    if 'toggle_form' not in request.session:
        request.session['toggle_form']=False
    if 'change_password' not in request.session:
        request.session['change_password']=False
    if request.session['logged_in']:
        context={
            'user':get_user_by_id(request.session['user_id']),
            'results':get_all_results(request.session['user_id']),
            'confidence':f"{get_average_confidence(request.session['user_id']):.2f}"
            
        }    
        return render(request,'profile.html',context)
    return redirect('/')

def edit_info(request):
    if change_info(request):
        return redirect('/toggle_edit_profile')
    return redirect('/profile')

def toggle_edit_profile(request):
    request.session['toggle_form']= not request.session['toggle_form']
    return redirect('/profile')

def toggle_change_password(request):
    request.session['change_password']= not request.session['change_password']
    return redirect('/profile')

def change_password(request):
    if change_password_check(request):
        return redirect('/toggle_change_password')
    else:
        return redirect('/profile')
    
def view_result_by_id(request,result_id):
    if request.session['logged_in']:
        user=get_user_by_id(request.session['user_id'])
        result = Result.objects.get(id=result_id)

        context = {
            "user": user,
            "result": result,
            "confidence_percentage":int(result.confidence_level*100),
            'companies':get_companies()
        }
        return render(request, "result.html", context) 
    return redirect('/')    