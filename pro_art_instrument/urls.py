
 
from django.urls import path
from . import views

urlpatterns = [
    path('pro_home',views.home,name='pro_home'),
    path('addinstruments', views.addinstruments, name="addinstruments"),
    path('update_instrument_details/<id>', views.update_instrument_details, name="update_instrument_details"),
    path('artgrantrequest/<Event_id>', views.artgrantrequest, name="artgrantrequest"),
    path('upload_image/<Event_id>', views.upload_image, name="upload_image"),
   
    
]
