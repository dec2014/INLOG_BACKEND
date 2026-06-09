from django.db import models
from BLOG.models import Blog
# Create your models here.
class FollowNotification(models.Model):
    content=models.TextField()
    read=models.BooleanField(default=False,db_index=True)
    owner=models.ForeignKey('Users.employees',on_delete=models.CASCADE)
    user=models.ForeignKey('Users.employees',on_delete=models.CASCADE,related_name='user_follow_notification')



class BlogNotification(models.Model):
    blog=models.ForeignKey(Blog,on_delete=models.CASCADE,related_name='blog_notification')
    read=models.BooleanField(default=False,db_index=True)
    sent_to=models.ForeignKey('Users.employees',on_delete=models.CASCADE)
    class Meta:
        unique_together=['blog','sent_to']