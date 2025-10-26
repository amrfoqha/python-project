import re
from django.db import models
from django.contrib import messages
import bcrypt
from django.db.models import Avg
from django.shortcuts import render, redirect
import requests

class UserManager(models.Manager):
    def validator_login(self, postData):
        errors = {}
        if len(postData['email'])<=0:
            errors['email'] = "email must be filed"
        else:
            pattern = re.compile(r'^[a-z.-_A-Z0-9]+@[a-zA-Z]+.[a-zA-Z]+$')
            if not pattern.match(postData['email']):
                errors['email'] = 'Wrong password or email'
            elif not is_exists(postData['email']):
                errors['email'] = 'Wrong password or email'
            elif len(postData['password'])==0:
                errors['password']='password should be filled'
            elif len(postData['password'])<8:
                errors['password'] = "Wrong password or email"
        return errors
    def validator_reg(self, postData):
        errors = {}
        if len(postData['first_name']) <= 0 :
            errors['first_name'] = "Name must be filed"
        if len(postData['last_name'])=="":
            errors['last_name']="Name must be filed"
        if len(postData['email'])<=0:
            errors['email']='email must be filled'
        else:    
            pattern = re.compile(r'^[a-z.-_A-Z0-9]+@[a-zA-Z]+.[a-zA-Z]+$')        
            if not pattern.match(postData['email']):
                errors['email'] = 'email is invalid'
            elif is_exists(postData['email']):
                errors['email'] = 'email is already exists'    
        if len(postData['phone'])<10:
            errors['phone'] = "inValid phone number"
        if len(postData['password'])==0:
            errors['password']='password should be filled'
        elif len(postData['password'])<8:
            errors['password'] = "Password should be at least 8 characters"
        if postData['password']!=postData['con_password']:
            errors['password'] = "password must be matched"
        return errors
    def validator_form(self,postData):
        errors = {}
        if len(postData.get('background', '').strip()) == 0:
            errors['background'] = "Why did you choose to study IT? is required."
        if len(postData.get('interest', '').strip()) == 0:
            errors['interest'] = "Which IT fields interest you most? is required."
        if len(postData.get('project', '').strip()) == 0:
            errors['project'] = "What was your favorite subject or project and why? is required."
        if len(postData.get('skills', '').strip()) == 0:
            errors['skills'] = "Which programming languages are you confident in? is required."
        if len(postData.get('experience', '').strip()) == 0:
            errors['experience'] = "What personal or academic project are you proud of? is required."
        if len(postData.get('goals', '').strip()) == 0:
            errors['goals'] = "Career Goals & Vision. is required."
        if len(postData.get('work_type', '').strip()) == 0:
            errors['work_type'] = "Preferred Work Type.is required"
        if len(postData.get('awareness', '').strip()) == 0:
            errors['awareness'] = "What IT trends interest you most right now?. is required."
        if len(postData.get('soft_skills', '').strip()) == 0:
            errors['soft_skill'] = "How do you handle teamwork?. is required."
        return errors
    
    def validator_change_password(self, postData):
        errors = {}
        if len(postData['new_password'])<=0:
            errors['new_password'] = "Password must be filled"
        elif  len(postData['new_password'])<=8:   
            errors['new_password'] = "Password must be at least 8 characters"
        elif len(postData['confirm_password'])<=0:
            errors['confirm_password'] = "Password must be filled"
        elif len(postData['confirm_password'])<=8:   
            errors['new_password'] = "Password must be at least 8 characters"      
        elif postData['new_password'] != postData['confirm_password']:
                errors['password'] = "Password not matched"
        return errors
    def validator_change_info(self, postData):
        errors = {}
        if len(postData['first_name']) <= 0 :
            errors['first_name'] = "Name must be filed"
        if len(postData['last_name'])<=0:
            errors['last_name']="Name must be filed"
        if len(postData['email'])<=0:
            errors['email']='email must be filled'
        else:    
            pattern = re.compile(r'^[a-z.-_A-Z0-9]+@[a-zA-Z]+.[a-zA-Z]+$')        
            if not pattern.match(postData['email']):
                errors['email'] = 'email is invalid'
        if len(postData['phone'])<10:
            errors['phone'] = "inValid phone number"
        return errors
    
    def validator_edit_info(self, postData):
        errors = {}
        if len(postData['first_name']) <= 0 :
            errors['first_name'] = "Name must be filed"
        if len(postData['last_name'])<=0:
            errors['last_name']="Name must be filed"
        if len(postData['phone'])<10:
            errors['phone'] = "inValid phone number"
        if len(postData['email'])<=0:
            errors['email']='email must be filled'    
        return errors
    
    def validator_message(self,postData,logged_in):
        errors = {}
        if not logged_in : 
            if len(postData['name']) <= 0 :
                errors['name'] = "Name must be filed"
            if len(postData['email'])<=0:
                errors['email']='email must be filled'
            else:    
                pattern = re.compile(r'^[a-z.-_A-Z0-9]+@[a-zA-Z]+.[a-zA-Z]+$')        
                if not pattern.match(postData['email']):
                    errors['email'] = 'email is invalid'
                    
        if len(postData['message']) <=0 :
            errors['message']='message must be filed'
        
        return errors

        
