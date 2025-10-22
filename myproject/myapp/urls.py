from django.urls import path
from . import views

urlpatterns =[
    path('',views.root),
    path('view_register',views.registration),
]