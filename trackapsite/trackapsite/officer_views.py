from django.shortcuts import render,redirect, HttpResponse
from django.urls import path, include
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from app.models import CustomUser, School_Year
from django.utils.safestring import mark_safe
#from django.http import JsonResponse

@login_required(login_url='/')
def home(request):
    return render(request,'officer/home.html')

# def REGISTRATION_OFFICER(request):
   
#     if request.method == "POST":
#         profile_pic = request.FILES.get('profile_pic')
#         first_name = request.POST.get('first_name').upper()
#         last_name = request.POST.get('last_name').upper()
#         username = request.POST.get('username')
#         password = request.POST.get('password')
#         email = request.POST.get('email')
#         #gender = request.POST.get('gender')
#         mobile = request.POST.get('mobile')
        
#         if  CustomUser.objects.filter(email=email).exists():
#              messages.warning(request,'Email is already taken')
#              return redirect('login')
#         if  CustomUser.objects.filter(username=username).exists():
#              messages.warning(request,'Username is already taken')
#              return redirect('login')     
#         else:
#             user = CustomUser(
#                 first_name = first_name,
#                 last_name = last_name,
#                 username = username,
#                 email = email,
#                 profile_pic = profile_pic,  
#                 user_type = 2,
#             )        
#             user.set_password(password)
#             user.save()
            
#             officer = Officer (
#                 admin = user,
#                 #gender = gender,
#                 mobile = mobile,
#                 # district_id_id = district_id,
#                 # municipality_id_id = municipality_id,
#                 # barangay_id_id = barangay_id,
#                 # province_id_id = province_id,
#                 # region_id_id = region_id
             

#             )
#             officer.save()
            
           
#             login_link = reverse('login')  # Assuming 'login' is the name of your login URL pattern
#             login_message = f'{user.first_name} {user.last_name} is successfully registered. <a href="{login_link}">Click here to login.</a>'
#             # return redirect('login')
#             messages.success(request, mark_safe(login_message))
#             return redirect('registration_officer')
    

#     # context = {
#     #     'region': region,
#     #     'province': province
#     # }
#     #return render(request, 'registration_teacher.html', context)
    
#     return render(request, 'registration_officer.html')