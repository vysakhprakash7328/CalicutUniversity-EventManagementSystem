import datetime
from django.shortcuts import redirect, render
from pld.models import Event_registration

from pro_art_instrument.form import addinstrumentform, uploadimageform
from .models import instrument_details

from users.models import Main_accounts
from django.core.files.storage import FileSystemStorage


# Create your views here.


def home(request):
    id=request.session['mainuserid']
    user=request.session['mainusername']
    main=Main_accounts.objects.get(id=id)
    today = datetime.datetime.now().date()

    if main.type == "INSTRUMENTS":

        id=request.session['mainuserid']
        user=request.session['mainusername']
        instr=instrument_details.objects.all()
        ev= Event_registration.objects.filter(Event_status = 0).order_by('Event_startDate')
        return render(request,'pro and art/instrumenthome.html',{'proid':id,'user':user,'instr':instr,'ev':ev,'today':today})
    elif main.type == 'ART':
        id=request.session['mainuserid']
        user=request.session['mainusername']
        ev = Event_registration.objects.filter(Art_and_Photography = 1,Event_status = 1,art_permission = 0)
        eve = Event_registration.objects.filter(art_permission = 1)
        return render(request,'pro and art/arthome.html',{'proid':id,'user':user,'ev':ev,'eve':eve,'today':today})

    else:

        id=request.session['mainuserid']
        user=request.session['mainusername']
        ev = Event_registration.objects.filter(Art_and_Photography = 1,Event_status = 1)
        return render(request,'pro and art/index.html',{'proid':id,'user':user,'ev':ev,'today':today})

def addinstruments(request):
    id=request.session['mainuserid']
    user=request.session['mainusername']

    form = addinstrumentform(request.POST)
    if form.is_valid():
        form.save()
        return redirect('pro_home')
        
    return render(request,'pro and art/addinstruments.html',{'form':form,'proid':id,'user':user})
def update_instrument_details(request,id):
    userid=request.session['mainuserid']
    user=request.session['mainusername']
    instruments=instrument_details.objects.get(pk=id)
    form =addinstrumentform(request.POST or None, instance=instruments)
    if form.is_valid():
        form.save()
        return redirect('pro_home')
    return render(request,'pro and art/addinstruments.html',{'instruments':instruments,'form':form,'proid':userid,'user':user})


def artgrantrequest(request,Event_id):
    id=request.session['mainuserid']
    user=request.session['mainusername']
    Event_registration.objects.filter(Event_id = Event_id).update(art_permission = 1)
    ev = Event_registration.objects.filter(Art_and_Photography = 1,Event_status = 1,art_permission = 0)
    eve = Event_registration.objects.filter(art_permission = 1)
    today = datetime.datetime.now().date()

    return render(request,'pro and art/arthome.html',{'proid':id,'user':user,'ev':ev,'eve':eve,'today':today})

# def upload_image(request,Event_id):
#     id=request.session['mainuserid']
#     user=request.session['mainusername']
#     event = Event_registration.objects.filter(Event_id = Event_id)
#     form = uploadimageform(request.POST or None , request.FILES, instance = event)
#     if request.method == "POST":
#         if form.is_valid:
#             form.save()
#     return render(request,'pro and art/uploadimage.html',{'form':form,'proid':id,'user':user})

def upload_image(request,Event_id):
    userid=request.session['mainuserid']
    user=request.session['mainusername']

    event =  Event_registration.objects.filter(Event_id = Event_id).first()
    print(event)
    form = uploadimageform(request.POST or None, request.FILES, instance=event)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = uploadimageform()
    return render(request, 'pro and art/uploadimage.html', {
        'form': form,
        'proid':id,
        'user':user
    })