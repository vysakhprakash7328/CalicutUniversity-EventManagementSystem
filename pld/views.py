from genericpath import exists
from itertools import chain
from operator import gt, lt

from typing import Type
from unicodedata import category
from django.shortcuts import redirect, render
from requests import request, session

from Unions.models import unions
from pro_art_instrument.models import instrument_details
from .models import Event_log, Event_registration, EventCategory, Hall_details, track
from .forms import   CategoryForm, DepartmentRequest, High_priority_eventForm, PublicEventForm, UnionRequests, VenueForm
from .forms import  EventForm, EventFormAdmin
from django.contrib.auth.models import User
from users.models import Department, DepartmentHead, Main_accounts
from public.models import public_registration

from django.conf import settings
from django.core.mail import send_mail
import datetime
from django.http import FileResponse
from fpdf import FPDF

from django.http import HttpResponse
from django.views.generic import View
from .process import html_to_pdf 
from django.contrib import messages
from django.utils.crypto import get_random_string





# Create your views here.
def home(request):
    users = User.objects.all()
    if request.session.get('mainuserid'):
        id=request.session['mainuserid']
        user=request.session['mainusername']

        if Main_accounts.objects.filter(pk=id,varification_choices='Non Varification'):
            obj1=Main_accounts.objects.get(pk=id,varification_choices='Non Varification')

            if obj1.type == 'GUEST HOUSE':
                return redirect('guest_home')
            elif obj1.type :
                return redirect('pro_home')
            return render(request,'pld/home.html',{'user':user,'proid':obj1,})
        elif Main_accounts.objects.filter(pk=id,varification_choices='Varification'):
            obj=Main_accounts.objects.get(pk=id,varification_choices='Varification')
            if obj.type:
                ev = track.objects.filter(approved_by = obj.type, status = 0)
                event=Event_registration.objects.all()
                vari_users=Main_accounts.objects.filter(varification_choices = 'Varification')
                check = track.objects.filter(status = 0)
                print(check)
                print(vari_users)
                


          
                return render(request,'pld/home.html',{'user':user,'mainuserid':obj,'events':event,'eve':ev,'variusers':vari_users,'check':check})
            
        return render(request,'pld/home.html',{'user':user,'mainuserid':obj})
    elif users.exists():
        dep=DepartmentHead.objects.filter(status=0)
        union=unions.objects.filter(status=0)
        vari_users=Main_accounts.objects.filter(varification_choices = 'Varification')

        ev = track.objects.filter(approved_by = 'PLD', status = 0)
        events=Event_registration.objects.all()
        return render(request,'pld/home.html',{'events':events,'eve':ev,'dep':dep,'union':union,'variusers':vari_users})

    elif request.session.get('unionid'):
    
        return redirect('Department')
    elif request.session.get('publicid'):
       
        return redirect('public_home')
    
    
def homepage(request):
    hall = Hall_details.objects.all()
    events = Event_registration.objects.filter(Event_status = 1).order_by('Event_startDate')
    today = datetime.datetime.now().date()
    venue = Hall_details.objects.all()
    return render(request,'Hometemplate/index.html',{'hall':hall,'events':events,'today':today,'venue':venue})


def view_venues(request):
    venues=Hall_details.objects.all()
    if request.session.get('id'):
        id=request.session['id']
        user=request.session['department_username']
        return render(request,'pld/venueDetails.html',{'venues':venues,'user':user,'depid':id})
    elif request.session.get('head_id'):
        id=request.session['head_id']
        user=request.session['head_username']
        return render(request,'pld/venueDetails.html',{'venues':venues,'user':user,'headid':id})
    elif request.session.get('mainuserid'):
        id=request.session['mainuserid']
        user=request.session['mainusername']
        return render(request,'pld/venueDetails.html',{'venues':venues,'user':user,'mainuserid':id,'proid':id,'user':user})
    elif request.session.get('unionid'):
        id=request.session['unionid']
        user=request.session['unionname']
        return render(request,'pld/venueDetails.html',{'venues':venues,'user':user,'unionid':id})
    elif request.session.get('publicid'):
        public_events=Hall_details.objects.filter(public_view=True)
        id=request.session['publicid']
        user=request.session['publicname']
        return render(request,'pld/venueDetails.html',{'venues':public_events,'user':user,'publicid':id})


    else:
        return render(request,'pld/venueDetails.html',{'venues':venues})

   
def event_approved(request,Event_id):
    users = User.objects.all()
    if request.method == 'POST':
        sendto = request.POST['approvedby']
        approved_on = datetime.datetime.now() 
        if request.session.get('head_id'):
            id=request.session['head_id']
            head_name = request.session['head_username']
            dep=Department.objects.get(head_ids = id)
            ev = Event_registration.objects.get(Event_id = Event_id)
            ev_start = Event_registration.objects.filter(Event_venue = ev.Event_venue,Event_startDate__range=[ev.Event_startDate,ev.Event_endDate],Event_status = 0).exclude(Event_id = Event_id)
            ev_end = Event_registration.objects.filter(Event_venue = ev.Event_venue,Event_endDate__range=[ev.Event_startDate,ev.Event_endDate],Event_status = 0).exclude(Event_id = Event_id)
            ev_outstart = Event_registration.objects.filter(Event_venue = ev.Event_venue,Event_startDate__lte = ev.Event_startDate,Event_endDate__gte = ev.Event_endDate,Event_status = 0).exclude(Event_id = ev.Event_id)
        
            obj = list(chain(ev_start,ev_end,ev_outstart))
            obj1=[*set(obj)]
            if sendto == 'approved':
                track.objects.filter(approved_by = dep.department_name,event_id = Event_id).update(approved_on = approved_on,status = 1,remarks = 'Approved')
                Event_registration.objects.filter(pk = Event_id).update(Event_status = 1,waiting_list = 1)
                for i in obj1:
                    Event_registration.objects.filter(Event_id = i.Event_id).update(waiting_list = 2)
                operation = "EVENT APPROVED"
                person = head_name
                person_category = "DEPARTMENT HEAD"
                Event_id = Event_id
                event_log(operation,person,person_category,Event_id)
                                
                return redirect('Department')
            else:
            
                track.objects.filter(event_id = Event_id , approved_by = dep.department_name).update(approved_on = approved_on,status = 1)
                track(event_id = Event_id, approved_by = sendto).save()
                operation = "EVENT REQUEST SENT TO "+ sendto
                person = head_name
                person_category = "DEPARTMENT HEAD"
                Event_id = Event_id
                event_log(operation,person,person_category,Event_id)
                return redirect('Department')
    
        elif request.session.get('mainuserid'):
            mainid=request.session['mainuserid']
            print(mainid)
            main=Main_accounts.objects.get(pk = mainid)
            if sendto == 'approved':
                track.objects.filter(event_id = Event_id , approved_by = main.type).update(approved_on = approved_on,status = 1,remarks = 'Approved')
                Event_registration.objects.filter(pk = Event_id).update(Event_status = 1)
                operation = "EVENT APPROVED"
                person = main.type
                person_category = "MAIN USERS"
                Event_id = Event_id
                event_log(operation,person,person_category,Event_id)
                return redirect('home')
            else:
                track.objects.filter(event_id = Event_id , approved_by = main.type).update(approved_on = approved_on,status = 1)
                track(event_id = Event_id, approved_by = sendto).save()
                operation = "EVENT REQUEST SENT TO"+ sendto
                person = main.type
                person_category = "MAIN USERS"
                Event_id = Event_id
                event_log(operation,person,person_category,Event_id)
                
                return redirect('home')
        elif users.exists():
            ev = Event_registration.objects.get(Event_id = Event_id)
            ev_start = Event_registration.objects.filter(Event_venue = ev.Event_venue,Event_startDate__range=[ev.Event_startDate,ev.Event_endDate],Event_status = 0).exclude(Event_id = Event_id)
            ev_end = Event_registration.objects.filter(Event_venue = ev.Event_venue,Event_endDate__range=[ev.Event_startDate,ev.Event_endDate],Event_status = 0).exclude(Event_id = Event_id)
            ev_outstart = Event_registration.objects.filter(Event_venue = ev.Event_venue,Event_startDate__lte = ev.Event_startDate,Event_endDate__gte = ev.Event_endDate,Event_status = 0).exclude(Event_id = ev.Event_id)
        
            obj = list(chain(ev_start,ev_end,ev_outstart))
            obj1=[*set(obj)]
                
        
            if sendto == 'approved':
                track.objects.filter(event_id = Event_id , approved_by = 'PLD').update(approved_on = approved_on,status = 1,remarks = 'Approved')
                Event_registration.objects.filter(pk = Event_id).update(Event_status = 1,waiting_list = 1)
                for i in obj1:
                    Event_registration.objects.filter(Event_id = i.Event_id).update(waiting_list = 2)
                operation = "EVENT APPROVED"
                person = "PLD"
                person_category = "ADMIN"
                Event_id = Event_id
                event_log(operation,person,person_category,Event_id)
                return redirect('home')
            else:
                track.objects.filter(event_id = Event_id , approved_by = 'PLD').update(approved_on = approved_on,status = 1)
                track(event_id = Event_id, approved_by = sendto).save()
                Event_registration.objects.filter(pk = Event_id).update(waiting_list = 1)
                operation = "EVENT REQUEST SENT TO"+sendto
                person = "PLD"
                person_category = "ADMIN"
                Event_id = Event_id
                event_log(operation,person,person_category,Event_id)
                for i in obj1:
                    Event_registration.objects.filter(Event_id = i.Event_id).update(waiting_list = 2)


            return redirect('home')
    return redirect('home')




