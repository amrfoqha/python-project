from django.urls import path
from . import views

urlpatterns =[
    path('',views.root),
    path('view_register',views.view_register),
    path('view_login',views.view_login),
    path('login',views.login),
    path('register',views.register),
    path('view_quze',views.view_quze),
]