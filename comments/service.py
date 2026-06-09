from .models import Comments
from rest_framework.permissions import IsAuthenticated
from Users.permissions import employee_verification
from BLOG.service import get_blog__organization
from follow.service import get_organization_following_list,get_user_following_list
from rest_framework.exceptions import ValidationError
from django.db import transaction
from streak.service import get_streak,streak_logic
from notifications.service import send_comment,send_comment_delete
from rest_framework.response import Response
from .permissions import Comments_update_permission,comment_access_permission
def get_all_comments():
    return Comments.objects.all()


def get_all_comment_of_blog(id):
    return Comments.objects.select_related('owner').filter(blog_id=id)

def get_comment_blog__organization_user():
    return Comments.objects.select_related('blog__organization').select_related('owner').all()

def get_comment_user():
    return Comments.objects.select_related('owner').all()

def comment_permissions(self):
    permission_map = {

    'list': [IsAuthenticated,employee_verification],

    'retrieve': [IsAuthenticated,employee_verification,comment_access_permission],

    'create': [IsAuthenticated,employee_verification,],

    'update': [IsAuthenticated,employee_verification,comment_access_permission,Comments_update_permission],

    'partial_update': [IsAuthenticated,employee_verification,comment_access_permission,Comments_update_permission],

    'destroy': [IsAuthenticated,employee_verification,comment_access_permission,Comments_update_permission],
    }
    permissions=permission_map.get(self.action,[IsAuthenticated])
    return [permission() for permission in permissions]


def comment_create_permission(self,request,*args,**kwargs):
    id=kwargs.get('pk')
    self.obj=get_blog__organization(id)
    if self.obj.organization.type=='Pvt':
        following=get_user_following_list(request.user)
        organizationfollowing=get_organization_following_list(request.user)
        if request.user.organization==self.obj.organization or self.obj.organization.Name in following or self.obj.organization.Name in organizationfollowing :
            return super().create(request, *args, **kwargs)
        else :
            raise ValidationError(f'you must belong to or follow the organization {self.obj.organization.Name} to comment on it')
        
    elif self.obj.organization.type=='Pub':
        return super().create(request, *args, **kwargs)



def comment_get_list_permission(self,request,*args,**kwargs):
    id=kwargs.get('pk')
    self.obj=get_blog__organization(id)
    if self.obj.organization.type=='Pvt':
        following=get_user_following_list(request.user)
        organizationfollowing=get_organization_following_list(request.user)
        if request.user.organization==self.obj.organization or self.obj.organization.Name in following or self.obj.organization.Name in organizationfollowing :
            return super().list(request, *args, **kwargs)
        else :
            raise ValidationError(f'you must belong to or follow the organization {self.obj.organization.Name} to get the comments of this blog on it')
        
    elif self.obj.organization.type=='Pub':
        return super().list(request, *args, **kwargs)


@transaction.atomic
def comment_create(self,serializer):
    try:
        comment=serializer.save(owner_id=self.request.user.id,blog_id=self.obj.id)
        streak_logic(self.request.user.id)
        send_comment(self.obj.organization.Name,comment)
        return Response(serializer.data)
    except Exception as e:
        raise ValidationError({
            'error':'comment could not be created',
            'details':str(e)
        })
    
@transaction.atomic
def comment_update(self,serializer):
    
    try:
        comment=serializer.save()
        send_comment(serializer.instance.blog.organization.Name,comment)
        return Response(serializer.data)
    except Exception as e:
        raise ValidationError({
            'error':'comment could not be updated',
            'details':str(e)
        })
    
@transaction.atomic
def comment_delete(self,instance):
    
    try:
        id=instance.id
        name=instance.blog.organization.Name
        instance.delete()

        send_comment_delete(id,name)
        return Response('deleted successfully')
    except Exception as e:
        raise ValidationError({
            'error':'comment could not be delete',
            'details':str(e)
        })