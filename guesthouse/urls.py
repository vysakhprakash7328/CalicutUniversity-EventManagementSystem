from django.urls import path
from . import views

urlpatterns = [
    path('guesthome', views.guest_home, name="guest_home"),
    path('addrooms', views.add_rooms, name="addrooms"),
    path('accomodation', views.accomodation, name="accomodation"),
    path('update/<room_id>', views.update_rooms, name="update_rooms"),
    path('bookings', views.bookings, name="bookings"),
    path('mybookings', views.mybookings, name="mybookings"),
    path('bookroom', views.bookroom, name="bookroom"),
    path('allbookings', views.allbookings, name="allbookings"),
    path('roomcancel/<bookid>', views.roomcancel, name="roomcancel"),
    path('aprovebooking/<bookid>', views.aprovebooking, name="aprovebooking"),
    path('deletebooking/<bookid>', views.deletebooking, name="deletebooking"),
    path('editbooking/<bookid>', views.editbooking, name="editbooking"),
    path('edit/<bookid>', views.edit, name="edit"),






     





    # path('delete/<room_id>', views.delete_rooms, name="delete_rooms"),
    





    
]