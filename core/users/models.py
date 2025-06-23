from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager,PermissionsMixin
from django.conf import settings
from django.utils import timezone
from datetime import timedelta

class CustomUserManager(BaseUserManager):
    def create_user(self,email,first_name,last_name,phone_number,password=None,**extra_fields):
        if not email:
            raise ValueError("Email is Requried")
        if not first_name:
            raise ValueError("first_name is Requried")
        if not last_name:
            raise ValueError("last_name is Requried")
        if not phone_number:
            raise ValueError("phone_number is Requried")
        
        email = self.normalize_email(email)
        user = self.model(
            email = email,
            first_name = first_name,
            last_name = last_name,
            phone_number = phone_number,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, first_name, last_name, phone_number, password=None, **extra_fields):
        extra_fields.setdefault('is_active',True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser',True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        if extra_fields.get('is_staff') is not True:
            raise ValueError("Superuser must have is_staff=True.")
        
        return self.create_user(
            email, first_name, last_name, phone_number, password, **extra_fields
        )
        
class User(AbstractBaseUser,PermissionsMixin):

    ROLE_CHOICES = [
        ('admin','Admin'),
        ('staff','Staff'),
        ('user','User'),
    ]

    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=10)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    role = models.CharField(max_length=20,choices=ROLE_CHOICES,default='user')

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name','last_name','phone_number']

    def __str__(self):
        return self.email
    

class EmailVerificationCode(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    is_used = models.BooleanField(default=False)

    def has_expired(self):
        return timezone.now() > self.expires_at
    
    def __str__(self):
        return f"{self.user.email} - {self.code}"