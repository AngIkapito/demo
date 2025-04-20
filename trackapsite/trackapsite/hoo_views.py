from django.shortcuts import render,redirect, HttpResponse, get_object_or_404
from django.urls import path, include, reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from app.models import CustomUser, School_Year, Salutation,Organization, MemberType, MembershipType, Member, OfficerType
from django.utils.safestring import mark_safe
from django.utils import timezone
from django.http import JsonResponse
import datetime

# Create your views here.
@login_required(login_url='/')
def home(request):
    return render(request,'hoo/home.html')

# For Schoolyear 
def ADD_SCHOOLYEAR(request):
    if request.method == "POST":
        sy_start = request.POST.get('sy_start')
        sy_end = request.POST.get('sy_end')
        # print(program_name)
        school_year = School_Year (
            sy_start = sy_start,
            sy_end = sy_end,
            created_by_id=request.user.id  # Set the created_by_username to the current user
        )
        school_year.save()
        messages.success(request, 'Cycle successfully added!')
        return redirect('add_schoolyear')
    return render(request, 'hoo/add_schoolyear.html')

def VIEW_SCHOOLYEAR(request):
    schoolyear = School_Year.objects.all()
    
    context = {
        'schoolyear':schoolyear,
    }
    # print(teacher)
    return render(request, 'hoo/view_schoolyear.html', context)


def EDIT_SCHOOLYEAR(request, id):
    schoolyear = School_Year.objects.filter(id = id)
    
    context = {
        'schoolyear':schoolyear
    }
    
    return render(request,'hoo/edit_schoolyear.html', context)


def UPDATE_SCHOOLYEAR(request):
    if request.method == "POST":
        id = request.POST.get('id')
        sy_start = request.POST.get('sy_start')
        sy_end = request.POST.get('sy_end')
        # print(program)
        
        schoolyear = School_Year.objects.get(id = id)
        schoolyear.sy_start = sy_start
        schoolyear.sy_end = sy_end
        
        schoolyear.save()
        
        messages.success(request, "Cycle successfully updated")
        return redirect('view_schoolyear')
    return render(request, 'hoo/edit_schoolyear.html')

def DELETE_SCHOOLYEAR(request, id):
    schoolyear = School_Year.objects.get(id = id)
    schoolyear.delete()
    messages.success(request, 'Cycle successfully deleted')
    return redirect('view_schoolyear')

# For Member List
def ADD_MEMBER(request):
    salutations = Salutation.objects.all()
    membershiptypes = MembershipType.objects.all()
    membertypes = MemberType.objects.all()
    officertypes = OfficerType.objects.all()
    organizations = Organization.objects.all()
    # customuser = CustomUser.objects.all()
    
    if request.method == "POST":
        # is_superuser = request.POST.get('is_superuser')
        # is_active = request.POST.get('is_active')
        # user_type = request.POST.get('user_type')
        
        membershiptype_id = request.POST.get('membershiptype_id')
        membertype_id = request.POST.get('membertype_id')
        organization_id = request.POST.get('organization_id')
        
        salutation_id = request.POST.get('salutation_id')
        officertype_id = request.POST.get('officertype_id')
        first_name = request.POST.get('first_name').upper()
        last_name = request.POST.get('last_name').upper()
        middle_name = request.POST.get('middle_name').upper()
        # profile_pic = request.FILES.get('profile_pic')
        position = request.POST.get('position').upper()
        email = request.POST.get('email')
        contact_no = request.POST.get('contact_no')
        birthdate = request.POST.get('birthdate')
        
        # Get the birthdate and convert it to a date object
        birthdate_str = request.POST.get('birthdate')
        birthdate = None
        if birthdate_str:
            try:
                birthdate = datetime.datetime.strptime(birthdate_str, '%Y-%m-%d').date()
            except ValueError:
                messages.warning(request, 'Invalid birthdate format. Please use YYYY-MM-DD.')
                return redirect('add_member')
        
        facebook_profile_link = request.POST.get('facebook_profile_link')
        # proof_of_payment = request.FILES.get('proof_of_payment')
        payment_date = request.POST.get('payment_date')
        terms_accepted = request.POST.get('terms_accepted') == 'true'
        
        username = request.POST.get('username')
        password = request.POST.get('password')
                 
        print(f"Checking email: {email}, Exists: {CustomUser .objects.filter(email=email).exists()}")              
        if email and CustomUser.objects.filter(email=email).exists():
             messages.warning(request,'Email is already taken')
             return redirect('add_member')
         
        elif CustomUser.objects.filter(username=username).exists():
             messages.warning(request,'Username is already taken')
             return redirect('add_member')     
         
        else:
            user = CustomUser(
                # is_superuser = is_superuser,
                # is_active = is_active,
                first_name = first_name,
                last_name = last_name,
                username = username,
                email = email,
                user_type = 3,
                # profile_pic = profile_pic,
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
                # proof_of_payment = proof_of_payment,
                terms_accepted = terms_accepted,
            )
            
            # member.set_password(password)
            member.save()
            
            messages.success(request,user.first_name + " " + user.last_name + " is successfully added")
            return redirect('add_member')
    
    context = {
        'salutations': salutations,  # Pass the salutations to the template
        'membershiptypes':membershiptypes,
        'membertypes': membertypes,
        'officertypes': officertypes,
        'organizations': organizations,
    }
    
    return render(request, 'hoo/add_member.html', context)

