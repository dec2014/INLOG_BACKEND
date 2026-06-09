from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from .models import FollowNotification

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
    async_to_sync(channel_layer.group_send)(room,{
                'type':'follower_employee',
                'name':obj.Name,

            })
    

def send_comment(name,comment):
    channel_layer=get_channel_layer()
    room=notification_room(name)
    async_to_sync(channel_layer.group_send)(room,{
        'type':'comments',
        'id':comment.id,
        'content':comment.text,
        'owner_id':comment.owner_id,
        'blog_id':comment.blog_id
        
    })

def send_comment_delete(id,name):
    channel_layer=get_channel_layer()
    room=notification_room(name)
    async_to_sync(channel_layer.group_send)(room,{
        'type':'comments_delete',
        'id':id,

        
    })


def send_notification_founder(obj,content):
    room2=user_room(obj.id)
    channel_layer=get_channel_layer()
    async_to_sync(channel_layer.group_send)(room2,{
        'type':'follower_employee_to_founder',
        'content':content,


    })


def send_notification_founder_follow(current_organization,obj):
    channel_layer=get_channel_layer()
    room=organization_room(current_organization.Name)
    async_to_sync(channel_layer.group_send)(room,{
        'type':'follower_founder',
        'name':obj.Name,

    })


def send_notification_user_unfollow(current_user,obj):
    room=user_room(current_user.id)
    channel_layer=get_channel_layer()
    async_to_sync(channel_layer.group_send)(room,{
                'type':'unfollower_employee',
                'name':obj.Name,

            })

def send_notification_founder_unfollow(current_organization,obj):
    channel_layer=get_channel_layer()
    room=organization_room(current_organization.Name)
    async_to_sync(channel_layer.group_send)(room,{
        'type':'unfollower_founder',
        'name':obj.Name,

    })