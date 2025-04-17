from django.shortcuts import render,redirect, HttpResponse
from django.urls import path, include
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from app.models import CustomUser
from django.utils.safestring import mark_safe
#from django.http import JsonResponse

@login_required(login_url='/')
def home(request):
    return render(request,'member/home.html')

def REGISTRATION_BYPASS(request):
   
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
                      
        if email and CustomUser.objects.filter(email=email).exists():
             messages.warning(request,'Email is already taken')
             return redirect('registration')
        if CustomUser.objects.filter(username=username).exists():
             messages.warning(request,'Username is already taken')
             return redirect('registration')     
        else:
            user = CustomUser(
                first_name = first_name,
                last_name = last_name,
                username = username,
                email = email if email else None,
                user_type = 3,
                )        
            user.set_password(password)
            user.save()
            
            login_link = reverse('login')  # Assuming 'login' is the name of your login URL pattern
            login_message = f'{user.first_name} {user.last_name} is successfully added. <a href="{login_link}">Click here to login.</a>'
            messages.success(request, mark_safe(login_message))
            return redirect('registration_bypass')
    
    return render(request, 'registration_bypass.html')

