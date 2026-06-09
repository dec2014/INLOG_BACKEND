from rest_framework import serializers
from .models import Comments
from Users.models import employees


class UserSerialization(serializers.ModelSerializer):
    class Meta:
        model=employees
        fields=['user_name','first_name','bio_pitcure']



class commentsSerialization(serializers.ModelSerializer):
    owner=UserSerialization()
    class Meta:
        model=Comments
        fields=['id','text','owner',"blog"]
        read_only_fields=['owner','id','blog']
