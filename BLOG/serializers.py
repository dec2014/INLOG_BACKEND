from rest_framework import serializers
from .models import Blog
from organization.models import Organization
from Users.models import employees
from like.service import like_by_user,blog_likes
from Pin.service import pin_by_user
from comments.service import comments_blog


class UserSerialization(serializers.ModelSerializer):
    class Meta:
        model=employees
        fields=['user_name','first_name','bio_pitcure']

class OrganizatoinSerializers(serializers.ModelSerializer):
    class Meta:
        model=Organization
        fields=['id','Name','bio_pitcure','type','founder']
        read_only_fields=['founder','id']



class BlogCreateSerializer(serializers.ModelSerializer):
    tag = serializers.ListField(
        child=serializers.CharField(),
        write_only=True
    )

    organization=OrganizatoinSerializers(read_only=True)
    created_by=UserSerialization(read_only=True)
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
    

class BlogSerializer(serializers.ModelSerializer):
    tag = serializers.ListField(
        child=serializers.CharField(),
        write_only=True
    )
    liked=serializers.SerializerMethodField()
    pinned=serializers.SerializerMethodField()
    organization=OrganizatoinSerializers(read_only=True)
    created_by=UserSerialization(read_only=True)
    likes_count=serializers.SerializerMethodField()
    comment_count=serializers.SerializerMethodField()
    class Meta:
        model=Blog
        fields=['id','content','pictures','title','tag','organization','created_by','created_at','likes_count','comment_count','liked','pinned']
        read_only_fields=['created_by','created_at','organization','id']


    def get_liked(self,obj):
        user=self.context.get('request').user.id
        return like_by_user(obj.id,user)
    
    def get_pinned(self,obj):
        user=self.context.get('request').user.id
        return pin_by_user(user,obj.id)
    
    def get_likes_count(self,obj):
        return blog_likes(obj.id)
    
    def get_comment_count(self,obj):
        return comments_blog(obj.id)
    

    def to_representation(self, instance):

        data = super().to_representation(instance)
        data['tag'] = [
            tag.name for tag in instance.tag.all()
        ]

        return data
    

class BlogListSerializer(serializers.ModelSerializer):
    tag = serializers.ListField(
        child=serializers.CharField(),
        write_only=True
    )
    
    likes_count=serializers.IntegerField(read_only=True)
    comment_count=serializers.IntegerField(read_only=True)
    organization=OrganizatoinSerializers(read_only=True)
    created_by=UserSerialization(read_only=True)
    class Meta:
        model=Blog
        fields=['id','content','pictures','title','tag','organization','created_by','created_at','likes_count','comment_count']
        read_only_fields=['created_by','created_at','organization','id']
    

    def to_representation(self, instance):

        data = super().to_representation(instance)
        data['tag'] = [
            tag.name for tag in instance.tag.all()
        ]

        return data
    

