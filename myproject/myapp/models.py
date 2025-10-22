import re
from django.db import models
from django.contrib import messages
import bcrypt

class UserManager(models.Manager):
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
        if len(postData['phone'])<10:
            errors['phone'] = "inValid phone number"
        if len(postData['password'])==0:
            errors['password']='password should be filled'
        elif len(postData['password'])<8:
            errors['password'] = "should be at least 8 characters"
        if postData['password']!=postData['con_password']:
            errors['password'] = "password must be matched"
        return errors

# Create your models here.
class User(models.Model):
    first_name=models.CharField(max_length=45)
    last_name=models.CharField(max_length=45)
    email=models.EmailField(max_length=55)
    phone=models.CharField(max_length=15)
    location=models.CharField(max_length=100)
    password=models.CharField(max_length=45)
    level=models.IntegerField(max_length=5,default=1)
    avatar=models.URLField(max_length=400,default="https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460_1280.png")
    objects = UserManager()

class Result(models.Model):
    description=models.TextField()
    recomindation=models.CharField(max_length=100)
    user=models.ForeignKey(User,related_name='results',on_delete=models.CASCADE)
    result=models.CharField(max_length=100)

def get_user_by_id(email,password):
    return User.objects.get(email=email,password=password)


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