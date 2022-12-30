
from django.urls import path
from . import views

urlpatterns = [
    path('publichome', views.public_home, name="public_home"),
    path('publicregister', views.public_register, name="public_register"),
    path('publiclogin', views.public_login, name="public_login"),
    path('pending_varification', views.pending_varification, name="pending_varification"),


    
]