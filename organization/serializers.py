from rest_framework import serializers
from .models import Organization
from Users.models import NewUser
import re


class UserSerialization(serializers.ModelSerializer):
    class Meta:
        model=NewUser
        fields=['user_name','first_name','bio_pitcure']

class OrganizationSerializers(serializers.ModelSerializer):
    founder=UserSerialization()
    def validate_Name(self, value):

        value = value.strip()


        if len(value) < 3:
            raise serializers.ValidationError(
                "Name must be at least 3 characters."
            )


        if not value[0].isalnum():
            raise serializers.ValidationError(
                "Name cannot start with a special character."
            )


        if not re.match(r'^[A-Za-z0-9 ]+$', value):
            raise serializers.ValidationError(
                "Only letters, numbers and spaces are allowed."
            )

        return value
    class Meta:
        model=Organization
        fields=['id','Name','bio_pitcure','type','body','founder']
        read_only_fields=['founder','id']