def cancelevent(request,Event_id):
    users = User.objects.all()
    if  request.method == 'POST':
        reason = request.POST['reason']
        print(reason)
        approved_on = datetime.datetime.now() 
        if request.session.get('head_id'):
            id=request.session['head_id']
            head=DepartmentHead.objects.get(pk = id)
            ev = Event_registration.objects.get(Event_id = Event_id)
            ev_start = Event_registration.objects.filter(Event_venue = ev.Event_venue,Event_startDate__range=[ev.Event_startDate,ev.Event_endDate],Event_status = 0).exclude(Event_id = Event_id)
            ev_end = Event_registration.objects.filter(Event_venue = ev.Event_venue,Event_endDate__range=[ev.Event_startDate,ev.Event_endDate],Event_status = 0).exclude(Event_id = Event_id)
            ev_outstart = Event_registration.objects.filter(Event_venue = ev.Event_venue,Event_startDate__lte = ev.Event_startDate,Event_endDate__gte = ev.Event_endDate,Event_status = 0).exclude(Event_id = ev.Event_id)
        
            obj = list(chain(ev_start,ev_end,ev_outstart))
            obj1=[*set(obj)]
            track.objects.filter(approved_by = head.department_name,event_id = Event_id).update(approved_on = approved_on,status = 2,remarks = reason)
            Event_registration.objects.filter(pk = Event_id).update(Event_status = 2,waiting_list = 0)
            for i in obj1:
                Event_registration.objects.filter(Event_id = i.Event_id).update(waiting_list = 0)
            return redirect('Department')
        

        elif request.session.get('mainuserid'):
            mainid=request.session['mainuserid']
            main=Main_accounts.objects.get(pk = mainid)
            ev = Event_registration.objects.get(Event_id = Event_id)
            ev_start = Event_registration.objects.filter(Event_venue = ev.Event_venue,Event_startDate__range=[ev.Event_startDate,ev.Event_endDate],Event_status = 0).exclude(Event_id = Event_id)
            ev_end = Event_registration.objects.filter(Event_venue = ev.Event_venue,Event_endDate__range=[ev.Event_startDate,ev.Event_endDate],Event_status = 0).exclude(Event_id = Event_id)
            ev_outstart = Event_registration.objects.filter(Event_venue = ev.Event_venue,Event_startDate__lte = ev.Event_startDate,Event_endDate__gte = ev.Event_endDate,Event_status = 0).exclude(Event_id = ev.Event_id)
        
            obj = list(chain(ev_start,ev_end,ev_outstart))
            obj1=[*set(obj)]
            track.objects.filter(event_id = Event_id , approved_by = main.type).update(approved_on = approved_on,status = 2,remarks = reason)
            Event_registration.objects.filter(pk = Event_id).update(Event_status = 2,waiting_list = 0)
            for i in obj1:
                Event_registration.objects.filter(Event_id = i.Event_id).update(waiting_list = 0)
            return redirect('home')
        
        elif users.exists():
            ev = Event_registration.objects.get(Event_id = Event_id)
            ev_start = Event_registration.objects.filter(Event_venue = ev.Event_venue,Event_startDate__range=[ev.Event_startDate,ev.Event_endDate],Event_status = 0).exclude(Event_id = Event_id)
            ev_end = Event_registration.objects.filter(Event_venue = ev.Event_venue,Event_endDate__range=[ev.Event_startDate,ev.Event_endDate],Event_status = 0).exclude(Event_id = Event_id)
            ev_outstart = Event_registration.objects.filter(Event_venue = ev.Event_venue,Event_startDate__lte = ev.Event_startDate,Event_endDate__gte = ev.Event_endDate,Event_status = 0).exclude(Event_id = ev.Event_id)
        
            obj = list(chain(ev_start,ev_end,ev_outstart))
                
            obj1=[*set(obj)]
            track.objects.filter(event_id = Event_id , approved_by = 'PLD').update(approved_on = approved_on,status = 2,remarks = reason)
            Event_registration.objects.filter(pk = Event_id).update(Event_status = 2,waiting_list = 0)
            for i in obj1:
                Event_registration.objects.filter(Event_id = i.Event_id).update(waiting_list = 0)
            return redirect('home')
        

    return render(request,'home')


def cancel(request,Event_id):
    if  request.method == 'POST':
        reason = request.POST['reason']
        approved_on = datetime.datetime.now()
        track.objects.filter(event_id = Event_id , approved_by = 'PLD').update(approved_on = approved_on,status = 2,remarks = reason)

        Event_registration.objects.filter(pk = Event_id).update(Event_status = 2,waiting_list = 2)
            
    


    return render(request,'pld/view_event.html')





def track_event(request):
    users = User.objects.all()
    if request.session.get('head_id'):
        headid=request.session['head_id']
        head_user = request.session['head_username']
        if Department.objects.filter(head_ids_id = headid):
            head_dep = Department.objects.get(head_ids_id = headid)
            events = Event_registration.objects.filter(Event_manager = head_dep.department_name)
            track_ev = track.objects.all()
            return render(request,'dpartment/eventtrack.html',{'headid':headid,'user':head_user,'track':track_ev,'event':events})
        else:
            return render(request,'dpartment/eventtrack.html',{'headid':headid,'user':head_user})
    elif request.session.get('id'):
        depid=request.session['id']
        depuser = request.session['department_username']
        if Department.objects.filter(pk=depid):
            dep = Department.objects.get(pk=depid)
            events = Event_registration.objects.filter(Event_manager = dep.department_name)
            track_ev = track.objects.all()
            return render(request,'dpartment/eventtrack.html',{'depid':depid,'user':depuser,'track':track_ev,'event':events})
        else:
            return render(request,'dpartment/eventtrack.html',{'depid':depid,'user':depuser})
    elif request.session.get('publicid'):
        publicid=request.session['publicid']
        publicname=request.session['publicname']
        if public_registration.objects.filter(pk=publicid):
            events = Event_registration.objects.filter(Event_manager = publicname)
            track_ev = track.objects.all()
            return render(request,'dpartment/eventtrack.html',{'publicid':publicid,'user':publicname,'track':track_ev,'event':events})
        else:
            return render(request,'dpartment/eventtrack.html',{'publicid':publicid,'user':publicname})
    elif request.session.get('unionid'):
        unionid=request.session['unionid']
        unionname=request.session['unionname']
        if unions.objects.filter(pk=unionid):
            events = Event_registration.objects.filter(Event_manager = unionname)
            track_ev = track.objects.all()
            return render(request,'dpartment/eventtrack.html',{'unionid':unionid,'user':unionname,'track':track_ev,'event':events})
        else:
            return render(request,'dpartment/eventtrack.html',{'unionid':unionid,'user':unionname})
    elif users.exists:
            events = Event_registration.objects.all()
            track_ev = track.objects.all()
            return render(request,'dpartment/eventtrack.html',{'track':track_ev,'event':events})
    
    return render(request,'dpartment/eventtrack.html')


# def add_venue(request):
#     if request.method == "POST":
#          form=Hall_detailsForm(request.POST)
#          if form.is_valid():
#              form.save()
#              return redirect('view_venue')
#     form=Hall_detailsForm
#     return render(request,'pld/Addvenue.html',{'form':form})

def add_venue(request):
   
    form = VenueForm(request.POST or None , request.FILES)
    if request.method == "POST":
        if request.session.get('head_id'):
            head=request.session['head_id']
            dep_name=DepartmentHead.objects.get(pk=head)
            department=request.session['head_username']
            if form.is_valid():
                #form.save()
                event =form.save(commit=False)
                event.Hall_manager = dep_name.department_name # logged in user
                event.save()
                return redirect('Department')
            return render(request,'pld/Addvenue.html',{'form':form,'headid':head,'user':department})

        elif request.user.is_authenticated:
            if form.is_valid():
                #form.save()
                event =form.save(commit=False)
                event.Hall_manager = request.user.username # logged in user
                event.save()
                return redirect('home')
            return render(request,'pld/Addvenue.html',{'form':form})
    if request.session.get('head_id'):
        head=request.session['head_id']
        dep_name=DepartmentHead.objects.get(pk=head)
        department=request.session['head_username']
        return render(request,'pld/Addvenue.html',{'form':form,'headid':head,'user':department})

    return render(request,'pld/Addvenue.html',{'form':form})


















