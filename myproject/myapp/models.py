import re
from django.db import models
class UserManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        if len(postData['first_name'])=="":
            errors['first_name'] = "first_name empity"
        if len(postData['last_name'])=="":
            errors['last_name']="last_name empity"
        pattern = re.compile(r'^[a-z.A-Z0-9]+@[a-zA-Z]+.[a-zA-Z]+$')
        if not pattern.match(postData['reg_email']):
            errors['invalid_email'] = 'email is invalid'
        if len(postData['phone'])<10:
            errors['phone'] = "shode be 10 numper"
        if len(postData['location'])=="":
            errors['location'] = "location empity"
        if len(postData['password'])<8:
            errors['password'] = "shode be 8ch"
        if len(postData['level'])=="":
            errors['level'] = "level empity"
        return errors

# Create your models here.
class User(models.Model):
    first_name=models.CharField(max_length=45)
    last_name=models.CharField(max_length=45)
    email=models.EmailField(max_length=55)
    phone=models.CharField(max_length=15)
    location=models.CharField(max_length=100)
    password=models.CharField(max_length=45)
    level=models.IntegerField(max_length=5)
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