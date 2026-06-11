from rest_framework.response import Response
from organization.models import Organization
from follow.service import user_following_list_exists,organization_following_list_exists
from django.db import transaction
from .models import BlogLike
from streak.service import streak_logic
from rest_framework.exceptions import ValidationError
from django.db.models.aggregates import Count

def top_post_organization(id):
    return BlogLike.objects.select_related('blog').filter(blog__organization_id=id,like=True).values('blog').annotate(total=Count('blog')).order_by('-total').first()

def all_likes_user(id):
    return BlogLike.objects.filter(like_user_id=id,like=True).count()

def like_by_user(blog,user):
    return BlogLike.objects.filter(blog_id=blog,like_user_id=user,like=True).exists()

def blog_likes(blog):
    return BlogLike.objects.filter(blog_id=blog,like=True).count()

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







