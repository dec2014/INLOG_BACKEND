from .models import Blog,Tag
from rest_framework.exceptions import ValidationError
from django.db import IntegrityError,transaction
from django.db.models.aggregates import Count
from django.db.models import Q,F
from rest_framework.permissions import IsAuthenticated
from Users.permissions import employee_verification
from organization.service import get_organization
from streak.service import streak_logic
from notifications.service import send_blog
from rest_framework.response import Response
from .permissions import Blog_access_permission,blog_update_destroy_permission
from organization.permissions import belong_to_same_organization
from Read.service import get_or_create_blogread
from tag.service import get_create_tag
from follow.service import user_following_list_exists,organization_following_list_exists


def total_post_organization(id):
    return Blog.objects.filter(organization_id=id).count()

def total_post_user(id):
    return Blog.objects.filter(created_by_id=id).count()

def blog_pinned_by_user(user):
    return Blog.objects.select_related('organization','created_by').prefetch_related('tag').filter(pinnedblog__pin_by_id=user.id,pinnedblog__pin=True)

def blog_pinned_by_organization(user):
    return Blog.objects.select_related('organization','created_by').prefetch_related('tag').filter(pinnedblog__pin_by__organization_id=user.organization_id ,pinnedblog__founder_pin=True)

def like_blog_by_users(user):
    return Blog.objects.select_related('organization','created_by').prefetch_related('tag').filter(blog_like__like_user_id=user.id ,blog_like__like=True)

def get_blog__organization(id):
    try:
        blog= Blog.objects.select_related('organization').prefetch_related('tag').get(id=id)
        return blog
    except IntegrityError as e:
        raise ValidationError({
            'error':'blog could not be found',
            'detail':str(e)
        })
    

def get_blog__organization__user(id):
    try:
        blog= Blog.objects.select_related('organization','creted_by').prefetch_related('tag').get(id=id)
        return blog
    except IntegrityError as e:
        raise ValidationError({
            'error':'blog could not be found',
            'detail':str(e)
        })
    


def filter_blog__organization__user(id):
    blogs= Blog.objects.select_related('organization','created_by').prefetch_related('tag').filter(organization_id=id).annotate(likes_count=Count('blog_like',
                                                                                                                                           filter=Q(blog_like__like=True)),
                                                                                                                                           comment_count=Count('comments')
    )
    return blogs

def get_blog__organization_all():
    return Blog.objects.select_related('organization').prefetch_related('tag').all()

def get_blog__organization__user_all():

    return Blog.objects.select_related('organization','created_by').prefetch_related('tag').all()
    


def search_blogs(self,search,organizationfollowing,following):
    return Blog.objects.select_related('organization','created_by').prefetch_related('tag').filter(Q(title__icontains=search)|
                                                                  Q(organization__Name__icontains=search)|
                                                                  Q(tag__name__icontains=search)).filter(
                                                                      Q(organization_id=self.request.user.organization_id)|
                                                                      Q(organization__Name__in=organizationfollowing)|
                                                                      Q(organization__Name__in=following)
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

        print(self.request.user.id)
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
        return Response(
            serializer.data
                         )
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
        if a:
            blog.tag.set(a)
        
    except Exception as e:
        raise ValidationError({
            'error':'blog is not updated',
            'details':str(e)
        })
    

    


def list_permission(self,request,*args,**kwargs):
    try:
        obj=get_organization(kwargs.get('pk'))
        if obj.type=='Pvt':
            following_exists=user_following_list_exists(request.user.id,obj.id)
            organizationfollowing_exists=organization_following_list_exists(request.user.organization_id, obj.id)
            if request.user.organization_id==obj.id or following_exists or organizationfollowing_exists :
                return True
            else :
                raise ValidationError(f'you must belong to or follow the organization {obj.Name} to read blogs posted by it ')
            
        elif obj.type=='Pub':
            return True
    except Exception as e:
        raise ValidationError({
            'error':'blogs cannot be fetched',
            'details':str(e)
        })
