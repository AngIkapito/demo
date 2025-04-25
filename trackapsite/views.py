from django.shortcuts import render,redirect, HttpResponse
from django.contrib.auth import authenticate, logout, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from app.models import CustomUser, School_Year, Salutation, Member, MembershipType, MemberType, Announcement, OfficerType, Organization
from django.utils.safestring import mark_safe
from django.urls import path, include, reverse
from datetime import datetime
from taggit.models import Tag

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
    announcements = Announcement.objects.prefetch_related('tags').all()
    tags = Tag.objects.all()
    query = request.GET.get('tags')
    
    if query:
        results = Tag.objects.filter(tags__name__icontains=query)  # Adjust based on your model's tag field
    else:
        results = Tag.objects.all()  # Show all items if no query
    
    # Get all announcements and order them by updated_at date, descending
    announcements = Announcement.objects.all().order_by('-updated_at')
    
    # Get the latest announcement
    latest_announcement = announcements.first()  # This will be the latest announcement
    
    context = {
        'announcements': announcements, 
        'tags': tags, 
        'results': results, 
        'latest_announcement': latest_announcement
        }
    return render(request,'announcement.html', context)


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
            messages.success(request,'Your Profile updated successfully!')
            return redirect('profile')
        except:
            messages.error(request, 'Failed to update your profile')
    return render(request,'profile.html')    


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
    salutations = Salutation.objects.all()
    membershiptypes = MembershipType.objects.all()
    membertypes = MemberType.objects.all()
    officertypes = OfficerType.objects.all()
    organizations = Organization.objects.all()
    # customuser = CustomUser.objects.all()
    
    if request.method == "POST":
        # is_superuser = request.POST.get('is_superuser')
        first_name = request.POST.get('first_name').upper()
        last_name = request.POST.get('last_name').upper()
        email = request.POST.get('email').strip().lower()
        
        username = request.POST.get('username').strip().lower()
        password = request.POST.get('password')
        
        membershiptype_id = request.POST.get('membershiptype_id')
        membertype_id = request.POST.get('membertype_id')
        organization_id = request.POST.get('organization_id')
        
        salutation_id = request.POST.get('salutation_id')
        officertype_id = request.POST.get('officertype_id')
        middle_name = request.POST.get('middle_name').upper()
        profile_pic = request.FILES.get('profile_pic')
        position = request.POST.get('position').upper()
        contact_no = request.POST.get('contact_no')
        birthdate = request.POST.get('birthdate')
        
        # Get the birthdate and convert it to a date object
        # birthdate_str = request.POST.get('birthdate')
        # birthdate = None
        # if birthdate_str:
        #     try:
        #         birthdate = datetime.datetime.strptime(birthdate_str, '%Y-%m-%d').date()
        #     except ValueError:
        #         messages.warning(request, 'Invalid birthdate format. Please use YYYY-MM-DD.')
        #         return redirect('registration_bypass1')
        
        facebook_profile_link = request.POST.get('facebook_profile_link')
        proof_of_payment = request.FILES.get('proof_of_payment')
        payment_date = request.POST.get('payment_date')
        terms_accepted = request.POST.get('terms_accepted') == 'true'
        
                 
        print(f"Checking email: {email}, Exists: {CustomUser .objects.filter(email=email).exists()}")              
        if email and CustomUser.objects.filter(email=email).exists():
             messages.warning(request,'Email is already taken')
             return redirect('registration_bypass1')
         
        elif CustomUser.objects.filter(username=username).exists():
             messages.warning(request,'Username is already taken')
             return redirect('registration_bypass1')     
         
        else:
            user = CustomUser(
                is_superuser = 0,
                is_active = 0,
                user_type = 3,
                first_name = first_name,
                last_name = last_name,
                username = username,
                email = email,
                profile_pic = profile_pic,
                )      
              
            user.set_password(password)
            user.save()
            
            member = Member(
                admin = user, 
                membershiptype_id = membershiptype_id,
                membertype_id = membertype_id,
                officertype_id = officertype_id,
                organization_id = organization_id,
                
                salutation_id = salutation_id,
                middle_name = middle_name,
                birthdate = birthdate,
                position = position,
                contact_no = contact_no,
                facebook_profile_link = facebook_profile_link,
                payment_date = payment_date,
                proof_of_payment = proof_of_payment,
                terms_accepted = terms_accepted,
            )
            
            member.save()
            
            home_link = reverse('home')  # Assuming 'login' is the name of your login URL pattern
            registration_message = f'{user.first_name} {user.last_name}. Kindly wait for the verification of your Membership. <br>Your default credentials will be sent via your Email. <a href="{home_link}">Click here to go to Homepage.</a>'
            messages.success(request, mark_safe(registration_message))
            # messages.success(request,user.first_name + " " + user.last_name + ", Kindly wait for the confirmation sent via your Email")
            # return redirect('home')
    
    context = {
        'salutations': salutations,  # Pass the salutations to the template
        'membershiptypes':membershiptypes,
        'membertypes': membertypes,
        'officertypes': officertypes,
        'organizations': organizations,
    }
    
    return render(request, 'registration_bypass1.html', context)
