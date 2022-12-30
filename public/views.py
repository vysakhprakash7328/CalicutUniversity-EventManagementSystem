from contextlib import redirect_stderr
from django.shortcuts import render, redirect
from urllib3 import Retry

from public.models import public_registration
from django.utils.crypto import get_random_string
from django.conf import settings
from django.core.mail import send_mail
from django.contrib import messages
from pld.models import Hall_details

# Create your views here.

def public_home(request):
    id=request.session['publicid']
    name=request.session['publicname']
    venues = Hall_details.objects.filter(public_view = '1')
    print(venues)
    print(name)
    return render(request,'public/publichome.html',{'publicid':id,'user':name,'venues':venues})


def public_register(request):
    if 'register' in request.POST:
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        address = request.POST['address']
        location = request.POST['location']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        if password1 == password2:
            try:
                otp = get_random_string(4, allowed_chars='0123456789')
                request.session['otp'] = otp
                request.session['email'] = email
                

                subject = f'Welcome to Calicut University Event Management Portal'
                message = f'The otp for Creating your account is {otp}. This OTP is valid for 10 minutes'
                email_from = settings.EMAIL_HOST_USER
                recipient_list = ['vysakhprakash3@gmail.com','mrkammath@gmail.com',email]
                send_mail( subject, message, email_from, recipient_list )
                public_registration(public_name = name,public_email = email,public_phone = phone,public_address = address,public_location = location,public_password = password2,status = '0').save()

                status = '1'
                return render(request,'public/publicregister.html',{'status':status,'email':email,'otpvarify':otp})

            except:
                messages.success(request,('Sorry! We cannot proceed this request right now. Please try after some time'))
                return redirect('public_register')

            
        return redirect('public_register')
    elif 'otpvarify' in request.POST:
        email = request.session['email']
        otpvarify = request.session['otp']
       
        otp = request.POST['otp']
        if otp == otpvarify:
            public_registration.objects.filter(public_email = email).update(status = '1')
            messages.success(request,'Registration successfull...')
            return redirect('public_login')
        else:
            status = '1'
            return redirect('public_register',{'status':status,'email':email})

    
    return render(request,'public/publicregister.html')


def public_login(request):
    if 'publicloginbtn' in request.POST:
        email = request.POST['username']
        password1 = request.POST['password']
        if public_registration.objects.filter(public_email=email,public_password=password1,status = '1'):
            user=public_registration.objects.get(public_email=email,public_password=password1)
            id=user.id
            name=user.public_name
            request.session['publicid']=id
            request.session['publicname']=name

            return redirect('public_home')
        elif public_registration.objects.filter(public_email=email,public_password=password1,status = '0'):
            try:
                otp = get_random_string(4, allowed_chars='0123456789')
                request.session['otp'] = otp
            
                

                subject = f'Welcome to Calicut University Event Management Portal'
                message = f'The otp for Creating your account is {otp}. This OTP is valid for 10 minutes'
                email_from = settings.EMAIL_HOST_USER
                recipient_list = ['vysakhprakash3@gmail.com','mrkammath@gmail.com',email]
                send_mail( subject, message, email_from, recipient_list )
                status = '1'
                return render(request,'public/publiclogin.html',{'status':status,'email':email})

            except:
                messages.success(request,('Sorry! We cannot proceed this request right now. Please try after some time'))
                return redirect('public_register')
        else:
            messages.success(request,'Username or password incorrect!')
    return render(request,'public/publiclogin.html')


def pending_varification(request):
    if 'otpvarifybtn' in request.POST:
        email = request.POST['email']
        otp = request.POST['otp']
        otpvarify = request.session['otp']
        print(otp)
        print(otpvarify)
        if otp == otpvarify:
            public_registration.objects.filter(public_email = email).update(status = '1')
            return redirect('public_login')
        else:
            messages.success(request,'OTP incorrect')
            status = '1'
            return render(request,'public/publiclogin.html',{'status':status,'email':email})





    


    return render(request,'public/publiclogin.html')