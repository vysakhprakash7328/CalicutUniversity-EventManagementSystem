
from django.urls import path
from . import views

urlpatterns = [
    path('login_user', views.login_user, name="login"),
    path('logout_user', views.logout_user, name='logout'),
    path('add_main_users', views.add_main_users, name='add_main_users'),

    path('departmentrequest',views.dep_request,name='dep_request'),
       
    
    path('add_department/<id>',views.add_department,name='add_department'),


    path('account_settings',views.account_settings,name='account_settings')

    
]