def singlevenue(request,venue_id):
    venue=Hall_details.objects.get(pk=venue_id)
    events=venue.event_registration_set.all()
    today = datetime.datetime.now().date()
    print(venue.Due_date)
    print(today)
    if venue.Due_date == today:
        Hall_details.object.filter(pk=venue_id).update(Amount = venue.NewAmount,NewAmount = "",Due_date="")
    
    if request.session.get('id'):
        id=request.session['id']
        username=request.session['department_username']
        return render(request,'pld/viewsinglevenue.html',{'venue':venue,'depid':id,'user':username,'events':events,'today':today})
    elif request.session.get('head_id'):
        id=request.session['head_id']
        username=request.session['head_username']
        return render(request,'pld/viewsinglevenue.html',{'venue':venue,'headid':id,'user':username,'events':events,'today':today})
    elif request.session.get('unionid'):
        id=request.session['unionid']
        username=request.session['unionname']
        return render(request,'pld/viewsinglevenue.html',{'venue':venue,'unionid':id,'user':username,'events':events,'today':today})
    elif request.session.get('publicid'):
        id=request.session['publicid']
        username=request.session['publicname']
        return render(request,'pld/viewsinglevenue.html',{'venue':venue,'publicid':id,'user':username,'events':events,'today':today})
    elif request.session.get('mainuserid'):
        id=request.session['mainuserid']
        username=request.session['mainusername']
        return render(request,'pld/viewsinglevenue.html',{'venue':venue,'mainuserid':id,'user':username,'events':events,'today':today})

    else:
        return render(request,'pld/viewsinglevenue.html',{'venue':venue,'events':events,'today':today})









    


def update_venue(request,venue_id):
    venue=Hall_details.objects.get(pk=venue_id)
    print(venue)
    if request.user.is_superuser:
        form =VenueForm(request.POST or None , request.FILES or None , instance=venue)


        if form.is_valid():
            duedate = request.POST['duedate']
            newamount = request.POST['newamount']
            if duedate == '' :
                form.save()
            else:
                venue =form.save(commit=False)
                venue.Due_date = duedate
                venue.NewAmount = newamount
                form.save()

            return redirect('home')
    elif request.session.get('head_id'):
        form =VenueForm(request.POST or None ,  instance=venue)

        head=request.session['head_id']
        department=request.session['head_username']
        if form.is_valid():
            duedate = request.POST['duedate']
            newamount = request.POST['newamount']
            if duedate == '' :
                form.save()
            else:
                venue =form.save(commit=False)
                venue.Due_date = duedate
                venue.NewAmount = newamount
                form.save()
            return redirect('Department')
        return render(request,'pld/updatevenue.html',{'venue':venue,'form':form,'headid':head,'user':department})

    
    return render(request,'pld/updatevenue.html',{'venue':venue,'form':form})




def my_venues(request):
    if request.user.is_authenticated:
        me = request.user
        venue = Hall_details.objects.filter(Hall_manager = me)
        return render(request, 'pld/my_venues.html', {"venue":venue})
    elif request.session.get("head_id"):
        dep_head_venue=request.session['head_id']
        dep_head_user=request.session['head_username']
        me = DepartmentHead.objects.get(pk=dep_head_venue)
        venue = Hall_details.objects.filter(Hall_manager = me.department_name)
        return render(request,'pld/my_venues.html', {"venue":venue,'user':dep_head_user,'headid':dep_head_venue})
  
    





def delete_venue(requset,venue_id):
    event=Hall_details.objects.get(pk=venue_id)
    event.delete()
    return redirect('view_venue')




#create and view events


def all_event(request):
    events=Event_registration.objects.filter(Event_status = 1).order_by('Event_startDate')
    today = datetime.datetime.now().date()
    if request.session.get('head_id'):
        id=request.session['head_id']
        username=request.session['head_username']
    
        return render(request,'pld/view_all_events.html',{'events':events,'headid':id,'user':username,'today':today})
    elif request.session.get('id'):
        id=request.session['id']
        username=request.session['department_username']
        return render(request,'pld/view_all_events.html',{'events':events,'depid':id,'user':username,'today':today})
    elif request.session.get('mainuserid'):
        id=request.session['mainuserid']
        username=request.session['mainusername']
        obj=Main_accounts.objects.get(pk=id)
        if obj.varification_choices == 'Varification':
            return render(request,'pld/view_all_events.html',{'events':events,'mainuserid':id,'user':username,'today':today})
        else:
            return render(request,'pld/view_all_events.html',{'events':events,'proid':id,'user':username,'today':today})
    elif request.session.get('unionid'):
        id=request.session['unionid']
        user=request.session['unionname']
        return render(request,'pld/view_all_events.html',{'events':events,'user':user,'unionid':id,'today':today})
    elif request.session.get('publicid'):
        id=request.session['publicid']
        user=request.session['publicname']
        return render(request,'pld/view_all_events.html',{'events':events,'user':user,'publicid':id,'today':today})
    return render(request,'pld/view_all_events.html',{'events':events,'today':today})



