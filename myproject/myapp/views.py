from django.shortcuts import render,redirect,HttpResponse
from .models import *
from .integration import analyze_user_data
from django.contrib import messages
# Create your views here.
def root(request):
    return render(request,'home.html')

def view_register(request):
    All_message = {}
    for message in messages.get_messages(request):
        All_message[message.extra_tags] = str(message)
    print(All_message)
    return render(request,'registration.html',All_message)
def view_login(request):
    return render(request,'login.html')



def login(request):
    user=get_user_by_id(request.POST['email'],request.POST['password'])
    request.session['id']=user.id
    return HttpResponse("ahalan wa saaahlaaan be a3az 7babenaa")

def register(request):
    if create_new_user(request):
        return redirect('/quiz')
    else:
        return redirect('/view_register')
    
def view_result(request):
    return render(request,"result.html")    






def submit_quiz(request):
    if request.method == "POST":
        user_id = request.user.id

        quiz_data = {
            "background": request.POST.get("background", ""),
            "interest": request.POST.get("interest", ""),
            "project": request.POST.get("project", ""),
            "skills": request.POST.get("skills", ""),
            "experience": request.POST.get("experience", ""),
            "goals": request.POST.get("goals", ""),
            "work_type": request.POST.get("work_type", ""),
            "awareness": request.POST.get("awareness", ""),
            "soft_skills": request.POST.get("soft_skills", "")
        }


        cv_summary = request.POST.get("cv_summary", "").strip()

        has_quiz_answers = any(value.strip() for value in quiz_data.values())
        has_cv = bool(cv_summary)

        if not has_quiz_answers and not has_cv:
            messages.error(request, "Please answer the questions or upload your CV.")
            return render(request, "quiz.html")


        result = analyze_user_data(user_id, quiz_data if has_quiz_answers else {}, cv_summary if has_cv else "")

        return render(request, "result.html", {"result": result})

    return render(request, "quiz.html")

def view_cv_form(request):
    return render(request,'cv_form.html')