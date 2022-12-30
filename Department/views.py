import datetime
from django.shortcuts import render ,redirect
from pld.models import Event_log, Event_registration, Hall_details, track

from users.models import Department, DepartmentHead, Main_accounts




# Create your views here.


def department(request):

    if request.session.get('head_id'):
        id=request.session['head_id']
        username=request.session['head_username']
        dep = DepartmentHead.objects.get(head_id = id)
        depart = DepartmentHead.objects.filter(head_id = id)
        if track.objects.filter(approved_by = dep.department_name, status = 0 ):
            ev = track.objects.filter(approved_by = dep.department_name, status = 0)
            events = Event_registration.objects.all()
            hall = Hall_details.objects.all()
        
            return render(request,'dpartment/department.html',{'headid':id,'user':username,'event':events,'dep':depart,'hall':hall,'ev':ev})
        elif track.objects.filter(approved_by = dep.department_name, status = 0 ):
            ev = track.objects.filter(approved_by = dep.department_name, status = 0)
            events = Event_registration.objects.all()
        
            return render(request,'dpartment/department.html',{'headid':id,'user':username,'event':events,'dep':depart,'ev':ev})
        else:
            return render(request,'dpartment/department.html',{'headid':id,'user':username})
    elif request.session.get('id'):
        id=request.session['id']
        usernames=request.session['department_username']
        

        today = datetime.datetime.now()
        ev_log = Event_log.objects.all().order_by('Date_and_time')
        events = Event_registration.objects.all()
        Hall = Hall_details.objects.all()
        

        return render(request,'dpartment/department.html',{'depid':id,'user':usernames,'ev_log':ev_log,'today':today,'events':events,'hall':Hall})    
    elif request.session.get('unionid'):
        id=request.session['unionid']
        usernames=request.session['unionname']

        return render(request,'dpartment/department.html',{'unionid':id,'user':usernames})
    
    else:
        return render(request,'dpartment/department.html')