def create_event(request):
    dep_id=request.session.get('id')
    union_ids=request.session.get('unionid')
    public_ids=request.session.get('publicid')
    currentdatetime = datetime.datetime.now()
    public_venues=Hall_details.objects.filter(public_view = True)
    avail_venues=Hall_details.objects.filter(Hall_availability = True)
    category=EventCategory.objects.all()

    

    if request.method == "POST":
        if request.user.is_superuser:
            form = EventForm(request.POST)
            category = request.POST['category']

            if form.is_valid():
                event =form.save(commit=False)
                event.Event_manager = 'admin'
                event_name = form['Event_name'].value()
                event_start_date=form['Event_startDate'].value()
                event_end_date=form['Event_endDate'].value()
                event_venue = form['Event_venue'].value()
                venue_amt = Hall_details.objects.get(Hall_id = event_venue)
                event.Category_name = category
             
                if category == '1':
                    event.Event_amount=venue_amt.Amount
                print(event_end_date)
                print(event_name)

                print(event_start_date) 

                    

                form.save()
                ev = Event_registration.objects.get(Event_manager = 'admin',Event_name = event_name,Event_startDate = event_start_date,Event_endDate = event_end_date)
                if venue_amt.Hall_manager == 'admin':                
                    track(event_id = ev.Event_id, approved_by = 'PLD').save()
                else:
                    track(event_id = ev.Event_id, approved_by = venue_amt.Hall_manager).save()
                operation = "CREATE EVENT"
                person = "admin"
                person_category = "admin"
                Event_id = ev.Event_id
                
                event_log(operation,person,person_category,Event_id)

                ev_start = Event_registration.objects.filter(Event_venue = event_venue,Event_startDate__range=[event_start_date,event_end_date],waiting_list = 1,Event_status = 0).exclude(Event_id = ev.Event_id)
                ev_end = Event_registration.objects.filter(Event_venue = event_venue,Event_endDate__range=[event_start_date,event_end_date],waiting_list = 1,Event_status = 0).exclude(Event_id = ev.Event_id)
                ev_outstart = Event_registration.objects.filter(Event_venue = event_venue,Event_startDate__lte = event_start_date,waiting_list = 1,Event_endDate__gte = event_end_date,Event_status = 0).exclude(Event_id = ev.Event_id)
        
                obj = list(chain(ev_start,ev_end,ev_outstart))
                obj1=[*set(obj)]
             
                if obj1:
                    Event_registration.objects.filter(Event_id = ev.Event_id).update(waiting_list = 2)

              

                            
                return redirect('home')



        elif request.session.get('id'):
            category = request.POST['category']

            dep_id=request.session.get('id')
            form = EventForm(request.POST)
         
            if form.is_valid():
                obj=Department.objects.get(pk=dep_id)
                event =form.save(commit=False)
                event.Event_manager = obj.department_name
                event.current_datetime = currentdatetime
                event_name = form['Event_name'].value()
                event_start_date=form['Event_startDate'].value()
                event_end_date=form['Event_endDate'].value()
                event_venue = form['Event_venue'].value()
                venue_amt = Hall_details.objects.get(Hall_id = event_venue)
                event.Category_name = category
             
                if category == '1':
                    event.Event_amount=venue_amt.Amount

              
                form.save()
                ev = Event_registration.objects.get(Event_manager = obj.department_name,Event_name = event_name,Event_startDate = event_start_date,Event_endDate = event_end_date)
                head = Department.objects.get(department_name = obj.department_name)
                track(event_id = ev.Event_id, approved_by = head.department_name).save()

                operation = "CREATE EVENT"
                person = obj.department_name
                person_category = "DEPARTMENT"
                Event_id = ev.Event_id
                event_log(operation,person,person_category,Event_id)




                ev_start = Event_registration.objects.filter(Event_venue = event_venue,Event_startDate__range=[event_start_date,event_end_date],waiting_list = 1,Event_status = 0).exclude(Event_id = ev.Event_id)
                ev_end = Event_registration.objects.filter(Event_venue = event_venue,Event_endDate__range=[event_start_date,event_end_date],waiting_list = 1,Event_status = 0).exclude(Event_id = ev.Event_id)
                ev_outstart = Event_registration.objects.filter(Event_venue = event_venue,Event_startDate__lte = event_start_date,waiting_list = 1,Event_endDate__gte = event_end_date,Event_status = 0).exclude(Event_id = ev.Event_id)
        
                obj = list(chain(ev_start,ev_end,ev_outstart))
                obj1=[*set(obj)]
                if obj1:
                    Event_registration.objects.filter(Event_id = ev.Event_id).update(waiting_list = 2)
                            






                return redirect('Department')



        elif request.session.get('unionid'):
            category = request.POST['category']
 
            form = EventForm(request.POST)
            if form.is_valid():
                obj=unions.objects.get(pk=union_ids)
                event =form.save(commit=False)
                event_name = form['Event_name'].value()
                event_start_date=form['Event_startDate'].value()
                event_end_date=form['Event_endDate'].value()
                event_venue = form['Event_venue'].value()
                event.Event_manager = obj.union_name
                event.current_datetime = currentdatetime
                event_venue = form['Event_venue'].value()
                venue_amt = Hall_details.objects.get(Hall_id = event_venue)
                event.Category_name = category
             
                if category == '1':
                    event.Event_amount=venue_amt.Amount
                form.save()
                ev = Event_registration.objects.get(Event_manager = obj.union_name,Event_name = event_name,Event_startDate = event_start_date,Event_endDate = event_end_date)
                hall=Hall_details.objects.get(Hall_id = event_venue)
                if hall.Hall_manager == 'admin':
                    track(event_id = ev.Event_id, approved_by = 'PLD').save()
                else:
                    track(event_id = ev.Event_id, approved_by = hall.Hall_manager).save()

                operation = "CREATE EVENT"
                person = obj.union_name
                person_category = "UNION"
                Event_id = ev.Event_id
                event_log(operation,person,person_category,Event_id)

                ev_start = Event_registration.objects.filter(Event_venue = event_venue,Event_startDate__range=[event_start_date,event_end_date],waiting_list = 1).exclude(Event_id = ev.Event_id)
                ev_end = Event_registration.objects.filter(Event_venue = event_venue,Event_endDate__range=[event_start_date,event_end_date],waiting_list = 1).exclude(Event_id = ev.Event_id)
                ev_outstart = Event_registration.objects.filter(Event_venue = event_venue,Event_startDate__lte = event_start_date,waiting_list = 1,Event_endDate__gte = event_end_date).exclude(Event_id = ev.Event_id)
        
                obj = list(chain(ev_start,ev_end,ev_outstart))
                obj1=[*set(obj)]
             
                if obj1:
                    Event_registration.objects.filter(Event_id = ev.Event_id).update(waiting_list = 2)
                            
                return redirect('Department')


        elif request.session.get('publicid'):
            form = PublicEventForm(request.POST)
            
            
            if form.is_valid():
                instrument = request.POST['instrument']
                obj=public_registration.objects.get(pk=public_ids)
                event =form.save(commit=False)
                event_name = form['Event_name'].value()
                event_start_date=form['Event_startDate'].value()
                event_end_date=form['Event_endDate'].value()
                event_venue = form['Event_venue'].value()
                event.Event_manager = obj.public_name
                event.current_datetime = currentdatetime
                event.public = True
                event_venue = form['Event_venue'].value()
                event.Instrument_details = instrument
                venue_amt = Hall_details.objects.get(Hall_id = event_venue)
              
                form.save()
                ev = Event_registration.objects.get(Event_manager = obj.public_name,Event_name = event_name,Event_startDate = event_start_date,Event_endDate = event_end_date) 
                hall=Hall_details.objects.get(Hall_id = event_venue)
                if hall.Hall_manager == 'admin':
                    track(event_id = ev.Event_id, approved_by = 'PLD').save()
                else:
                    track(event_id = ev.Event_id, approved_by = hall.Hall_manager).save()

                operation = "CREATE EVENT"
                person = obj.public_name
                person_category = "PUBLIC"
                Event_id = ev.Event_id
                event_log(operation,person,person_category,Event_id)

                ev_start = Event_registration.objects.filter(Event_venue = event_venue,Event_startDate__range=[event_start_date,event_end_date],waiting_list = 1,Event_status = 0).exclude(Event_id = ev.Event_id)
                ev_end = Event_registration.objects.filter(Event_venue = event_venue,Event_endDate__range=[event_start_date,event_end_date],waiting_list = 1,Event_status = 0).exclude(Event_id = ev.Event_id)
                ev_outstart = Event_registration.objects.filter(Event_venue = event_venue,Event_startDate__lte = event_start_date,waiting_list = 1,Event_endDate__gte = event_end_date,Event_status = 0).exclude(Event_id = ev.Event_id)
        
                obj = list(chain(ev_start,ev_end,ev_outstart))
                obj1=[*set(obj)]
                if obj1:
                    Event_registration.objects.filter(Event_id = ev.Event_id).update(waiting_list = 2)
                            
                return redirect('public_home')

        else:
            form = EventForm(request.POST)
            if form.is_valid():
                #form.save()
                event =form.save(commit=False)
                event.Event_manager = request.user # logged in user

                form.save()
                return redirect('home')
    else:
        # Just Going To The Page, Not Submitting 
        if request.user.is_superuser:
            form = EventForm
        elif request.session.get('id'):
            form = EventForm
        elif request.session.get('unionid'):
            form = EventForm
        elif request.session.get('publicid'):
            form = PublicEventForm
        else:
            form = EventForm
    if request.user.is_superuser:
        allevent=Event_registration.objects.filter(Event_status = 1)
        allvenuse=Hall_details.objects.all()
        category= EventCategory.objects.all()
        return render(request,'pld/add_event.html',{'form':form,'all':allevent,'all_venues':allvenuse,'cat':category,'avail_venues':avail_venues,'category':category})
    if request.session.get('id'):
        obj=Department.objects.get(pk=dep_id)
        allevent=Event_registration.objects.filter(Event_status = 1)
        allvenuse=Hall_details.objects.all()
        category= EventCategory.objects.all()

        return render(request,'pld/add_event.html',{'form':form,'depid':dep_id,'all':allevent,'user':obj.department_name,'all_venues':allvenuse,'cat':category,'avail_venues':avail_venues,'category':category})
    elif request.session.get('unionid'):
        allevent=Event_registration.objects.filter(Event_status = 1)
        obj=unions.objects.get(pk=union_ids)
        allvenuse=Hall_details.objects.all()
        category= EventCategory.objects.all()

        return render(request,'pld/add_event.html',{'form':form,'unionid':union_ids,'user':obj.union_name,'all_venues':allvenuse,'all':allevent,"public_venues":public_venues,'cat':category,'avail_venues':avail_venues,'category':category})
    elif request.session.get('publicid'):
        allevent=Event_registration.objects.filter(Event_status = 1)
        obj=public_registration.objects.get(pk=public_ids)
        allvenuse=Hall_details.objects.all()
        instrument = instrument_details.objects.all()

        return render(request,'pld/add_event.html',{'form':form,'publicid':public_ids,'user':obj.public_name,'all':allevent,"public_venues":public_venues,'all_venues':allvenuse,'cat':category,'instr':instrument,'avail_venues':avail_venues})

    else:
        allevent=Event_registration.objects.filter(Event_status = 1)
        category= EventCategory.objects.all()
        allvenuse=Hall_details.objects.all()
        return render(request,'pld/add_event.html',{'form':form,'all_venues':allvenuse,'all':allevent,'cat':category,'avail_venues':avail_venues,'category':category})