def VIEWALL_MEMBER(request):
    # customuser = request.user
    customuser = CustomUser.objects.all()
    members = Member.objects.all()
    salutations = Salutation.objects.all()
    membershiptypes = MembershipType.objects.all()
    membertypes = MemberType.objects.all()
    officertypes = OfficerType.objects.all()
    organizations = Organization.objects.all()
    
    context = {
        'customuser':customuser,
        'members':members,
        'salutations': salutations,  # Pass the salutations to the template
        'membershiptypes':membershiptypes,
        'membertypes': membertypes,
        'officertypes': officertypes,
        'organizations': organizations,
    }
    # print(customuser)
    return render(request, 'hoo/viewall_member.html', context)

def EDIT_MEMBER(request, id):
    salutations = Salutation.objects.all()
    membershiptypes = MembershipType.objects.all()
    membertypes = MemberType.objects.all()
    officertypes = OfficerType.objects.all()
    organizations = Organization.objects.all()
    
    member = get_object_or_404(Member, id=id)

    # selected_user =   # Assuming 'admin' is a ForeignKey to CustomUser 
    
    context = {
        # 'selected_user': selected_user,  # Pass the selected user to the template
        'member': member,
        'salutations': salutations,  # Pass the salutations to the template
        'membershiptypes': membershiptypes,
        'membertypes': membertypes,
        'officertypes': officertypes,
        'organizations': organizations,
    }
    
    return render(request, 'hoo/edit_member.html', context)

def UPDATE_MEMBER(request):
    if request.method == "POST":
        member_id = request.POST.get('member_id')
        is_superuser = request.POST.get('is_superuser') == 'on'  # Convert to boolean
        is_active = request.POST.get('is_active')      # Convert to boolean
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
        payment_date = request.POST.get('payment_date')
        terms_accepted = request.POST.get('terms_accepted')
        
        username = request.POST.get('username')
        password = request.POST.get('password')
        # print(program)
        
        customuser = CustomUser.objects.get(id = member_id)
        # customuser = get_object_or_404(CustomUser , id=member_id)
        
        
        # customuser.id = member_id
        customuser.is_superuser = is_superuser
        customuser.is_active = is_active
        customuser.user_type = user_type
        
        customuser.membership_type = membership_type
        customuser.member_type = member_type
        
        customuser.salutation = salutation
        customuser.first_name = first_name
        customuser.last_name = last_name
        customuser.middle_name = middle_name
        # customuser.profile_pic = request.FILES.get('profile_pic')
        customuser.position = position
        customuser.email = email
        customuser.contact_no = contact_no
        customuser.birthdate = birthdate
        customuser.facebook_profile_link = facebook_profile_link
        customuser.payment_date = payment_date
        customuser.terms_accepted = terms_accepted
        
        customuser.username = username
        customuser.password = password
        
        
        # Retrieve the user object or return a 404 error if not found
        
        if password !=None and password != "":
            customuser.set_password(password)
            
        customuser.save()
        
        messages.success(request, "Member successfully updated")
        return redirect('viewall_member')
    return render(request, 'hoo/edit_member.html')

def DELETE_MEMBER(request, id):
    customuser = CustomUser.objects.get(id = id)
    customuser.delete()
    messages.success(request, 'Member successfully deleted')
    return redirect('viewall_member')

def MEMBER_DETAILS(request,id):
    selected_member = Member.objects.filter(id = id)
    member= Member.objects.get(id=id)
    
    context = {
        'member':member,
        'selected_member':selected_member,
        # 'municipality':municipality
   
    }
    return render(request, 'hoo/member_details.html', context)
