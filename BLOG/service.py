from .models import Blog,Tag
from rest_framework.exceptions import ValidationError
from django.db import IntegrityError,transaction
from django.db.models import Q,F
from rest_framework.permissions import IsAuthenticated
from Users.permissions import employee_verification
from organization.service import get_organization
from streak.service import streak_logic
from channels.layers import get_channel_layer
from notifications.service import send_blog
from rest_framework.response import Response
from .permissions import Blog_access_permission,blog_update_destroy_permission
from organization.permissions import belong_to_same_organization
from Read.service import get_or_create_blogread
from tag.service import get_create_tag
from follow.service import get_organization_following_list,get_user_following_list
def get_blog__organization(id):
    try:
        blog= Blog.objects.select_related('organization').get(id=id)
        return blog
    except IntegrityError as e:
        raise ValidationError({
            'error':'blog could not be found',
            'detail':str(e)
        })
    

def filter_blog__organization__user(id):
    Blog.objects.select_related('organization','created_by').filter(organization_id=id)


def get_blog__organization__user_all():
    Blog.objects.select_related('organization','created_by').all()


def search_blogs(self,search,organizationfollowing,following):
    return Blog.objects.select_related('organization').prefetch_related('tag').filter(Q(title__icontains=search)|
                                                                  Q(organization__Name__icontains=search)|
                                                                  Q(tag__name__icontains=search)).filter(
                                                                      Q(organization_id=self.request.user.organization_id)|
                                                                      Q(organization__Name__in=organizationfollowing)|
                                                                      Q(organization_id__in=following)
                                                                      ).distinct()

def blog_permissions(self):
    permission_map = {

    'list': [IsAuthenticated,employee_verification],

    'retrieve': [IsAuthenticated,employee_verification,Blog_access_permission],

    'create': [IsAuthenticated,employee_verification,belong_to_same_organization],

    'update': [IsAuthenticated,employee_verification,blog_update_destroy_permission],

    'partial_update': [IsAuthenticated,employee_verification,blog_update_destroy_permission],

    'destroy': [IsAuthenticated,employee_verification,blog_update_destroy_permission],
    }
    permissions=permission_map.get(self.action,[IsAuthenticated])
    return [permission() for permission in permissions]


@transaction.atomic
def blog_create(self,serializer):

    try:
        tags=serializer.validated_data.pop('tag')
        blog=serializer.save(created_by=self.request.user,organization=self.request.user.organization)
        for tag in tags:
            t,_=get_create_tag(tag)
            blog.tag.add(t)
        streak_logic(self.request.user.id)
        transaction.on_commit(
            lambda:send_blog(self,blog)
        )
        return Response(serializer.data)
    except Exception as e:
        raise ValidationError({
            'error':'blog could not be created',
            'details':str(e)
        })

@transaction.atomic
def blog_read(self,request,*args,**kwargs):
    try:
        serializer=self.get_serializer(self.blog)
        
        get_or_create_blogread(self.blog,request.user)
        streak_logic(request.user.id)
        return Response(serializer.data)
    except Exception as e:
        raise ValidationError({
            'error':'could not fetch the blog',
            'details':str(e)
        })
@transaction.atomic 
def blog_update(self,serializer):
    try:
        blog=serializer.instance

        tags=serializer.validated_data.pop('tag')
        a=[]
        for tag in tags:
            t,_=get_create_tag(tag)
            a.append(t)
        if a is not None:
            blog.tag.set(a)
    except Exception as e:
        raise ValidationError({
            'error':'blog is not updated',
            'details':str(e)
        })
    

    return super().perform_update(serializer)


def list_permission(self,request,*args,**kwargs):
    obj=get_organization(kwargs.get('pk'))
    if obj.organization.type=='Pvt':
        following=get_user_following_list(request.user.id)
        organizationfollowing=get_organization_following_list(request.user.organization_id)
        if request.user.organization_id==obj.id or obj.Name in following or obj.Name in organizationfollowing :
            return super().list(request, *args, **kwargs)
        else :
            raise ValidationError(f'you must belong to or follow the organization {obj.organization.Name} to read blogs posted by it ')
        
    elif self.obj.organization.type=='Pub':
        return super().list(request, *args, **kwargs)
