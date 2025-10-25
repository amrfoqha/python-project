from django.urls import path
from . import views

urlpatterns =[
    path('',views.root,name='home'),
    path('view_register',views.view_register),
    path('view_login',views.view_login),
    path('login',views.login),
    path('register',views.register),
    path('view_quze',views.view_quze),
    path('view_result',views.result_view),
    path('view_cv_form',views.view_cv_form),
    path('submit_form',views.submit_quze),
    path('logout',views.logout),
    path('profile',views.profile),
    path('edit_info',views.edit_info),
    path('toggle_edit_profile',views.toggle_edit_profile),
    path('toggle_change_password',views.toggle_change_password),
    path('change_password',views.change_password),
    path('view_result/<int:result_id>',views.view_result_by_id),
    path('contact_us',views.contact_us),
    path('new_message',views.new_message)
    

]