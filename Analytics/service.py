from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from BLOG.service import total_post_user,total_post_organization,get_blog__organization__user
from comments.service import all_comment_user
from like.service import all_likes_user,top_post_organization
from Read.service import all_read_user,all_read_organization
from streak.service import get_streak,top_employee_on_streak
from follow.service import count_organization_follower,user_following_list_exists,organization_following_list_exists
from Users.service import total_employees_organization,get_employee__organization
from django.db import transaction
from organization.service import get_organization
from rest_framework.exceptions import ValidationError
from BLOG.serializers import BlogSerializer

@transaction.atomic
def employee_analytics(self,request,*args,**kwargs):
    try:
        id=kwargs.get('pk')
        obj=get_employee__organization(id)
        following_exists=user_following_list_exists(request.user.id,obj.organization_id)
        organizationfollowing_exists=organization_following_list_exists(request.user.organization_id, obj.organization_id)
        if request.user.organization==obj.organization or following_exists or organizationfollowing_exists or obj.organization.type=='Pub':
            total_post=total_post_user(id)
            total_comments=all_comment_user(id)
            total_likes=all_likes_user(id)
            total_reads=all_read_user(id)
            streak=get_streak(id)
            count=streak.count
            max_streak=streak.max_streak
            return Response({'total_post':total_post,'total_comments':total_comments,'total_likes':total_likes,'total_reads':total_reads,'count':count,'max_streak':max_streak})
        else :
            raise ValidationError(f'you must belong to or follow the organization {obj.organization.Name} to get the analytics of this employee. ')

        
      
        
     
    except Exception as e:
        raise ValidationError({
            'error':'could not fetch the employee analytics',
            'details':str(e)
        })


@transaction.atomic
def organization_analytics(self,request,*args,**kwargs):

    try:
        id=kwargs.get('pk')
        obj=get_organization(id)

        following_exists=user_following_list_exists(request.user.id,obj.id)
        organizationfollowing_exists=organization_following_list_exists(request.user.organization_id, obj.id)
        if request.user.organization_id==obj.id or following_exists or organizationfollowing_exists or obj.type=='Pub':
            total_employee=total_employees_organization(id)
            total_blog=total_post_organization(id)
            total_read=all_read_organization(id)
            total_followers=count_organization_follower(id)
            top_employee=top_employee_on_streak(id)
            top_post_id=top_post_organization(id)
            if top_post_id:
                top_post_id=top_post_id['blog']
                top_post=get_blog__organization__user(top_post_id)
                serializer=BlogSerializer(top_post,context={'request':request})
                print(top_post)
                return Response({'total_employee':total_employee,'total_blog':total_blog,'total_read':total_read,'total_followers':total_followers,'top_employee':top_employee,'top_post':serializer.data})
            return Response({'total_employee':total_employee,'total_blog':total_blog,'total_read':total_read,'total_followers':total_followers,'top_employee':top_employee,'top_post':'no likes'})
        else :
            raise ValidationError(f'you must belong to or follow the organization {obj.Name} to get the analytics of this employee. ')

        
    except Exception as e:
        raise ValidationError({
            'error':'could not fetch the organization analytics',
            'details':str(e)
        })
