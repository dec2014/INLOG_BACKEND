from .models import employees
from rest_framework.exceptions import ValidationError
from django.db import IntegrityError,transaction
from rest_framework.response import Response
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from Users.models import employees
from organization.service import get_organization_by_founder
from streak.service import get_streak
from .email import TempEmployeeCredentials
from follow.service import user_following_list_exists,organization_following_list_exists

def current_user_logined(id):
    try:
        current_user=employees.objects.select_related('organization').get(pk=id)
        return current_user
    except IntegrityError as e:
        raise ValidationError('cannot find the user')
    
def get_user(id):
    try:
        current_user=employees.objects.get(pk=id)
        return current_user
    except IntegrityError as e:
        raise ValidationError('cannot find the user')

def get_employee__organization(id):
    try:
        current_user=employees.objects.select_related('organization').get(id)
        return current_user
    except IntegrityError as e:
        raise ValidationError('cannot find the user')

def get_all_employee__organization():
    try:
        current_user=employees.objects.select_related('organization').all()
        return current_user
    except IntegrityError as e:
        raise ValidationError('cannot find the user')


def total_employees_organization(id):
    return employees.objects.filter(organization_id=id).count()

def get_all_employees():
    return employees.objects.all()

def employees_organization_all(id):
    return employees.objects.select_related('organization').filter(organization_id=id)

@transaction.atomic
def verification_user(self, request, *args, **kwargs):
    try:
        u=kwargs.get('uuid')
        uuid=urlsafe_base64_decode(u).decode()
        user=get_user(uuid)
        token=kwargs.get('token','')
        if default_token_generator.check_token(user,token):
            user.is_verified=True
            user.save()
            return Response('verification successfull')
    except Exception as e:
        raise ValidationError({
            'error':'could not verify the user',
            'details':str(e)
        })
    
@transaction.atomic
def employee_create(self, request, *args, **kwargs):
    try:
        email=request.data.get('email','')
        password=request.data.get('password','')
        TempEmployeeCredentials(email,password)
        serializer=self.get_serializer(data=request.data)
        if serializer.is_valid():
            
            organization=get_organization_by_founder(request.user.id)
            # user.organization=organization
            serializer.save(is_password_temp=True,organization=organization)
            get_streak(serializer.data['id'])
            return Response(serializer.data)
    except Exception as e:
        raise ValidationError({
            'error':'could not create the employee',
            'details':str(e)
        })
    

@transaction.atomic
def change_password(self, request, *args, **kwargs):
    try:
        user=request.user
        serializer=self.get_serializer(user,data=request.data)
        if serializer.is_valid():
            serializer.save(is_password_temp=False)
            return Response('password changed successfully')
    except Exception as e:
        raise ValidationError({
            'error':'could not change the password.',
            'details':str(e)
        })


@transaction.atomic
def force_password_change_by_founder(self, request, *args, **kwargs):
    try:
        user=get_user(kwargs.get('pk'))
        if request.user.role !='F':
            raise ValidationError('you cannot perform the action as you are not the founder of the organizaiton')

        if request.user.id==user.id:
            raise ValidationError('you cannot force yourself the founder to force change your password.')

        if request.user.organization_id!=user.organization_id:
            raise ValidationError('you can only force change the password of employee who belong to your organization')

        user.is_password_temp=True
        user.save()
        return Response('password force changed successfully')
    except Exception as e:
        raise ValidationError({
            'error':'could not force change the password.',
            'details':str(e)
        })
    
@transaction.atomic
def password_change_by_founder_of_employee(self, request, *args, **kwargs):
    try:
        user=get_user(kwargs.get('pk'))
        if request.user.role !='F':
            raise ValidationError('you cannot perform the action as you are not the founder of the organizaiton')

        if request.user.id==user.id:
            raise ValidationError('you cannot force yourself the founder to force change your password.')

        if request.user.organization_id!=user.organization_id:
            raise ValidationError('you can only force change the password of employee who belong to your organization')

        password=request.data.get('password','')
        email=user.email
        serializer=self.get_serializer(user,data=request.data)
        if serializer.is_valid():
            serializer.save()
            TempEmployeeCredentials(email,password)
            return Response('password changed for the employee')
    except Exception as e:
        raise ValidationError({
            'error':'could not change the password of the employee.',
            'details':str(e)
        })
    


@transaction.atomic
def list_employee(self, request, *args, **kwargs):
    obj=get_employee__organization(kwargs.get('pk'))
    if obj.organization.type=='Pvt':
        following_exists=user_following_list_exists(request.user.id,obj.organization_id)
        organizationfollowing_exists=organization_following_list_exists(request.user.organization_id, obj.organization_id)
        if request.user.organization==obj.organization or following_exists or organizationfollowing_exists :
            obj_all=employees_organization_all(kwargs.get.id)
            serializer=self.get_serializer(obj_all,many=True)
            return Response(serializer.data)

        else :
            self.message=f'you must belong to or follow the organization {obj.blog.organization.Name} to get the employee '
            return False
        
    elif obj.organization.type=='Pub':
        obj_all=employees_organization_all(kwargs.get.id)
        serializer=self.get_serializer(obj_all,many=True)
        return Response(serializer.data)