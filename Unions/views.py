from django.shortcuts import render

from .forms import  UnionRegistrationForm
from django.shortcuts import render, redirect
from Unions.models import unions


def union_home(request):
    unionid=request.session['unionid']
    unionname=request.session['unionname']
    return render(request,'dpartment/department.html',{'unionid':unionid,'user':unionname})

def union_request(request):
    if request.method == "POST":
        unionname = request.POST['unionname']
        unionmail = request.POST['unionmail']
        presidentname = request.POST['presidentname']
        presidentphone = request.POST['presidentphone']
        secretaryname = request.POST['secretaryname']
        secretaryphone = request.POST['secretaryphone']

        unions(union_name = unionname,union_email = unionmail,president_name = presidentname,president_phone = presidentphone,secretary_name = secretaryname,secretary_phone = secretaryphone).save()
        
            
        return redirect('login')

    else:
        return render(request,'unions/unionregistration.html')

