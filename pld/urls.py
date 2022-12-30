

from django.urls import path
from . import views

urlpatterns = [
    path('home', views.home,name="home"),
    path('', views.homepage,name="homepage"),
    path('view_venue',views.view_venues,name="view_venue"),
    path('add_venue/',views.add_venue,name="add_venue"),
    path('show_venue/<venue_id>',views.singlevenue,name="singlevenue"),
    path('update_venue/<venue_id>',views.update_venue,name="updatevenue"),
    path('delete_venue/<venue_id>',views.delete_venue,name="delete_venue"),

    path('all_event',views.all_event,name="all_event"),
    path('create_event',views.create_event,name="create_event"),
    path('singlevent/<Event_id>',views.singlevent,name="singlevent"),
    path('edit_event/<Event_id>',views.edit_event,name="edit_event"),
    path('delete_event/<Event_id>',views.delete_event,name="delete_event"),   
    path('priority_event',views.priority_event,name="priority_event"),

    path('my_events',views.my_events,name="my_events"),
    path('my_venues',views.my_venues,name="my_venues"),


    
    path('view_users',views.view_users,name="view_users"),  
    path('view_single_user',views.view_single_user,name="view_single_user"),  
    path('change_user_settings/<user_id>',views.change_user_settings,name="change_user_settings"),
    path('createuser/<head_id>',views.create_user,name='create_user'),  
    path('createunion/<union_id>',views.create_union,name='create_union'),

    #Approval function url

    path('approved/<Event_id>',views.event_approved,name='event_approved'),
    path('trackevent',views.track_event,name='track_event'),
    path('searchevents',views.search_events,name='search_events'),
    path('pdfreport',views.pdf_report,name='pdf_report'),
    path('hallreport',views.hall_report,name='hall_report'),
    path('cancelevent/<Event_id>',views.cancelevent,name='cancelevent'),
    path('reqresubmission/<Event_id>',views.reqresubmission,name='reqresubmission'),
    path('GeneratePdf/<Event_id>', views.GeneratePdf,name='GeneratePdf'),   
    path('cancel/<Event_id>', views.cancel,name='cancel'),
    path('forgot_password',views.forgot_password,name='forgot_password'),   
    path('setpassword/<email>',views.setpassword,name='setpassword'),  






    path('event_log/<operation><person><person_category><event_id>',views.event_log,name='event_log'),   
    path('log_records',views.log_records,name='log_records'),   

    path('Event_brochure/<Event_id>',views.Event_brochure,name="Event_brochure"),
    path('Event_brochurehome/<Event_id>',views.Event_brochurehome,name="Event_brochurehome"),
    path('upload/<Event_id>',views.upload,name='upload'),
    path('pdf_report_dep',views.pdf_report_dep,name='pdf_report_dep')





    
]