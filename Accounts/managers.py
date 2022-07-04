from locale import normalize
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager,PermissionsMixin
from django.core.mail import send_mail

class MyaccountManager(BaseUserManager):
    
    def create_user(self,email,name,password):
        
        if not email:
            raise ValueError('user must have a valid email address')
        if not name:
            raise ValueError('user must have a name')
        
        # if not phone:
        #     raise ValueError('user must have a phone number')
        
        user=self.model(
            email=self.normalize_email(email),
            name=name,
            
        )
        
        user.set_password(password)
        user.save(using=self._db)
        
        return user
    
    
    def create_superuser(self,email,name,password=None):
        user=self.create_user(
            email=self.normalize_email(email),
            name=name,
            password=password,
           
        )
        
        user.is_admin=True
        user.is_active=True
        user.is_superuser=True
        user.is_staff=True
        user.save(using=self._db)
        
        return user