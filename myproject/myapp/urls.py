from django.urls import path
from . import views

urlpatterns =[

    path('',views.root),
    path('login',views.login)
    path('',views.home)
    

]