def singlevent(request,Event_id):
    event=Event_registration.objects.get(pk=Event_id)
    vari_users=Main_accounts.objects.filter(varification_choices = 'Varification')

    if request.session.get('id'):
        id=request.session['id']
        username=request.session['department_username']
        ev= Event_registration.objects.get(Event_id = Event_id)
        ev_start = Event_registration.objects.filter(Event_venue = ev.Event_venue,Event_startDate__range=[ev.Event_startDate,ev.Event_endDate],Event_status__in = [0,3]).exclude(Event_id = Event_id)
        ev_end = Event_registration.objects.filter(Event_venue = ev.Event_venue,Event_endDate__range=[ev.Event_startDate,ev.Event_endDate],Event_status__in = [0,3]).exclude(Event_id = Event_id)
        ev_outstart = Event_registration.objects.filter(Event_venue = ev.Event_venue,Event_startDate__lte = ev.Event_startDate,Event_endDate__gte = ev.Event_endDate,Event_status__in = [0,3]).exclude(Event_id = ev.Event_id)
        
        obj = list(chain(ev_start,ev_end,ev_outstart))
        obj1=[*set(obj)]
        return render(request,'pld/view_event.html',{'event':event,'depid':id,'user':username,'obj':obj1})
        
    elif request.session.get('head_id'):
        id=request.session['head_id']
        username=request.session['head_username']
        ev= Event_registration.objects.get(Event_id = Event_id)
        deps = Department.objects.get(head_ids = id)
        ev_start = Event_registration.objects.filter(Event_venue = ev.Event_venue,Event_startDate__range=[ev.Event_startDate,ev.Event_endDate],Event_status__in = [0,3]).exclude(Event_id = Event_id)
        ev_end = Event_registration.objects.filter(Event_venue = ev.Event_venue,Event_endDate__range=[ev.Event_startDate,ev.Event_endDate],Event_status__in = [0,3]).exclude(Event_id = Event_id)
        ev_outstart = Event_registration.objects.filter(Event_venue = ev.Event_venue,Event_startDate__lte = ev.Event_startDate,Event_endDate__gte = ev.Event_endDate,Event_status__in = [0,3]).exclude(Event_id = ev.Event_id)
        
        obj = list(chain(ev_start,ev_end,ev_outstart))
        obj1=[*set(obj)]
        print(obj1)
        ev = track.objects.filter(approved_by = deps.department_name, status = 0)

        depart = DepartmentHead.objects.filter(head_id = id)
        hall = Hall_details.objects.all()
        return render(request,'pld/view_event.html',{'event':event,'headid':id,'user':username,'obj':obj1,'eve':ev,'dep':depart,'hall':hall})
    elif request.session.get('unionid'):
        id=request.session['unionid']
        username=request.session['unionname']
        return render(request,'pld/view_event.html',{'event':event,'unionid':id,'user':username})
    elif request.session.get('publicid'):
        id=request.session['publicid']
        username=request.session['publicname']
        return render(request,'pld/view_event.html',{'event':event,'publicid':id,'user':username})
    elif request.session.get('mainuserid'):
        id=request.session['mainuserid']
        username=request.session['mainusername']
        
        varifiedaccounts = Main_accounts.objects.filter(varification_choices = 'Varification')
        nonvarifiedaccounts = Main_accounts.objects.filter(varification_choices = 'Non Varification')
        return render(request,'pld/view_event.html',{'event':event,'mainuserid':id,'user':username,'variusers':vari_users,'varifiedaccounts':varifiedaccounts,'nonvarifiedaccounts':nonvarifiedaccounts})
    elif request.user.is_superuser:
        ev= Event_registration.objects.get(Event_id = Event_id)
        print(ev.Event_venue)
        ev_start = Event_registration.objects.filter(Event_venue = ev.Event_venue,Event_startDate__range=[ev.Event_startDate,ev.Event_endDate],Event_status__in = [0,3] ).exclude(Event_id = Event_id)
        ev_end = Event_registration.objects.filter(Event_venue = ev.Event_venue,Event_endDate__range=[ev.Event_startDate,ev.Event_endDate],Event_status__in = [0,3]).exclude(Event_id = Event_id)
        ev_outstart = Event_registration.objects.filter(Event_venue = ev.Event_venue,Event_startDate__lte = ev.Event_startDate,Event_endDate__gte = ev.Event_endDate,Event_status__in = [0,3]).exclude(Event_id = ev.Event_id)
        
        obj = list(chain(ev_start,ev_end,ev_outstart))
        obj1=[*set(obj)]
        print(obj1)
        ev = track.objects.filter(approved_by = 'PLD', status = 0)

        return render(request,'pld/view_event.html',{'event':event,'obj':obj1,'variusers':vari_users,'eve':ev})



    else:
        return render(request,'pld/view_event.html',{'event':event})







def view_single_user(request):

    if request.session.get('head_id'):
        headid=request.session['head_id']
        headusername=request.session['head_username']
        user = DepartmentHead.objects.get(pk=headid)
        return render(request,'user/viewsingleuser.html',{'headid':headid,'user':headusername,'users':user})
    elif request.session.get('id'):
        depid=request.session['id']
        depusername=request.session['department_username']
        user = Department.objects.get(pk=depid)
        print(user)
        return render(request,'user/viewsingleuser.html',{'depid':depid,'user':depusername,'users':user})
    elif request.session.get('mainuserid'):
        proid=request.session['mainuserid']
        prousername=request.session['mainusername']
        user= Main_accounts.objects.get(pk=proid)
        print(user)
        return render(request,'user/viewsingleuser.html',{'mainuserid':proid,'user':prousername,'users':user})
    elif request.session.get('unionid'):
        union_ids=request.session['unionid']
        unionname=request.session['unionname']
        user= unions.objects.get(pk=union_ids)
        print(user)
        return render(request,'user/viewsingleuser.html',{'unionid':union_ids,'user':unionname,'users':user})
    elif request.session.get('publicid'):
        public_ids=request.session['publicid']
        publicname=request.session['publicname']
        user = public_registration.objects.get(pk=public_ids)
        
        return render(request,'user/viewsingleuser.html',{'publicid':public_ids,'user':publicname,'users':user})
    
    elif request.user.is_superuser:
        us=request.user
        return render(request,'user/viewsingleuser.html',{'users':us})
    return render(request,'user/viewsingleuser.html')





def edit_event(request,Event_id):
    event=Event_registration.objects.get(pk=Event_id)  
    allevent=Event_registration.objects.filter(Event_status = 1)
    allvenuse=Hall_details.objects.all()
    category= EventCategory.objects.all()
    public_venues=Hall_details.objects.filter(public_view = True)

    if request.user.is_superuser:
        form =EventForm(request.POST or None, instance=event)
        if form.is_valid():
            wait = form.save(commit=False)
            event_name = form['Event_name'].value()
            event_start_date=form['Event_startDate'].value()
            event_end_date=form['Event_endDate'].value()
            track.objects.filter(event_id = Event_id ).delete()
            form.save()
            Event_registration.objects.filter(pk = Event_id).update(Event_status = 0)  
            ev = Event_registration.objects.get(Event_manager = 'admin',Event_name = event_name,Event_startDate = event_start_date,Event_endDate = event_end_date)
            track(event_id = ev.Event_id, approved_by = 'PLD').save()      
            return redirect('home')
        return render(request,'pld/edit_event.html',{'event':event,'form':form,'all':allevent,'all_venues':allvenuse,'cat':category})




    elif request.session.get('unionid'):
        union_ids=request.session.get('unionid')
        union_user=request.session['unionname']
        form=EventForm(request.POST or None, instance=event)
        if form.is_valid():
            obj=unions.objects.get(pk=union_ids)
            wait =form.save(commit=False)
            event_name = form['Event_name'].value()
            event_start_date=form['Event_startDate'].value()
            event_end_date=form['Event_endDate'].value()
            event_venue = form['Event_venue'].value()
            track.objects.filter(event_id = Event_id ).delete()
            form.save()
            Event_registration.objects.filter(pk = Event_id).update(Event_status = 0,Resubmission = 0)  
            ev = Event_registration.objects.get(Event_manager = obj.union_name,Event_name = event_name,Event_startDate = event_start_date,Event_endDate = event_end_date)
            hall=Hall_details.objects.get(Hall_id = event_venue)
            if hall.Hall_manager == 'admin':
                track(event_id = ev.Event_id, approved_by = 'PLD').save()
            else:
                track(event_id = ev.Event_id, approved_by = hall.Hall_manager).save()
            return redirect('Department')
        return render(request,'pld/edit_event.html',{'event':event,'form':form,'unionid':union_ids,'user':union_user,'all':allevent,'all_venues':allvenuse,'cat':category})





    elif request.session.get('id'):
        dep_id=request.session.get('id')
        dep_user=request.session['department_username']
        form=EventForm(request.POST or None, instance=event)
        
        if form.is_valid():
            obj=Department.objects.get(pk=dep_id)
            event =form.save(commit=False)
            event.Event_manager = obj.department_name
            event_name = form['Event_name'].value()
            event_start_date=form['Event_startDate'].value()
            event_end_date=form['Event_endDate'].value()
            track.objects.filter(event_id = Event_id ).delete()
            form.save()
            Event_registration.objects.filter(pk = Event_id).update(Event_status = 0,Resubmission = 0) 
            ev = Event_registration.objects.get(Event_manager = obj.department_name,Event_name = event_name,Event_startDate = event_start_date,Event_endDate = event_end_date)
            head = DepartmentHead.objects.get(department_name = obj.department_name)
            track(event_id = ev.Event_id, approved_by = head.department_name).save()
            return redirect('Department')

        return render(request,'pld/edit_event.html',{'event':event,'form':form,'depid':dep_id,'user':dep_user,'all':allevent,'all_venues':allvenuse,'cat':category})
    





    elif request.session.get('publicid'):
        public_ids=request.session.get('publicid')
        public_user=request.session['publicname']
        obj=public_registration.objects.get(pk=public_ids)

        form=EventForm(request.POST or None, instance=event)
        if form.is_valid():

            event =form.save(commit=False)
            obj=public_registration.objects.get(pk=public_ids)

            event.Event_manager = obj.public_name
            event_name = form['Event_name'].value()
            event_start_date=form['Event_startDate'].value()
            event_end_date=form['Event_endDate'].value()
            event_venue = form['Event_venue'].value()

            track.objects.filter(event_id = Event_id ).delete()
            form.save()
            Event_registration.objects.filter(pk = Event_id).update(Event_status = 0,Resubmission = 0)  
            ev = Event_registration.objects.get(Event_manager = obj.public_name,Event_name = event_name,Event_startDate = event_start_date,Event_endDate = event_end_date)
            hall=Hall_details.objects.get(Hall_id = event_venue)
          
            
            if hall.Hall_manager == 'admin':
                track(event_id = ev.Event_id, approved_by = 'PLD').save()
            else:
                track(event_id = ev.Event_id, approved_by = hall.Hall_manager).save()
            return redirect('public_home')
        return render(request,'pld/edit_event.html',{'event':event,'form':form,'publicid':public_ids,'user':public_user,'all':allevent,"public_venues":public_venues,'all_venues':allvenuse,'cat':category})

    else:
        form =EventForm(request.POST or None, instance=event)
        if form.is_valid():
            form.save()
            return redirect('Department')

   
    return render(request,'pld/edit_event.html',{'event':event,'form':form})










