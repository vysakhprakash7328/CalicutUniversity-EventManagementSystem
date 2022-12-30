from django.urls import path
from . import views

urlpatterns = [
 
    path('union_request',views.union_request,name="union_request"),
    path('union_home',views.union_home,name="union_home"),
    

    
]