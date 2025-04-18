from django.shortcuts import render,redirect, HttpResponse
from django.contrib.auth import authenticate, logout, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from app.models import CustomUser, School_Year, Salutation, MembershipType, MemberType
from django.utils.safestring import mark_safe
from django.urls import path, include, reverse
from datetime import datetime

# Create your views here.

def BASE(request):
    current_year = datetime.now().year
    return render(request,'base.html',{'current_year': current_year})

def HOME(request):
    return render(request,'home.html')

def ABOUT(request):
    return render(request,'about.html')

def CONTACT(request):
    return render(request,'contact.html')

def ANNOUNCEMENT(request):
    return render(request,'announcement.html')

def EVENT(request):
    return render(request,'event.html')

def LOGIN(request):
    return render(request,'login.html')

def ERRORPAGE(request):
    return render(request,'error_page.html')

def REGISTRATION(request):
    if request.method == "POST":
        first_name = request.POST.get('first_name').upper()
        last_name = request.POST.get('last_name').upper()
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Check if the email is already taken
        if email and CustomUser .objects.filter(email=email).exists():
            messages.warning(request, 'Email is already taken')
            return redirect('registration')

        # Check if the username is already taken
        elif CustomUser .objects.filter(username=username).exists():
            messages.warning(request, 'Username is already taken')
            return redirect('registration')
        
        else:
            # Create a new user if email and username are unique
            user = CustomUser (
                first_name=first_name,
                last_name=last_name,
                username=username,
                email=email,
                user_type=3,  # Adjust this based on your user type logic
            )
            
            user.set_password(password)  # Hash the password
            user.save()  # Save the user to the database
            # try:
            #     user.save()  # Save the user to the database
            #     # Prepare a success message with a login link
            login_link = reverse('login')  # Assuming 'login' is the name of your login URL pattern
            login_message = f'{user.first_name} {user.last_name} is successfully added. <a href="{login_link}">Click here to login.</a>'
            messages.success(request, mark_safe(login_message))
            # except Exception as e:
            #     messages.error(request, 'An error occurred while creating your account. Please try again.')
        return redirect('registration')

    return render(request, 'registration.html')  # Render the registration form if not a POST request

#feb282025
def doLogin(request):
    if request.method == "POST":
        username = request.POST.get('email')
        password = request.POST.get('password')
        remember_me = request.POST.get('remember_me')  # Get the value of the checkbox
        user = authenticate(request=request, username=username, password=password)

        if user is not None:
            login(request, user)
            user_type = user.user_type
            
            # Set session expiry based on "Remember Me" checkbox
            if remember_me:
                request.session.set_expiry(2592000)  # 30 days in seconds
            else:
                request.session.set_expiry(0)  # Session expires when the browser is closed

            # Redirect based on user type
            if user_type == '1':
                return redirect('hoo_home')
            elif user_type == '2':
                return redirect('officer_home')
            elif user_type == '3':
                return redirect('member_home')
            else:
                messages.error(request, 'Invalid user type.')
                return redirect('login')
        else:
            messages.error(request, 'Email and Password are Invalid')
            return redirect('login')
            
def doLogout(request):
    logout(request)
    return redirect('homepage')

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
        elif CustomUser.objects.filter(username=username).exists():
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

# Pagamit ito sa mga SSITE officer para mag add ng mga members sa 
# System using trackapsite.com/registration_bypass1/
def REGISTRATION_BYPASS1(request):
    
    if request.method == "POST":
        is_superuser = request.POST.get('is_superuser')
        is_active = request.POST.get('is_active')
        user_type = request.POST.get('user_type')
        
        membership_type = request.POST.get('membership_type')
        member_type = request.POST.get('member_type')
        
        salutation = request.POST.get('salutation')
        first_name = request.POST.get('first_name').upper()
        last_name = request.POST.get('last_name').upper()
        middle_name = request.POST.get('middle_name').upper()
        # profile_pic = request.FILES.get('profile_pic')
        position = request.POST.get('position').upper()
        email = request.POST.get('email')
        contact_no = request.POST.get('contact_no')
        birthdate = request.POST.get('birthdate')
        facebook_profile_link = request.POST.get('facebook_profile_link')
        # proof_of_payment = request.FILES.get('proof_of_payment')
        # payment_date = request.POST.get('payment_date')
        # terms_accepted = request.POST.get('terms_accepted')
        
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
                is_superuser = is_superuser,
                is_active = is_active,
                user_type = user_type,
                
                membership_type = membership_type,
                member_type = member_type,
                
                salutation = salutation,
                first_name = first_name,
                last_name = last_name,
                middle_name = middle_name,
                birthdate = birthdate,
                # profile_pic = profile_pic,
                position = position,
                contact_no = contact_no,
                facebook_profile_link = facebook_profile_link,
                # proof_of_payment = proof_of_payment,
                # payment_date = payment_date,
                # terms_accepted = terms_accepted,
                
                username = username,
                email = email if email else None,
                )        
            user.set_password(password)
            user.save()
            
            login_link = reverse('login')  # Assuming 'login' is the name of your login URL pattern
            login_message = f'{user.first_name} {user.last_name} is successfully added. <a href="{login_link}">Click here to login.</a>'
            messages.success(request, mark_safe(login_message))
            return redirect('registration_bypass1')
    
    return render(request, 'registration_bypass1.html', {
    })

@login_required(login_url='/')  
def PROFILE(request):
    user = CustomUser.objects.get(id = request.user.id)
    
    context = {
        "user":user,

    }
    return render(request, 'profile.html', context)

@login_required(login_url='/')
def PROFILE_UPDATE(request):
    if request.method == "POST":
        profile_pic = request.FILES.get('profile_pic')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        # print(profile_pic, first_name, last_name, email, username, password)
        
        try:
            customuser = CustomUser.objects.get(id = request.user.id)

            customuser.first_name = first_name
            customuser.last_name = last_name
            
            if password !=None and password != "":
                customuser.set_password(password)
            
            if profile_pic !=None and profile_pic != "":
                customuser.profile_pic = profile_pic

            customuser.save()
            messages.success(request,'Your Profile updated successfully! You will be redirected to Login page')
            return redirect('profile')
        except:
            messages.error(request, 'Failed to update your profile')
    return render(request,'profile.html')    