# Create your models here.
class User(models.Model):
    first_name=models.CharField(max_length=45)
    last_name=models.CharField(max_length=45)
    email=models.EmailField(max_length=55)
    phone=models.CharField(max_length=15)
    location=models.CharField(max_length=100)
    password=models.CharField(max_length=255)
    level=models.IntegerField(default=1)
    avatar=models.FileField(upload_to='uploads/',default='uploads/blank-profile-picture-973460_1280.webp')
    objects = UserManager()
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

class Result(models.Model):
    career_recommendation=models.TextField()
    confidence_level=models.FloatField(null=True, blank=True)
    key_strengths=models.TextField(null=True, blank=True)
    personality_traits=models.TextField(null=True, blank=True)
    nearest_companies=models.TextField(null=True, blank=True)
    reasoning=models.TextField(null=True, blank=True)
    recommended_skills_to_learn=models.TextField(null=True, blank=True)
    growth_opportunities=models.TextField()
    user=models.ForeignKey(User,related_name='results',on_delete=models.CASCADE)
    objects = UserManager()
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    

class Message(models.Model):
    message=models.TextField()
    name=models.CharField(max_length=45)
    email=models.EmailField()
    objects = UserManager()
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)


def get_user_by_id(user_id):
    return User.objects.get(id=user_id)

def create_user(first_name, last_name, email,phone,location, password,level):
    User.objects.create(first_name=first_name,last_name=last_name, email=email, phone=phone,location=location, password=password,level=level)


def create_new_user(request):
    email=request.POST['email']
    first_name=request.POST['first_name']
    last_name=request.POST['last_name']
    password=request.POST['password']
    phone=request.POST['phone']
    location=request.POST['location']
    errors=User.objects.validator_reg(request.POST)
    if len(errors)>0:
        for key,val in errors.items():
            messages.error(request,val,f'reg_{key}')
        return False
    hash1=bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    user=User.objects.create(email=email,first_name=first_name,last_name=last_name,password=hash1,phone=phone,location=location)
    return True        


def get_user_by_id(user_id):
    return User.objects.get(id=user_id)

def search_email(email):
    return User.objects.filter(email=email)[0]
def login_user(request):
    email=request.POST['email']
    password=request.POST['password']
    errors=User.objects.validator_login(request.POST)
    if len(errors)>0:
        for key,val in errors.items():
            messages.error(request,val,f'log_{key}')
        return False
    user=search_email(email)
    if bcrypt.checkpw(password.encode(),user.password.encode()):
        request.session['logged_in']=True
        request.session['user_id']=user.id
        return True
    else:
        messages.error(request,'Wrong password or email','log_password')
        return False



def is_exists(email):
    return User.objects.filter(email=email).exists()


def is_exists_exclude(email,user_id):
    return User.objects.filter(email=email).exclude(id=user_id).exists()