def delete_event(requset,Event_id):
    event=Event_registration.objects.get(pk=Event_id)
    event.delete()
    if request.user.is_superuser:
        return redirect('home')
    else:
        return redirect('Department')






#show you own events and venues

def my_events(request):
    tracks = track.objects.filter(status = 2) 
    trackevents = track.objects.all()
    dep_users = DepartmentHead.objects.all()
    if request.user.is_authenticated:
        me = request.user
	# 	events = Event_registration.objects.filter(Event_manager = me)
        events=Event_registration.objects.filter(Event_manager = me)
        return render(request, 'pld/my_events.html', {"events":events,'tracks':tracks,'trackevents':trackevents,'dep_users':dep_users})
    elif request.session.get("id"):
        dep_event=request.session['id']
        dep_user=request.session['department_username']
        me = Department.objects.get(pk=dep_event)
        events=Event_registration.objects.filter(Event_manager = me.department_name).order_by('Event_startDate')
        return render(request, 'pld/my_events.html', {"events":events,"depid":dep_event,"user":dep_user,'tracks':tracks,'trackevents':trackevents,'dep_users':dep_users})
    elif request.session.get("head_id"):
        dep_event=request.session['head_id']
        dep_user=request.session['head_username']
        me = DepartmentHead.objects.get(pk=dep_event)
        events=Event_registration.objects.filter(Event_manager = me.department_name + " head").order_by('Event_startDate')
        head_name = me.department_name + " head"
        return render(request, 'pld/my_events.html', {"events":events,"headid":dep_event,"user":dep_user,'tracks':tracks,'trackevents':trackevents,'dep_users':dep_users,'head_name':head_name})
    
    
    
    elif request.session.get('unionid'):
        id=request.session['unionid']
        user=request.session['unionname']
        me = unions.objects.get(pk=id)
        events=Event_registration.objects.filter(Event_manager = me.union_name)

        return render(request,'pld/my_events.html',{'events':events,'user':user,'unionid':id,'tracks':tracks,'trackevents':trackevents,'dep_users':dep_users})
    elif request.session.get('publicid'):
        id=request.session['publicid']
        user=request.session['publicname']
        me = public_registration.objects.get(pk=id)
        events=Event_registration.objects.filter(Event_manager = me.public_name)
        return render(request,'pld/my_events.html',{'events':events,'user':user,'publicid':id,'tracks':tracks,'trackevents':trackevents,'dep_users':dep_users})
    


    else:
        events=Event_registration.objects.all()
        return render(request, 'pld/my_events.html', {"events":events})
	# if request.user.is_authenticated:
	# 	me = request.user
	# 	events = Event_registration.objects.filter(Event_manager = me)
	# 	return render(request, 'pld/my_events.html', {"events":events})
        

	# else:
	# 	return redirect('home')


def reqresubmission(request,Event_id):
    approved_accnts = track.objects.get(event_id = Event_id,status = 0)
    eves = Event_registration.objects.get(Event_id = Event_id)
    if request.session.get('id'):
        Event_registration.objects.filter(Event_id = Event_id).update(Resubmission = 1)
        return redirect('Department')
    elif request.session.get('mainuserid'):
        Event_registration.objects.filter(Event_id = Event_id).update(Resubmission = 2)
        track.objects.filter(event_id = Event_id).delete()
        if Department.objects.filter(department_name = eves.Event_manager):
            track(event_id = Event_id,approved_by = eves.Event_manager).save()
        else:
            track(event_id = Event_id,approved_by = 'PLD').save()
        return redirect('home')
    elif request.session.get('head_id'):
        
        Event_registration.objects.filter(Event_id = Event_id).update(Resubmission = 2)
        track.objects.filter(event_id = Event_id).delete()
        if Department.objects.filter(department_name = eves.Event_manager):
            track(event_id = Event_id,approved_by = eves.Event_manager).save()
        else:
            track(event_id = Event_id,approved_by = 'PLD').save()
        return redirect('Department')
    elif request.session.get('unionid'):
        
        Event_registration.objects.filter(Event_id = Event_id).update(Resubmission = 1)
        
        return redirect('Department')
    elif request.session.get('publicid'):
        
        Event_registration.objects.filter(Event_id =Event_id).update(Resubmission = 1)
        
        return redirect('public_home')
    
    if request.user.is_authenticated:
        Event_registration.objects.filter(Event_id = Event_id).update(Resubmission = 2)
        track.objects.filter(event_id = Event_id).delete()
        
        track(event_id = Event_id,approved_by = eves.Event_manager).save()
        
        return redirect('home')

    print(approved_accnts)

    return render(request,'home')





# viewuser or mydepartments


def view_users(request):
    users=User.objects.all()
    department_heads = DepartmentHead.objects.filter(status=1)
    mainusers =Main_accounts.objects.all()
    union=unions.objects.filter(status=1)
    category = EventCategory.objects.all()
    if request.session.get('head_id'):
        depid = request.session['head_id']
        depuser = request.session['head_username']
        Departments =Department.objects.filter(head_ids = depid)
        return render(request,'pld/viewusers.html',{'headid':depid,'user':depuser,'departmentusers':Departments})

    
    else:
        form =CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('view_users')
        return render(request,'pld/viewusers.html',{'users':users,'depheads':department_heads,'mainusers':mainusers,'union':union,"ctg":category,"form":form})







# change user settings

def change_user_settings(request,user_id):
    # print(user_id)
    if request.method == 'POST':
        oldpass = request.POST['oldpass']
        newpass1 = request.POST['newpass1']
        newpass2 = request.POST['newpass2']
        if newpass1 == newpass2:

            if request.session.get('head_id'):
                head = DepartmentHead.objects.get(pk = user_id)
                if head.head_password == oldpass:
                    DepartmentHead.objects.filter(head_id = user_id).update(head_password = newpass2)  
                else:
                    messages.success(request,('Old Password not match'))
                    return redirect('view_single_user')

            elif request.session.get('id'):
         
                dep = Department.objects.get(id = user_id)
                if dep.department_password == oldpass:
                    Department.objects.filter(id = user_id).update(department_password = newpass2)
                    messages.success(request,('Password successfully changed...'))
  
                else:
                    messages.success(request,('Old Password not match'))

                    return redirect('view_single_user')            
            elif request.session.get('union_id'):
         
                union = unions.objects.get(id = user_id)
                if union.union_password == oldpass:
                    unions.objects.filter(union_id = user_id).update(union_password = newpass2)
                    messages.success(request,('password successfully changed...'))
  
                else:
                    messages.success(request,('Old Password not match'))

                    return redirect('view_single_user')            
            elif request.session.get('public_id'):
         
                public = public_registration.objects.get(id = user_id)
                if public.public_password == oldpass:
                    public_registration.objects.filter(id = user_id).update(public_password = newpass2)  
                else:
                    return redirect('view_single_user')            
            elif request.session.get('mainuserid'):
         
                main = Main_accounts.objects.get(id = user_id)
                if main.password == oldpass:
                    Main_accounts.objects.filter(id = user_id).update(password = newpass2)  
                else:
                    return redirect('view_single_user')            
                    
            elif request.user.is_superuser:
                user = User.objects.get(pk = user_id)
                if user.password == oldpass:
                    User.objects.filter(pk = user_id).update(password = newpass2)
           
        return redirect('view_single_user')
    else:
        print('hloooooooi')
        return redirect('view_single_user')




