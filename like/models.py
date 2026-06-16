from django.db import models
from BLOG.models import Blog
# Create your models here.


class BlogLike(models.Model):
    blog=models.ForeignKey(Blog,on_delete=models.CASCADE,related_name='blog_like')
    like=models.BooleanField(default=True)
    like_user=models.ForeignKey('Users.employees',on_delete=models.CASCADE)
    class Meta:
        unique_together=['blog','like_user']