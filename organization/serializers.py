from rest_framework import serializers
from .models import Organization
from Users.models import employees
import re
from follow.service import user_following_list_exists,organization_following_list_exists,count_organization_follower


class UserSerialization(serializers.ModelSerializer):
    class Meta:
        model=employees
        fields=['user_name','first_name','bio_pitcure']

class OrganizationSerializers(serializers.ModelSerializer):
    founder=UserSerialization(read_only=True)
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




class OrganizationRetrieveSerializers(serializers.ModelSerializer):
    founder=UserSerialization()
    follow=serializers.SerializerMethodField()
    follow_count=serializers.SerializerMethodField()

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
    
    def get_follow_count(self,obj):
        return count_organization_follower(obj.id)
    
    def get_follow(self,obj):
        user=self.context.get('request').user
        if obj.founder_id==user.id:
            return False
        return user_following_list_exists(user.id,obj.id) or organization_following_list_exists(user.organization_id,obj.id)
    class Meta:
        model=Organization
        fields=['id','Name','bio_pitcure','type','body','founder','follow','follow_count']
        read_only_fields=['founder','id']