#create department user

def create_user(request,head_id):
    users=DepartmentHead.objects.get(pk=head_id)
    if request.method == "POST":
        form = DepartmentRequest(request.POST, instance=users)
        email=users.head_mail
        name=users.head_name
        password=form['head_password'].value()
        if form.is_valid():
          
            
           
            try:
                subject = f'welcome {name}, Your account is created successfully'
                message = f'Your Username is {email} and your temporary password is {password}. Please change your password after successfull login...!'
                email_from = settings.EMAIL_HOST_USER
                recipient_list = ['vysakhprakash3@gmail.com','mrkammath@gmail.com',email]
                send_mail( subject, message, email_from, recipient_list )
            except:
                return redirect('home')
            
            form.save()
            DepartmentHead.objects.filter(pk=head_id).update(status = 1)
            return redirect('home')
            

    else:
        form = DepartmentRequest()
  

    return render(request,'user/createdepartmentuser.html',{'forms':form,'department':users})

def create_union(request,union_id):
    union=unions.objects.get(pk=union_id)
    if request.method == "POST":
        form = UnionRequests(request.POST, instance=union)
        email=union.union_email
        name=union.union_name
        password=form['union_password'].value()
        if form.is_valid():
          
            
           
            try:
                subject = f'welcome {name}, Your account is created successfully'
                message = f'Your Username is {email} and your temporary password is {password}. Please change your password after successfull login...!'
                email_from = settings.EMAIL_HOST_USER
                recipient_list = ['vysakhprakash3@gmail.com','mrkammath@gmail.com',email]
                send_mail( subject, message, email_from, recipient_list )
            except:
                return redirect('home')

            
            form.save()
            unions.objects.filter(pk=union_id).update(status = 1)
            return redirect('home')
            

    else:
        form = UnionRequests()
  

    return render(request,'unions/createunionuser.html',{'forms':form,'union':union})


def search_events(request):
    if request.method == 'POST':
        key = request.POST['search']
        type = request.POST['type']
        if type == 'eventname':
            event = Event_registration.objects.filter(Event_name = key, Event_status = 1)
            return render(request,'pld/view_all_events.html',{'events':event,'type':type,'key':key})
        if type == 'department':
            event = Event_registration.objects.filter(Event_manager = key , Event_status = 1)
            return render(request,'pld/view_all_events.html',{'events':event,'type':type,'key':key})
        if type == 'month':
            event = Event_registration.objects.filter(Event_startDate__month = key, Event_status = 1)
            return render(request,'pld/view_all_events.html',{'event':event,'type':type,'key':key})
        if type == 'date':
            event = Event_registration.objects.filter(Event_startDate__day = key, Event_status = 1)
            return render(request,'pld/view_all_events.html',{'event':event,'type':type,'key':key})

    return render(request,'all_event')




def pdf_report(request):
    if request.method == 'POST':
            yearstart = request.POST['yearstart']
            yearend = request.POST['yearend']
            today = datetime.datetime.now().date()
   
            ev=Event_registration.objects.filter(Event_startDate__range=[yearstart,yearend],Event_status = 1)
            count = ev.count()
            pdf = html_to_pdf('pld/dateresult.html',{'yearstart':yearstart,'yearend':yearend,'events':ev,'count':count,'today':today})
            return HttpResponse(pdf, content_type='application/pdf')
    hall = Hall_details.objects.all()
    return render(request,'pld/pdfreport.html',{'hall':hall})


def hall_report(request): 
    if request.method == 'POST':
            halls = request.POST['hall']
            datestart = request.POST['datestart']
            dateend = request.POST['dateend']
            today = datetime.datetime.now().date()

            hall_name = Hall_details.objects.get(Hall_id = halls)
            ev=Event_registration.objects.filter(Event_startDate__range=[datestart,dateend],Event_status = 1,Event_venue = halls)
            count = ev.count()
            pdf = html_to_pdf('pld/hallresult.html',{'hall':hall_name.Hall_name,'datestart':datestart,'dateend':dateend,'events':ev,'count':count,'today':today})
            return HttpResponse(pdf, content_type='application/pdf')

    hall = Hall_details.objects.all()
    return render(request,'pld/pdfreport.html',{'hall':hall})

def pdf_report_dep(request):
    headid=request.session['head_id']
    headuser=request.session['head_username']
    head = DepartmentHead.objects.get(head_id = headid)
    dep = Department.objects.filter(head_ids = headid)
    hall = Hall_details.objects.filter(Hall_manager = head.department_name)

    if 'hallbtn' in request.POST:
        halls =  request.POST['halls']
        start = request.POST['datestart']
        end = request.POST['dateend']
        ev=Event_registration.objects.filter(Event_startDate__range=[start,end],Event_status = 1,Event_venue = halls)
        count = ev.count()
        hall_name = Hall_details.objects.get(Hall_id = halls)
        today = datetime.datetime.now().date()
        pdf = html_to_pdf('pld/hallresult.html',{'hall':hall_name.Hall_name,'datestart':start,'dateend':end,'events':ev,'count':count,'today':today})
        return HttpResponse(pdf, content_type='application/pdf')
    elif 'depbtn' in request.POST:
        dep = request.POST['dep']
        start = request.POST['datestart']
        end = request.POST['dateend']
        ev=Event_registration.objects.filter(Event_startDate__range=[start,end],Event_status = 1,Event_manager = dep)
        count = ev.count()
        today = datetime.datetime.now().date()
        pdf = html_to_pdf('pld/hallresult.html',{'hall':dep,'datestart':start,'dateend':end,'events':ev,'count':count,'today':today})
        return HttpResponse(pdf, content_type='application/pdf')




    return render(request,'pld/pdfreport.html',{'dep':dep,'hall':hall,'headid':headid,'user':headuser})

    



def GeneratePdf(request,Event_id):
    ev = Event_registration.objects.get(Event_id = Event_id)

    pdf = html_to_pdf('pld/circular.html',{'ev':ev})
        
    return HttpResponse(pdf, content_type='application/pdf')

def forgot_password(request):

    if 'otpbtn' in request.POST:
        otp = get_random_string(4, allowed_chars='0123456789')
        request.session['otp'] = otp

        email = request.POST['mail']
        print()
        if DepartmentHead.objects.filter(head_mail = email,status = 1) or Department.objects.filter(department_email = email) or unions.objects.filter(union_email = email,status = 1) or Main_accounts.objects.filter(email=email) or User.objects.filter(email=email):
            try:
                subject = f'Forgot Password'
                message = f'The otp for changing your account password is {otp}. This OTP is valid for 10 minutes'
                email_from = settings.EMAIL_HOST_USER
                recipient_list = ['vysakhprakash3@gmail.com','mrkammath@gmail.com',email]
                send_mail( subject, message, email_from, recipient_list )
                status = '1'
                return render(request,'user/forgotpassword.html',{'status':status,'email':email,'otpvarify':otp})
            except:
                return redirect('/')
        else:
            messages.success(request,('You are not a varified user'))
            return redirect('forgot_password')
    elif 'submitotpbtn' in request.POST:
        print("submitotpbtn")
        otpvarify = request.session['otp']
        otpcheck = request.POST['otp']
        email = request.POST['mail']
        status = '1'
        if otpcheck == otpvarify:

            return render(request,'user/resetpassword.html',{'email':email})
        else:
            return render(request,'user/forgotpassword.html',{'status':status,'email':email,'otpvarify':otpvarify})



                     
           
    return render(request,'user/forgotpassword.html')

def setpassword(request,email):
    if request.method == 'POST':
        pass1 = request.POST['password1']
        pass2 = request.POST['password2']
        if pass1 == pass2:
            if Department.objects.filter(department_email = email):
                    Department.objects.filter(department_email = email).update(department_password = pass2)
                    return redirect('login')
            elif DepartmentHead.objects.filter(head_mail = email):
                DepartmentHead.objects.filter(head_mail = email).update(head_password = pass2)
                return redirect('login')
            elif unions.objects.filter(union_email = email):
                unions.objects.filter(union_email = email).update(union_password = pass2)
                return redirect('login')
            elif Main_accounts.objects.filter(email=email):
                Main_accounts.objects.filter(email=email).update(password=pass2)
                return redirect('login')
            elif User.objects.filter(email=email):
                User.objects.filter(email=email).update(password=pass2)
                return redirect('login')
        else:
            return render(request,'user/resetpassword.html',{'email':email})

    return render(request,'user/resetpassword.html')





def event_log(operation,person,person_category,event_id):
    date_and_time = datetime.datetime.now()
    Event_log(operation = operation,person_name = person,person_category = person_category,Event_id = event_id,Date_and_time = date_and_time).save()
    
    HttpResponse('successfully submitted')