def check_form(request):

        errors = User.objects.validator_form(request.POST)
        if len(errors) > 0:
            for key, val in errors.items():
                messages.error(request, val, extra_tags=f'form_{key}')
            return False
        else:
            messages.success(request, "Form submitted successfully!")
            return True


def get_resilt(id):
    user =User.objects.get(id=id)
    return user.results


def get_all_results(user_id):
    return Result.objects.filter(user__id=user_id)

def get_average_confidence(user_id):
    avg=Result.objects.filter(user__id=user_id).aggregate(a=Avg('confidence_level'))
    if avg['a']:  
        return avg['a']
    return 0

def get_companies():
    res=Result.objects.last()
    company_list = res.nearest_companies.split('%')
    list_of_companies = []

    for el in company_list:
        arr = el.strip().split('-')
        name = arr[0].strip()

        roles = [r.strip() for r in arr[1].split(',')] if len(arr) > 1 else []
        
        list_of_companies.append({
            'name': name,
            'roles': roles
        })
    return list_of_companies

def change_password_check(request):
    object=UserManager()
    errors=object.validator_change_password(request.POST)
    if len(errors)>0:
        for key,val in errors.items():
            messages.error(request,val,extra_tags=f"change_pass__{key}")
        return False
    else:
        user=get_user_by_id(request.session['user_id'])
        hash_pass=bcrypt.hashpw(request.POST['new_password'].encode(),bcrypt.gensalt()).decode()
        user.password= hash_pass
        user.save()
        return True
    
def change_info(request):    
    object=UserManager()
    errors=object.validator_change_info(request.POST)
    if len(errors)>0:
        for key,val in errors.items():
            messages.error(request,val,extra_tags=f"change_info__{key}")
        return False
    else:
        first_name=request.POST['first_name']
        last_name=request.POST['last_name']
        email=request.POST['email']
        phone=request.POST['phone']
        location=request.POST['location']
        user=get_user_by_id(request.session['user_id'])
        new_avatar=request.FILES.get('img')
        if new_avatar:
            uploaded_file = new_avatar
            
            user.avatar=uploaded_file
        
        user.first_name=first_name
        user.last_name=last_name
        
        user.phone=phone
        user.location=location
        if email != user.email:
            if is_exists(email):
                messages.error(request,'email is already exists',extra_tags="change_info__email")
                return False
            else:
                user.email=email
        user.save()    
        return True
            
            
def is_admin(user_id):
    user=get_user_by_id(user_id)
    if user.level== 2:
        return True
    return False            

def get_all_client():
    return User.objects.filter(level="1")

def del_user(id):
    user=get_user_by_id(id)
    user.delete()
    return

def modify_user(request, id):
    object = UserManager()
    errors = object.validator_edit_info(request.POST)
    if errors:
        for key, val in errors.items():
            messages.error(request, val, extra_tags=f"edit_info__{key}")
        return False
    else:
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        phone = request.POST['phone']
        location = request.POST['location']

        user = get_user_by_id(id)
        user.first_name = first_name
        user.last_name = last_name
        user.phone = phone
        user.location = location
        if is_exists_exclude(email,id):
            messages.error(request, 'Email already exists', extra_tags="edit_info__email")
            return False
        else:
            user.email = email

        user.save()
        return True





def create_new_message(request):

    logged_in=request.session['logged_in']
    if "name" in request.POST:
        name=request.POST['name']
    else:
        user=get_user_by_id(request.session['user_id'])
        name=f'{user.first_name} {user.last_name}' 
    if "email" in request.POST:
        email=request.POST['email']
    else:
        user=get_user_by_id(request.session['user_id'])
        email=user.email
               
    errors=Message.objects.validator_message(request.POST,logged_in)
    if len(errors)>0:
        for key,val in errors.items():
            messages.error(request,val,f'message_{key}')
        return False
    message=request.POST['message']
    Message.objects.create(name=name,email=email,message=message)
    return True 

def get_all_messages():
    return Message.objects.all()