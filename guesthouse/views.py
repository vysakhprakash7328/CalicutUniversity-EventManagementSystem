from django.shortcuts import render, redirect
from guesthouse.forms import roomdetailsform

from guesthouse.models import guesthouse_rooms,bookingDetails
from pld.models import Main_accounts

# Create your views here.
def guest_home(request):
    rooms = guesthouse_rooms.objects.all()
    if request.session.get('mainuserid'):
        id=request.session['mainuserid']
        name=request.session['mainusername']
        return render(request,'guesthouse/guesthome.html',{'mainuserid':id,'user':name,'rooms':rooms})
    elif request.session.get('unionid'):
        id=request.session['unionid']
        name=request.session['unionname']
        return render(request,'guesthouse/guesthome.html',{'unionid':id,'user':name,'rooms':rooms})
    elif request.session.get('id'):
        id=request.session['id']
        name=request.session['department_username']
        return render(request,'guesthouse/guesthome.html',{'id':id,'user':name,'rooms':rooms})
    elif request.session.get('head_id'):
        id=request.session['head_id']
        name=request.session['head_username']
        return render(request,'guesthouse/guesthome.html',{'id':id,'user':name,'rooms':rooms})
    elif request.user.is_authenticated:
        return render(request,'guesthouse/guesthome.html',{'rooms':rooms})

def add_rooms(request):
    id=request.session['mainuserid']
    name=request.session['mainusername']
    if request.method == 'POST':
        form=roomdetailsform(request.POST or None , request.FILES)
        if form.is_valid():
            form.save()
            return redirect('guest_home')
    else:
        form=roomdetailsform()

    return render(request,'guesthouse/addrooms.html',{'mainuserid':id,'user':name,'form':form})





def accomodation(request):
    rooms = guesthouse_rooms.objects.all()
    if request.session.get('mainuserid'):
            id=request.session['mainuserid']
            name=request.session['mainusername']
    return render(request,'guesthouse/accomodation.html',{'mainuserid':id,'user':name,'rooms':rooms})




def update_rooms(request,room_id):
    room=guesthouse_rooms.objects.get(pk=room_id)
    print(room)
    if request.session.get('mainuserid'):
        id=request.session['mainuserid']
        name=request.session['mainusername']
        form=roomdetailsform(request.POST or None,request.FILES or None, instance=room)
        if form.is_valid():
            form.save()
            return redirect('guest_home')
    else:
        form=roomdetailsform()
    return render(request,'guesthouse/updaterooms.html',{'mainuserid':id,'user':name,'form':form})







def bookings(request):
    roomType=guesthouse_rooms.objects.all()
    if request.session.get('mainuserid'):
        id=request.session['mainuserid']
        name=request.session['mainusername']
        return render(request,'guesthouse/bookings.html',{'mainuserid':id,'user':name,'roomType':roomType})
    elif request.session.get('id'):
        id=request.session['id']
        name=request.session['department_username']
        return render(request,'guesthouse/bookings.html',{'id':id,'user':name,'roomType':roomType})
    elif request.user.is_authenticated:
        return render(request,'guesthouse/bookings.html',{'roomType':roomType})
    for i in roomType:
        print(i.room_type)
    return render(request,'guesthouse/bookings.html',{'roomType':roomType})




def bookroom(request):
    rooms = guesthouse_rooms.objects.all()

    if request.method=='POST':
        b=bookingDetails()
        b.room_type=request.POST['roomtype']
        b.number_of_rooms=request.POST['numberofrooms']
        b.name=request.POST['name']
        b.check_in=request.POST['checkin']
        b.check_out=request.POST['checkout']
        b.number_of_persons=request.POST['numberofpersons']

        room_typ=request.POST['roomtype']

        room_types=guesthouse_rooms.objects.get(room_type=room_typ)
        b.room_rate=room_types.room_rent
        b.status=-0
        if request.session.get('mainuserid'):
            id=request.session['mainuserid']
            personname=Main_accounts.objects.get(id=id)
            b.person_name=personname.type
        else:
            b.person_name=request.user

        b.save()
        return redirect('guest_home')





def mybookings(request):
    
    if request.session.get('mainuserid'):
        id=request.session['mainuserid']
        name=request.session['mainusername']
        personname=Main_accounts.objects.get(id=id)
        data=bookingDetails.objects.filter(person_name=personname.type)
        print(data)
        return render(request,'guesthouse/mybookings.html',{'mainuserid':id,'user':name,'data':data})
    elif request.user:
        data=bookingDetails.objects.filter(person_name=request.user)
        return render(request,'guesthouse/mybookings.html',{'data':data})

    return render(request,'guesthouse/mybookings.html')




def allbookings(request):
    data=bookingDetails.objects.all()
    if request.session.get('mainuserid'):
        id=request.session['mainuserid']
        name=request.session['mainusername']
        return render(request,'guesthouse/allbookings.html',{'mainuserid':id,'user':name,'data':data})




def roomcancel(request,bookid):
    book=bookingDetails.objects.filter(booking_id=bookid).update(status=3)
    return redirect('allbookings')



def aprovebooking(request,bookid):
    book=bookingDetails.objects.filter(booking_id=bookid).update(status=2)
    return redirect('allbookings')

def deletebooking(request,bookid):
    book=bookingDetails.objects.get(booking_id=bookid).delete()
    return redirect('mybookings')


def editbooking(request,bookid):
    data=bookingDetails.objects.get(booking_id=bookid)
    roomType=guesthouse_rooms.objects.all()
    if request.session.get('mainuserid'):
        id=request.session['mainuserid']
        name=request.session['mainusername']
        return render(request,'guesthouse/bookings.html',{'mainuserid':id,'user':name,'data':data,'roomType':roomType})

    return render(request,'guesthouse/bookings.html',{'data':data,'roomType':roomType})

def edit(request,bookid):
    booking=bookingDetails.objects.get(booking_id=bookid)
    if request.method=='POST':
        room_type=request.POST['roomtype']
        number_of_rooms=request.POST['numberofrooms']
        name=request.POST['name']
        check_in=request.POST['checkin']
        check_out=request.POST['checkout']
        number_of_persons=request.POST['numberofpersons'] 
        room_typ=request.POST['roomtype']
        room_types=guesthouse_rooms.objects.get(room_type=room_typ)
        if booking.status!=0:
            bookingDetails.objects.filter(booking_id=bookid).update(status=0)
        room_rate=room_types.room_rent
        bookingDetails.objects.filter(booking_id=bookid).update(room_type=room_type,number_of_rooms=number_of_rooms,name=name,check_in=check_in,check_out=check_out,number_of_persons=number_of_persons,room_rate=room_rate)

    return redirect('mybookings')