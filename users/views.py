

import email
import hashlib 
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from pld.models import Event_log
from pld.views import event_log
from public.models import public_registration

from users.models import Department, DepartmentHead, Main_accounts
from Unions.models import unions
# from django.contrib import messages
# from django.contrib.auth.forms import UserCreationForm
from .forms import  AdduserForm ,DepartmentHeadRegistration,RegisterDepartmentForm
from django.conf import settings
from django.core.mail import send_mail


# Create your views here.
#login user and department
def login_user(request):
    
   
    if request.method == "POST":
      
        username1 = request.POST['username']
        password = request.POST['password']
      
        
    
        department=Department.objects.filter( department_email = username1, department_password=password)
        admin = authenticate(request, username=username1, password=password)
        department_head=DepartmentHead.objects.filter(head_mail = username1,head_password=password)
        main_users=Main_accounts.objects.filter(email = username1,password=password)
        union=unions.objects.filter(union_email=username1,union_password=password)


        if department_head:
            dep=DepartmentHead.objects.get(head_mail = username1,head_password=password,status = 1)            
            id=dep.head_id
            username=dep.head_name
            request.session['head_id']=id
            request.session['head_username']= username

            operation = "DEPARTMENT HEAD LOGIN"
            person = username
            person_category = "DEPARTMENT HEAD"
            Event_id = ""
            event_log(operation,person,person_category,Event_id)

            
          
            return redirect('Department')
       
        elif department:
            deps=Department.objects.get(department_email = username1, department_password=password)            
            ids=deps.id
            usernames=deps.department_name
            request.session['id']=ids
            request.session['department_username']= usernames
           
           
            operation = "DEPARTMENT LOGIN"
            person = usernames
            person_category = "DEPARTMENT "
            Event_id = ""
            event_log(operation,person,person_category,Event_id)

            
            return redirect('Department')
        elif main_users:
            main_user=Main_accounts.objects.get(email = username1,password=password)            
            id=main_user.id
            username=main_user.type
            request.session['mainuserid']=id
            request.session['mainusername']= username
            operation = "LOGIN"
            person = username
            person_category = "MAIN USER"
            Event_id = ""
            event_log(operation,person,person_category,Event_id)

                
            if main_user.varification_choices == 'Varification':
           
                return redirect('home')
            else:
                if main_user.type == 'GUEST HOUSE':
                    return redirect('guest_home')

                else:
                    return redirect('pro_home')
        elif union:
            uni=unions.objects.get(union_email=username1,union_password=password)
            id=uni.union_id
            name=uni.union_name
            request.session['unionid']=id
            request.session['unionname']=name
            operation = "UNION LOGIN"
            person = name
            person_category = "UNION"
            Event_id = ""
            event_log(operation,person,person_category,Event_id)


            
            return redirect('union_home')

        elif admin:
                if admin is not None:
                    operation = "ADMINLOGIN"
                    person = "ADMIN"
                    person_category = "ADMIN"
                    Event_id = ""
                    event_log(operation,person,person_category,Event_id)

                
                    login(request, admin)
                    return redirect('home')
        else:
            
            return redirect('login')  
    else:
        return render(request, 'user/user_login.html', {})




def logout_user(request):
    logout(request)
    return redirect('homepage')
        

# creating varification user
def add_main_users(request):
    if request.method == "POST":
        form =AdduserForm(request.POST)
        name = form['name'].value()
        type = form['type'].value()
        if form.is_valid():
            field=form.save(commit=False)
            field.name = name.capitalize()
            field.type = type.upper()
            form.save()
            return redirect('home')
    else:
        form = AdduserForm()
    return render(request,'user/register_user.html',{'forms':form})


#department request and verification


def dep_request(request):
    if request.method == "POST":
        dep_name = request.POST['depname']
        headmail = request.POST['headmail']
        headname = request.POST['headname']
        if Department.objects.filter(department_email = headmail) or DepartmentHead.objects.filter(head_mail = headmail):
            return redirect('/')
            
        else:    
            
            DepartmentHead(department_name = dep_name,head_mail = headmail,head_name = headname).save()
            
        return redirect('login')

    else:
        
        return render(request,'user/departmentrequest.html')








#add a department

def add_department(request,id):
    head=request.session['head_id']
    user=request.session['head_username']
    if request.method == "POST":
        form = RegisterDepartmentForm(request.POST)
        password=form['department_password'].value()
        name=form['department_name'].value()
        email=form['department_email'].value()
        if form.is_valid():
            dep =form.save(commit=False)
            dep.head_ids_id = DepartmentHead.objects.get(pk=id).head_id # logged in user
            # subject = f'welcome {name} department, Your account is created successfully'
            # message = f'Your Username is {username} and your temporary password is {password}. Please change your password after successfull login...!'
            # email_from = settings.EMAIL_HOST_USER
            # recipient_list = ['vysakhprakash3@gmail.com','mrkammath@gmail.com',email]
            # send_mail( subject, message, email_from, recipient_list )
            if Department.objects.filter(department_email = email) or DepartmentHead.objects.filter(head_mail = email):
                return redirect('Department')            
            else:
                dep.save()
            return redirect('Department')
        else:
            return render(request,'dpartment/adddepartment.html')

    else:
        form = RegisterDepartmentForm()
    return render(request,'dpartment/adddepartment.html',{'form':form,'headid':head,'user':user})


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def account_settings(request):
    if request.session.get('head_id'):
        headid=request.session['head_id']
        headusername=request.session['head_username']
        user = DepartmentHead.objects.get(pk=headid)
        return render(request,'header/settings.html',{'headid':headid,'user':headusername,'users':user})
    elif request.session.get('id'):
        depid=request.session['id']
        depusername=request.session['department_username']
        user = Department.objects.get(pk=depid)
        print(user)
        return render(request,'header/settings.html',{'depid':depid,'user':depusername,'users':user})
    elif request.session.get('mainuserid'):
        proid=request.session['mainuserid']
        prousername=request.session['mainusername']
        user= Main_accounts.objects.get(pk=proid)
        print(user)
        return render(request,'header/settings.html',{'mainuserid':proid,'user':prousername,'users':user})
    elif request.session.get('unionid'):
        union_ids=request.session['unionid']
        unionname=request.session['unionname']
        user= unions.objects.get(pk=union_ids)
        print(user)
        return render(request,'header/settings.html',{'unionid':union_ids,'user':unionname,'users':user})
    elif request.session.get('publicid'):
        public_ids=request.session['publicid']
        publicname=request.session['publicname']
        user = public_registration.objects.get(pk=public_ids)
        
        return render(request,'header/settings.html',{'publicid':public_ids,'user':publicname,'users':user})
    
    elif request.user.is_superuser:
        us=request.user
        log = Event_log.objects.filter(person_name = 'ADMIN').order_by('Date_and_time')
        ip = get_client_ip(request)
        print(ip)

        return render(request,'header/settings.html',{'users':us,'log':log,'ip':ip})
    
    return render(request,'header/settings.html')


