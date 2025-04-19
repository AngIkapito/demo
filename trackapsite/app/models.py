from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
import datetime
from taggit.managers import TaggableManager

# Create your models here.
class CustomUser(AbstractUser):
    # User information
    USER = (
        (1, 'hoo'),
        (2, 'officer'),
        (3, 'member'),
    )
    user_type = models.CharField(choices=USER, max_length=25)
    profile_pic = models.ImageField(upload_to='profile_pic/')
    email = models.EmailField(max_length=150, unique=True)
    
class Salutation(models.Model):
    name = models.CharField(max_length=20)
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='salutations')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
        
class Region(models.Model):
    name = models.CharField(max_length=100)
    info = models.CharField(max_length=100)
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='regions')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
class Organization(models.Model):
    initials = models.CharField(max_length=10)
    name = models.CharField(max_length=200)
    type = models.CharField(max_length=100)
    logo = models.ImageField(upload_to='org_logo/')
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='organizations')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
class Announcement(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()  # Changed to TextField for longer descriptions
    banner = models.ImageField(upload_to='announcement/')  # Simplified upload path
    status = models.BooleanField(default=True)
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='announcements')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    tags = TaggableManager()
    
    def __str__(self):
        return self.title
    
class School_Year(models.Model):
    sy_start = models.DateField()
    sy_end = models.DateField()
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='schoolyears')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.sy_start.year}-{self.sy_end.year}"
    
class MemberType(models.Model):
    name = models.CharField(max_length=100)
    info = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='membertypes')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name

class MembershipType(models.Model):
    name = models.CharField(max_length=100)
    info = models.CharField(max_length=100)
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='membershiptypes')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
class OfficerType(models.Model):
    name = models.CharField(max_length=100)
    info = models.CharField(max_length=100)
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='officertypes')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
 
class Member(models.Model):
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    
    #Personal Information of Member
    middle_name = models.CharField(max_length=100,default="")
    contact_no = models.CharField(max_length=13,default="")
    birthdate = models.DateField(null=True, blank=True)
    gender =  models.CharField(max_length=6)
    
    #Membership Information
    officertype = models.ForeignKey(OfficerType, on_delete=models.CASCADE)
    membershiptype = models.ForeignKey(MembershipType, on_delete=models.CASCADE)
    membertype = models.ForeignKey(MemberType, on_delete=models.CASCADE)
    salutation = models.ForeignKey(Salutation, on_delete=models.CASCADE)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    
    position = models.CharField(max_length=50)
    facebook_profile_link = models.URLField(blank=True, null=True)
    proof_of_payment = models.FileField(upload_to='payments/')
    payment_date = models.DateField(null=True, blank=True)
    terms_accepted = models.BooleanField(default=False, null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.admin.first_name + " " + self.admin.last_name
    
    