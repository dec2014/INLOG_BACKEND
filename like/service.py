from rest_framework.response import Response
from organization.models import Organization
from follow.service import user_following_list_exists,organization_following_list_exists
from django.db import transaction
from .models import BlogLike
from streak.service import streak_logic
from rest_framework.exceptions import ValidationError

def blog_like_create_update(blog,user):
    obj_like,created=BlogLike.objects.update_or_create(
        blog=blog,
        like_user=user,
    )
    if not created:
        obj_like.like= not obj_like.like
        obj_like.save()
    return obj_like,created

@transaction.atomic
def like_unlike_blog(self,request,*args,**kwargs):
    
    
    try:
        obj_like,created=blog_like_create_update(self.blog,request.user)
        streak_logic(request.user.id)

        return Response({'like':obj_like.like,'created':created})
    except Exception as e:
        ValidationError({
            'error':'could not like the blog',
            'details':str(e)
        })







