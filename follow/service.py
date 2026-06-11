from Users.models import employees
from .models import OrganizationFollower,OrganizationFollowing,UserFollowing

from django.db import transaction,IntegrityError
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from notifications.service import create_follow_notification,send_notification_founder,send_notification_founder_follow,send_notification_founder_unfollow,send_notification_user_follow,send_notification_user_unfollow


def count_organization_follower(id):
    return UserFollowing.objects.filter(following_id=id).count()

def get_organization_following_list(id):
    return OrganizationFollowing.objects.select_related('following').filter(organization_id=id).values_list('following__Name',flat=True)

def get_user_following_list(id):
    return UserFollowing.objects.select_related('following').filter(user_id=id).values_list('following__Name',flat=True)

def organization_following_list_exists(organization_id,following_id):
    return OrganizationFollowing.objects.select_related('following').filter(organization_id=organization_id,following_id=following_id).exists()

def user_following_list_exists(user_id,organization_id):
    return UserFollowing.objects.select_related('following').filter(user_id=user_id,following_id=organization_id).exists()

def create_follow(obj,current_user):
    try:
        follow=UserFollowing.objects.create(user_id=current_user.id,following_id=obj.id)
        return follow
    except IntegrityError as e:
        raise ValidationError({
            'error':'user already follows the organizaion'
        })

def organization_follow(current_organization,obj):
    
    try:
        follow=OrganizationFollowing.objects.create(organization_id=current_organization.id,following_id=obj.id)
        return follow
    except IntegrityError as e:
        raise ValidationError({
            'error':f'your organization already follows the organizaion {obj.Name}'
        })
    

def organization_follower(obj,current_organization):
    
    try:
        follower=OrganizationFollower.objects.create(organization_id=obj.id,follower_id=current_organization.id)
        return follower
    except IntegrityError as e:
        raise ValidationError({
            'error':f'organization {obj.Name} already has a follower {current_organization.Name}'
        })

def organization_follower_delete(obj,current_organization):
    
    try:
        OrganizationFollower.objects.get(follower_id=current_organization.id,organization_id=obj.id).delete()
    except IntegrityError as e:
        raise ValidationError({
            
            'error':f'organization {obj.Name} already does not have a follower {current_organization.Name}'
        })

def organization_following_delete(obj,current_organization):
    
    try:
        OrganizationFollowing.objects.get(organization_id=current_organization.id,following_id=obj.id).delete()
    except IntegrityError as e:
        raise ValidationError({
            'error':f'your organization does not already follows the organizaion {obj.Name}'
        })

def unfollow_user(current_user,obj):
    
    try:
        UserFollowing.objects.get(user_id=current_user.id, following_id=obj.id).delete()
    except IntegrityError as e:
        raise ValidationError({
            'error':'user already does not follow the organization'
        })



@transaction.atomic
def follow(request,obj):
    from Users.service import current_user_logined
    try:
        
        current_user=current_user_logined(request.user.id)
        if current_user.role==employees.roles.EMPLOYEE:
            create_follow(obj,current_user)
            content=f'{current_user.user_name} started following your organization'
            create_follow_notification(content,obj,current_user)


            transaction.on_commit(
                lambda:send_notification_user_follow(current_user,obj)
            )
            


            
            transaction.on_commit(
                lambda:send_notification_founder(obj,content)
            )
            
            
        else:
            create_follow(obj,current_user)
            current_organization=current_user.organization
            content=f'{current_user.user_name} founder of {current_organization.Name} started following your organization'
            organization_follow(current_organization,obj)
            organization_follower(obj,current_organization)
            create_follow_notification(content,obj,current_user)



            transaction.on_commit(
                lambda:send_notification_founder_follow(current_organization,obj)
            )
            



            transaction.on_commit(
                lambda:send_notification_founder(obj,content)
            )
            
        return Response('followed successfully')
    except Exception as e:
        raise ValidationError({
            'error':'could not follow the organization',
            'detail':str(e)
        })
    



@transaction.atomic
def unfollow(request,obj):
    from Users.service import current_user_logined
    try:
        
        current_user=current_user_logined(request.user.id)
        if current_user.role==employees.roles.EMPLOYEE:
            unfollow_user(current_user,obj)
            content=f'{current_user.user_name} unfollowed your organization'
            create_follow_notification(content,obj,current_user)

            transaction.on_commit(
                lambda:send_notification_user_unfollow(current_user,obj)
            )
            


            
            transaction.on_commit(
                lambda:send_notification_founder(obj,content)
            )
            
            
        else:
            unfollow_user(current_user,obj)
            
            current_organization=current_user.organization
            content=f'{current_user.user_name} founder of {current_organization.Name} unfollowed your organization'
            organization_following_delete(obj,current_organization)
            organization_follower_delete(obj,current_organization)
            create_follow_notification(content,obj,current_user)



            transaction.on_commit(
                lambda:send_notification_founder_unfollow(current_organization,obj)
            )
            


            
            transaction.on_commit(
                lambda:send_notification_founder(obj,content)
            )
            
        return Response('unfollowed successfully')
    except Exception as e:
        raise ValidationError({
            'error':'could not unfollow the organization',
            'detail':str(e)
        })