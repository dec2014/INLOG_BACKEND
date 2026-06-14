from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from .models import FollowNotification,BlogNotification
from asgiref.sync import sync_to_async
from django.utils.text import Truncator
import logging
logger = logging.getLogger(__name__)



@sync_to_async
def asyncBlogCreation(self,event):
    BlogNotification.objects.create(blog_id=event['id'],sent_to_id=self.user.id)

    return True




def user_room(id):
    return f'user_{id}'

def organization_room(name):
    return f'organization_{name}'

def notification_room(name):
    return f'notification_{name}'


def create_follow_notification(content,obj,current_user):
    FollowNotification.objects.create(content=content,owner_id=obj.founder_id,user_id=current_user.id)

def send_notification_user_follow(current_user,obj):
    room=user_room(current_user.id)
    channel_layer=get_channel_layer()
    try:
        async_to_sync(channel_layer.group_send)(room,{
                    'type':'follower_employee',
                    'name':obj.Name,

                })
    except Exception:
        logger.exception('failed to send the notification.')
    

def send_comment(name,comment):
    channel_layer=get_channel_layer()
    room=notification_room(name)
    try:
        async_to_sync(channel_layer.group_send)(room,{
            'type':'comments',
            'id':comment.id,
            'content':comment.text,
            'owner_id':comment.owner_id,
            'blog_id':comment.blog_id
            
        })
    except Exception:
        logger.exception('failed to send the comment.')

def send_comment_delete(id,name):
    channel_layer=get_channel_layer()
    room=notification_room(name)
    try:
        async_to_sync(channel_layer.group_send)(room,{
            'type':'comments_delete',
            'id':id,

            
        })
    except Exception:
        logger.exception('failed to send the notification.')


def send_notification_founder(obj,content):
    room2=user_room(obj.founder_id)
    channel_layer=get_channel_layer()
    try:
        async_to_sync(channel_layer.group_send)(room2,{
            'type':'follower_employee_to_founder',
            'content':content,


        })
    except Exception:
        logger.exception('failed to send the notification.')


def send_notification_founder_follow(current_organization,obj):
    channel_layer=get_channel_layer()
    room=organization_room(current_organization.Name)
    try:
        async_to_sync(channel_layer.group_send)(room,{
            'type':'follower_founder',
            'name':obj.Name,

        })
    except Exception:
        logger.exception('failed to send the notification.')


def send_notification_user_unfollow(current_user,obj):
    room=user_room(current_user.id)
    channel_layer=get_channel_layer()
    try:
        async_to_sync(channel_layer.group_send)(room,{
                    'type':'unfollower_employee',
                    'name':obj.Name,

                })
    except Exception:
        logger.exception('failed to send the notification.')

def send_notification_founder_unfollow(current_organization,obj):
    channel_layer=get_channel_layer()
    room=organization_room(current_organization.Name)
    try:
        async_to_sync(channel_layer.group_send)(room,{
            'type':'unfollower_founder',
            'name':obj.Name,

        })
    except Exception:
        logger.exception('failed to send the notification.')

def send_blog(self,blog):
    channel_layer=get_channel_layer()
    room=f'notification_{self.obj.Name}'
    try:
        async_to_sync(channel_layer.group_send)(room,{
            'type':'blog_notification',
            'id':blog.id,
            'content':Truncator(blog.content).chars(100),
            'created_by':blog.created_by.user_name,
            'created_at':str(blog.created_at),
            'user_name':self.request.user.user_name
        })
    except Exception:
        logger.exception('failed to send the blog.')