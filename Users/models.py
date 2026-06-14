from django.db import models
from django.contrib.auth.models import BaseUserManager,PermissionsMixin,AbstractBaseUser
from verification.service import EmailVerification,TempEmployeeCredentials
from organization.models import Organization
# Create your models here.


class CustomManager(BaseUserManager):
    def create_user(self, email,password,**otherfields):
        if not email:
            raise ValueError('u must provide a email')
        email=self.normalize_email(email)        
        user=self.model(email=email,**otherfields)
        if user.role==self.model.roles.FOUNDER:
            user.is_verified=False
            
            
        else:

            user.is_password_temp=True

            
        
        user.set_password(password)
        
        user.save()
        
            
        
        return user
    def create_superuser(self, email,password,**otherfields):
        otherfields.setdefault('is_active',True)
        otherfields.setdefault('is_staff',True)
        otherfields.setdefault('is_superuser',True)
        return self.create_user(email,password,**otherfields)



    

class employees(AbstractBaseUser,PermissionsMixin):

    class roles(models.TextChoices):
        FOUNDER='F','Founder'
        EMPLOYEE='E','Employee'
    email=models.EmailField(unique=True)
    user_name=models.CharField(max_length=255, unique=True)
    first_name=models.CharField(max_length=255)
    last_name=models.CharField(max_length=255,null=True)
    bio_pitcure=models.ImageField(upload_to='profiles/',null=True,blank=True)
    created_at=models.DateTimeField(auto_now=True)
    role=models.CharField(max_length=1, choices=roles.choices,default=roles.FOUNDER)
    is_active=models.BooleanField(default=True)
    is_password_temp=models.BooleanField(default=False)
    is_verified=models.BooleanField(default=True)
    created_organization=models.BooleanField(default=False)
    organization=models.ForeignKey(Organization,on_delete=models.CASCADE,null=True ,blank=True)
    last_login_act=models.DateTimeField(null=True,blank=True)

        

    is_staff=models.BooleanField(default=False)

    objects=CustomManager()
    USERNAME_FIELD='email'
    REQUIRED_FIELDS=['first_name','user_name','last_name']
    def __str__(self):
        return self.user_name
    