def log_records(request):
    log = Event_log.objects.all()
    return render(request,'pld/log_records.html',{'log':log})


def priority_event(request):
    all_venues=Hall_details.objects.filter(Hall_availability= True)
    aproved_events=Event_registration.objects.filter(Event_status=1)
   
    form =High_priority_eventForm()


    if request.session.get('head_id'):
        headid=request.session.get('head_id')
        headusername=request.session['head_username']
        my_department_name=DepartmentHead.objects.get(head_id=headid)
        venues=Hall_details.objects.filter(Hall_manager=my_department_name.department_name,Hall_availability= True)



        if request.method == "POST":
            form =High_priority_eventForm(request.POST)
            if form.is_valid():
                event =form.save(commit=False)
               
                event_venue=form['Event_venue'].value()
                startdate=form['Event_startDate'].value()
                enddate=form['Event_endDate'].value()
                event_name = form['Event_name'].value()
                category_name = form['Category_name'].value()
                event.Event_manager = my_department_name.department_name + " head"
                venue_amt = Hall_details.objects.get(Hall_id = event_venue)
                event.Event_status = '1'  
                if category_name == '1':
                    event.Event_amount=venue_amt.Amount

                event.save()
            ev = Event_registration.objects.get(Event_manager = my_department_name.department_name + " head" ,Event_name = event_name,Event_startDate = startdate,Event_endDate = enddate)
            today = datetime.datetime.now()
            track(event_id = ev.Event_id, approved_by = my_department_name.department_name + " head",approved_on = today,remarks = 'Approved',status = 1).save()

            ev_start = Event_registration.objects.filter(Event_venue = event_venue,Event_startDate__range=[startdate,enddate],Event_status = 1).exclude(Event_id = ev.Event_id)
            ev_end = Event_registration.objects.filter(Event_venue = event_venue,Event_endDate__range=[startdate,enddate],Event_status = 1).exclude(Event_id = ev.Event_id)
            ev_outstart = Event_registration.objects.filter(Event_venue = event_venue,Event_startDate__lte = startdate,Event_endDate__gte = enddate,Event_status = 1).exclude(Event_id = ev.Event_id)
    
            obj = list(chain(ev_start,ev_end,ev_outstart))
            obj1=[*set(obj)]
            
            if obj1:
                for i in obj1:
                    Event_registration.objects.filter(Event_id = i.Event_id).update(waiting_list = 2,Event_status=3,Art_and_Photography = 0,art_permission=0,Event_amount=0,Resubmission=0)
                    track.objects.filter(event_id=i.Event_id).delete()

        return render(request,'pld/priority_event.html',{'headid':headid,'user':headusername,'event':aproved_events,'venues':venues,'form':form,'all_venues':all_venues})

    elif request.user.is_superuser:
        if request.method == "POST":
            form =High_priority_eventForm(request.POST)
            if form.is_valid():

                event =form.save(commit=False)
               
                event_venue=form['Event_venue'].value()
                startdate=form['Event_startDate'].value()
                enddate=form['Event_endDate'].value()
                event_name = form['Event_name'].value()
                category_name = form['Category_name'].value()
                venue_amt = Hall_details.objects.get(Hall_id = event_venue)  
                if category_name == '1':
                    event.Event_amount=venue_amt.Amount



                event.save()
            ev = Event_registration.objects.get(Event_manager = 'admin',Event_name = event_name,Event_startDate = startdate,Event_endDate = enddate)            
            track(event_id = ev.Event_id, approved_by = 'PLD').save()
         
            ev_start = Event_registration.objects.filter(Event_venue = event_venue,Event_startDate__range=[startdate,enddate],Event_status = 1).exclude(Event_id = ev.Event_id)
            ev_end = Event_registration.objects.filter(Event_venue = event_venue,Event_endDate__range=[startdate,enddate],Event_status = 1).exclude(Event_id = ev.Event_id)
            ev_outstart = Event_registration.objects.filter(Event_venue = event_venue,Event_startDate__lte = startdate,Event_endDate__gte = enddate,Event_status = 1).exclude(Event_id = ev.Event_id)
    
            obj = list(chain(ev_start,ev_end,ev_outstart))
            obj1=[*set(obj)]
            
            if obj1:
                for i in obj1:
                    Event_registration.objects.filter(Event_id = i.Event_id).update(waiting_list = 2,Event_status=3,Art_and_Photography = 0,art_permission=0,Event_amount=0,Resubmission=0)
                    track.objects.filter(event_id=i.Event_id).delete()



        venues=Hall_details.objects.filter(Hall_manager="admin",Hall_availability= True)
        return render(request,'pld/priority_event.html',{'event':aproved_events,'venues':venues,'form':form,'all_venues':all_venues})

def Event_brochurehome(request,Event_id):
    event=Event_registration.objects.get(pk=Event_id)

    return render(request,'Brochure Home/brochure home.html',{'event':event})

def Event_brochure(request,Event_id):
   
    event=Event_registration.objects.get(pk=Event_id)
    vari_users=Main_accounts.objects.filter(varification_choices = 'Varification')

    if request.session.get('id'):
        id=request.session['id']
        username=request.session['department_username']
        ev= Event_registration.objects.get(Event_id = Event_id)
        ev_start = Event_registration.objects.filter(Event_venue = ev.Event_venue,Event_startDate__range=[ev.Event_startDate,ev.Event_endDate],Event_status__in = [0,3]).exclude(Event_id = Event_id)
        ev_end = Event_registration.objects.filter(Event_venue = ev.Event_venue,Event_endDate__range=[ev.Event_startDate,ev.Event_endDate],Event_status__in = [0,3]).exclude(Event_id = Event_id)
        ev_outstart = Event_registration.objects.filter(Event_venue = ev.Event_venue,Event_startDate__lte = ev.Event_startDate,Event_endDate__gte = ev.Event_endDate,Event_status__in = [0,3]).exclude(Event_id = ev.Event_id)
        
        obj = list(chain(ev_start,ev_end,ev_outstart))
        obj1=[*set(obj)]
        return render(request,'Brochure Home/index.html',{'event':event,'depid':id,'user':username,'obj':obj1})
        
    elif request.session.get('head_id'):
        id=request.session['head_id']
        username=request.session['head_username']
        ev= Event_registration.objects.get(Event_id = Event_id)
        deps = Department.objects.get(head_ids = id)
        ev_start = Event_registration.objects.filter(Event_venue = ev.Event_venue,Event_startDate__range=[ev.Event_startDate,ev.Event_endDate],Event_status__in = [0,3]).exclude(Event_id = Event_id)
        ev_end = Event_registration.objects.filter(Event_venue = ev.Event_venue,Event_endDate__range=[ev.Event_startDate,ev.Event_endDate],Event_status__in = [0,3]).exclude(Event_id = Event_id)
        ev_outstart = Event_registration.objects.filter(Event_venue = ev.Event_venue,Event_startDate__lte = ev.Event_startDate,Event_endDate__gte = ev.Event_endDate,Event_status__in = [0,3]).exclude(Event_id = ev.Event_id)
        
        obj = list(chain(ev_start,ev_end,ev_outstart))
        obj1=[*set(obj)]
        print(obj1)
        ev = track.objects.filter(approved_by = deps.department_name, status = 0)

        depart = DepartmentHead.objects.filter(head_id = id)
        hall = Hall_details.objects.all()
        return render(request,'Brochure Home/index.html',{'event':event,'headid':id,'user':username,'obj':obj1,'eve':ev,'dep':depart,'hall':hall})
    elif request.session.get('unionid'):
        id=request.session['unionid']
        username=request.session['unionname']
        return render(request,'Brochure Home/index.html',{'event':event,'unionid':id,'user':username})
    elif request.session.get('publicid'):
        id=request.session['publicid']
        username=request.session['publicname']
        return render(request,'Brochure Home/index.html',{'event':event,'publicid':id,'user':username})
    elif request.session.get('mainuserid'):
        id=request.session['mainuserid']
        username=request.session['mainusername']
        
        varifiedaccounts = Main_accounts.objects.filter(varification_choices = 'Varification')
        nonvarifiedaccounts = Main_accounts.objects.filter(varification_choices = 'Non Varification')
        return render(request,'Brochure Home/index.html',{'event':event,'mainuserid':id,'user':username,'variusers':vari_users,'varifiedaccounts':varifiedaccounts,'nonvarifiedaccounts':nonvarifiedaccounts})
    elif request.user.is_superuser:
        print(event.Event_images)




        return render(request,'Brochure Home/index.html',{'event':event})



    else:
        return render(request,'Brochure Home/index.html',{'event':event})

def upload(request,Event_id):
    if request.method == 'POST':
        ev=Event_registration.objects.get(Event_id = Event_id)
        ev.Evenent_images = request.FILES['images']
        ev.save()
        return redirect('all_event')