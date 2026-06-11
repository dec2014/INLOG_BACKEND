
from rest_framework import generics
from .serializer import UserCreateSerializer,UserCreateEmployeeSerializer,changePasswordSerializer,MyTokenObtainPairSerializer,EmployeeSerializer
from .service import verification_user,employee_create,change_password,force_password_change_by_founder,password_change_by_founder_of_employee,get_all_employees,get_all_employee__organization,list_employee
from rest_framework import permissions
from rest_framework_simplejwt.authentication import JWTAuthentication
from .permissions import is_temp_pass,Founder_Set_Up,employeeDeletePermission,employee_view_permission,employee_verification
from rest_framework_simplejwt.views import TokenObtainPairView
from streak.service import create_streak
from django.db import transaction,IntegrityError
from rest_framework.exceptions import ValidationError


# Create your views here.
class CreateUser(generics.CreateAPIView):
    serializer_class=UserCreateSerializer

    @transaction.atomic
    def perform_create(self, serializer):
        try:

            serializer.save()
            create_streak(serializer.data['id'])
        except IntegrityError:
            raise ValidationError('could not create the user')
        
    

class employee_retrieve(generics.RetrieveAPIView):
    queryset=get_all_employee__organization()
    serializer_class=EmployeeSerializer
    lookup_field='pk'
    authentication_classes=[JWTAuthentication]
    permission_classes=[permissions.IsAuthenticated,employee_verification,employee_view_permission]
    def retrieve(self, request, *args, **kwargs):
        
        try:
            return super().retrieve(request, *args, **kwargs)
        except Exception as e:
            raise ValidationError({
                'error':'could not get the employee',
                'details':str(e)
            })


class employee_list(generics.ListAPIView):
    queryset=get_all_employee__organization()
    serializer_class=EmployeeSerializer
    authentication_classes=[JWTAuthentication]
    permission_classes=[permissions.IsAuthenticated,employee_verification]
    def list(self, request, *args, **kwargs):
        return list_employee(self, request, *args, **kwargs)


class Verification(generics.RetrieveAPIView):
    serializer_class=UserCreateSerializer
    def retrieve(self, request, *args, **kwargs):
        return verification_user(self, request, *args, **kwargs)
        


class EmployeeTemperary(generics.CreateAPIView):
    serializer_class=UserCreateEmployeeSerializer
    authentication_classes=[JWTAuthentication]
    permission_classes=[permissions.IsAuthenticated,Founder_Set_Up]
    def create(self, request, *args, **kwargs):
        return employee_create(self, request, *args, **kwargs)
    


class changePassword(generics.UpdateAPIView):
    serializer_class=changePasswordSerializer
    authentication_classes=[JWTAuthentication]
    permission_classes=[permissions.IsAuthenticated,is_temp_pass]
    def update(self, request, *args, **kwargs):
        return change_password(self, request, *args, **kwargs)
    

class force_password_reset(generics.UpdateAPIView):
    authentication_classes=[JWTAuthentication]
    permission_classes=[permissions.IsAuthenticated,Founder_Set_Up]
    def update(self, request, *args, **kwargs):
        return force_password_change_by_founder(self, request, *args, **kwargs)



class changePasswordByFounder(generics.UpdateAPIView):

    serializer_class=changePasswordSerializer
    authentication_classes=[JWTAuthentication]
    permission_classes=[permissions.IsAuthenticated,Founder_Set_Up]
    def update(self, request, *args, **kwargs):
        return password_change_by_founder_of_employee(self, request, *args, **kwargs)
        


class mytoken(TokenObtainPairView):
    serializer_class=MyTokenObtainPairSerializer
        
        
class employeeDelete(generics.DestroyAPIView):
    queryset=get_all_employees()
    lookup_field='pk'
    authentication_classes=[JWTAuthentication]
    permission_classes=[permissions.IsAuthenticated,employeeDeletePermission]

