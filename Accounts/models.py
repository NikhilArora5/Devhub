from ast import Mod
from pickle import TRUE
from django.db import models
import email
from enum import unique
from operator import mod
from re import L
import re
from statistics import mode
from tokenize import blank_re
from unicodedata import name
from unittest.util import _MAX_LENGTH
from wsgiref.validate import validator
from django.db import models
from locale import normalize
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager,PermissionsMixin
from phonenumber_field.modelfields import PhoneNumberField
from phonenumbers import region_code_for_country_code
from django.core.validators import RegexValidator
from .managers import MyaccountManager
import uuid
#from django.contrib.auth.models import 
#from manager import MyaccountManager


#validating Phone number
phone_regex = RegexValidator(regex=r'^\+?91?\d{10}$', message="Phone number must be entered in the format: '+91XXXXXXXXXX'. Up to 10 digits allowed.")
# Create your models her



class Account(AbstractBaseUser,PermissionsMixin):
    email=models.EmailField(verbose_name='email',max_length=60,unique=True)
    
    
    name=models.CharField(max_length=30,unique=False)
    last_login=models.DateTimeField(verbose_name='last login' ,auto_now=True)
    is_admin=models.BooleanField(default=False)
    is_active=models.BooleanField(default=True)
    is_staff=models.BooleanField(default=False)
    is_superuser=models.BooleanField(default=False)
    email_confirmed=models.BooleanField(default=False)
    phone=PhoneNumberField(null=True,blank=True,unique=False,validators=[phone_regex])
    created= models.DateTimeField(verbose_name='created', auto_now_add=True)
    location = models.CharField(max_length=200, blank=True, null=True)
    short_intro = models.CharField(max_length=200, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    profile_image = models.ImageField(
        null=True, blank=True, upload_to='profiles/', default="profiles/user-default.png")
    social_github = models.CharField(max_length=200, blank=True, null=True)
    social_twitter = models.CharField(max_length=200, blank=True, null=True)
    social_linkedin = models.CharField(max_length=200, blank=True, null=True)
    social_youtube = models.CharField(max_length=200, blank=True, null=True)
    social_website = models.CharField(max_length=200, blank=True, null=True)
    
    
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)

    
    
    
    
    objects=MyaccountManager()
    USERNAME_FIELD='email'
    
    REQUIRED_FIELDS=["name"]
    
    
    
    
    def __str__(self):
        return str(f'  {self.name}  ')
    
    def get_email(self):
        return self.email
    
    def get_name(self):
        return self.name
    
    def get_contact(self):
        return self.phone
    
    def has_perm(self,perm,obj=None):
        return self.is_admin
    
    def has_module_perms(self, app_label):
        return True


class skill(models.Model):
    owner=models.ForeignKey(Account,null=True,blank=True,on_delete=models.CASCADE)
    name=models.TextField(max_length=30,unique=False)
    description=models.CharField(max_length=400, blank=True, null=True)
    created=models.DateTimeField(auto_now_add=True)
    id=models.UUIDField(default=uuid.uuid4,unique=True,primary_key=True,editable=False)

    def __str__(self):
        return str(self.name)


class Message(models.Model):
    sender = models.ForeignKey(
        Account, on_delete=models.SET_NULL, null=True, blank=True)
    recipient = models.ForeignKey(
        Account, on_delete=models.SET_NULL, null=True, blank=True, related_name="messages")
    name = models.CharField(max_length=200, null=True, blank=True)
    email = models.EmailField(max_length=200, null=True, blank=True)
    subject = models.CharField(max_length=200, null=True, blank=True)
    body = models.TextField()
    is_read = models.BooleanField(default=False, null=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)

    def __str__(self):
        return self.subject

    class Meta:
        ordering = ['is_read', '-created']
# Create your models here.
