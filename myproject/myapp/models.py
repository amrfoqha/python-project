import re
from django.db import models
from django.contrib import messages
import bcrypt
from django.db.models import Avg

class UserManager(models.Manager):
    def validator_login(self, postData):
        errors = {}
        if len(postData['email'])<=0:
            errors['email'] = "email must be filed"
        else:
            pattern = re.compile(r'^[a-z.A-Z0-9]+@[a-zA-Z]+.[a-zA-Z]+$')
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
            pattern = re.compile(r'^[a-z.A-Z0-9]+@[a-zA-Z]+.[a-zA-Z]+$')        
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
        if len(postData.get('q1', '').strip()) == 0:
            errors['q1'] = "Why did you choose to study IT? is required."
        if len(postData.get('q2', '').strip()) == 0:
            errors['q2'] = "Please specify your motivation for studying this field."
        if len(postData.get('q3', '').strip()) == 0:
            errors['q3'] = "Please list your IT fields of interest (comma separated)."
        if len(postData.get('q4', '').strip()) == 0:
            errors['q4'] = "Please describe your favorite subject or project."
        if len(postData.get('q5', '').strip()) == 0:
            errors['q5'] = "Please enter programming languages you are confident in."
        if len(postData.get('q6', '').strip()) == 0:
            errors['q6'] = "Describe a project you are proud of."
        if len(postData.get('q7', '').strip()) == 0:
            errors['q7'] = "Please list the tools or technologies you've used."
        if len(postData.get('q8', '').strip()) == 0:
            errors['q8'] = "Please describe any internships or part-time IT work."
        if len(postData.get('q9', '').strip()) == 0:
            errors['q9'] = "Please describe a technical challenge you solved."
        if len(postData.get('q10', '').strip()) == 0:
            errors['q10'] = "Please specify what kind of role you are aiming for."
        if postData.get('q11', '') not in ['Startup', 'Corporate', 'Freelance']:
            errors['q11'] = "Please select a valid work environment."
        if len(postData.get('q12', '').strip()) == 0:
            errors['q12'] = "Please list IT trends that interest you."
        if len(postData.get('q13', '').strip()) == 0:
            errors['q13'] = "Please specify how you stay updated with new technologies."
        if len(postData.get('q14', '').strip()) == 0:
            errors['q14'] = "Please describe how you handle teamwork."
        if len(postData.get('q15', '').strip()) == 0:
            errors['q15'] = "Please explain how you communicate technical info to non-tech people."
        if len(postData.get('q16', '').strip()) == 0:
            errors['q16'] = "Please describe how you handle pressure or deadlines."
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
            pattern = re.compile(r'^[a-z.A-Z0-9]+@[a-zA-Z]+.[a-zA-Z]+$')        
            if not pattern.match(postData['email']):
                errors['email'] = 'email is invalid'
            elif is_exists(postData['email']):
                errors['email'] = 'email is already exists'    
        if len(postData['phone'])<10:
            errors['phone'] = "inValid phone number"
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
    avatar=models.URLField(max_length=400,default="https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460_1280.png")
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

def is_exists_exclude(email):
    return User.objects.filter(email=email).exclude(id=request.session['user_id']).exists()


def submit_form(request):
        errors = User.objects.validator_form(request.POST)
        if len(errors) > 0:
            for key, val in errors.items():
                messages.error(request, val, extra_tags=f'form_{key}')
            return False
        else:
            messages.success(request, "Form submitted successfully!")
            return True

        



def get_all_results(user_id):
    return Result.objects.filter(user__id=user_id)

def get_average_confidence(user_id):
    avg=Result.objects.filter(user__id=user_id).aggregate(a=Avg('confidence_level'))
    return avg['a']

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

    print(list_of_companies)
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
        avatar=request.POST['avatar']
        user=get_user_by_id(request.session['user_id'])
        
        user.first_name=first_name
        user.last_name=last_name
        
        user.phone=phone
        user.location=location
        if avatar:
            user.avatar=avatar
        if email != user.email:
                user.email=email
        user.save()    
        return True
            