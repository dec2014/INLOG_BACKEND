from rest_framework import serializers
from .models import Blog
from organization.models import Organization
from Users.models import NewUser



class UserSerialization(serializers.ModelSerializer):
    class Meta:
        model=NewUser
        fields=['user_name','first_name','bio_pitcure']

class OrganizatoinSerializers(serializers.ModelSerializer):
    class Meta:
        model=Organization
        fields=['id','Name','bio_pitcure','type','founder']
        read_only_fields=['founder','id']



class BlogSerializer(serializers.ModelSerializer):
    tag = serializers.ListField(
        child=serializers.CharField(),
        write_only=True
    )
    organization=OrganizatoinSerializers()
    created_by=UserSerialization()
    class Meta:
        model=Blog
        fields=['id','content','pictures','title','tag','organization','created_by','created_at']
        read_only_fields=['created_by','created_at','organization','id']

    def to_representation(self, instance):

        data = super().to_representation(instance)
        data['tag'] = [
            tag.name for tag in instance.tag.all()
        ]

        return data
    






