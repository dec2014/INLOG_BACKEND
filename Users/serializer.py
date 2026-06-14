from rest_framework import serializers
from .models import employees
from django.utils import timezone
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta():
        model=employees
        fields=['id','user_name','password','first_name','last_name','email','bio_pitcure']
        read_only_fields=['id',]
    def create(self, validated_data):
        return employees.objects.create_user(**validated_data)
    

class UserCreateEmployeeSerializer(serializers.ModelSerializer):
    role=serializers.ChoiceField(choices=[
        ('E','Employee')
    ])
    class Meta():
        model=employees
        fields=['id','user_name','password','first_name','last_name','email','bio_pitcure','role']
        read_only_fields=['organization','id']
    def create(self, validated_data):
        return employees.objects.create_user(**validated_data)


class EmployeeSerializer(serializers.ModelSerializer):
    
    class Meta():
        model=employees
        fields=['id','user_name','password','first_name','last_name','email','bio_pitcure','role']
        read_only_fields=['organization','id']
    



class changePasswordSerializer(serializers.ModelSerializer):
    class Meta():
        model=employees
        fields=['password',]

    def update(self, instance, validated_data):
        password=validated_data.get('password',instance.password)
        instance.set_password(password)
        instance.is_password_temp=False
        instance.save()
        return instance
        


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data= super().validate(attrs)
        self.user.last_login_act=timezone.now()
        self.user.save(update_fields=['last_login_act'])
        return data
