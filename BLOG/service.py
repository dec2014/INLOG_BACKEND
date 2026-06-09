from .models import Blog,Tag
from rest_framework.exceptions import ValidationError
from django.db import IntegrityError,transaction
from rest_framework.permissions import IsAuthenticated
from Users.permissions import employee_verification
from organization.service import get_organization
from streak.service import streak_logic

def get_blog__organization(id):
    try:
        blog= Blog.objects.select_related('organization').get(id=id)
        return blog
    except IntegrityError as e:
        raise ValidationError({
            'error':'blog could not be found',
            'detail':str(e)
        })
    
def get_create_tag(tag):
    Tag.objects.get_or_create(name=tag)


def blog_permissions(self):
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


def blog_create_permission(self,request,*args,**kwargs):
    organization=get_organization(kwargs.get('pk'))
    if organization.id!=request.user.organization_id:
        raise ValidationError('you cannot create the blog for this organization as you do not belong to it.')
    return super().create(request, *args, **kwargs)

@transaction.atomic
def blog_create(self,serializer):

    tags=serializer.validated_data.pop('tag')
    blog=serializer.save(created_by=self.request.user,organization_id=self.request.user.organization_id)
    for tag in tags:
        t,_=get_create_tag(tag)
        blog.tag.add(t)
    streak_logic(self.request.user.id)
    
    channel_layer=get_channel_layer()
    room=f'notification_{organization.Name}'
    async_to_sync(channel_layer.group_send)(room,{
        'type':'blog_notification',
        'id':blog.id,
        'content':blog.content,
        'created_by':blog.created_by.user_name,
        'created_at':str(blog.created_at),
        'user_name':self.request.user.user_name
    })
    return Response(serializer.data)