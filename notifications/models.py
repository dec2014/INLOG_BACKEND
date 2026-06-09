from django.db import models

# Create your models here.
class FollowNotification(models.Model):
    content=models.TextField()
    read=models.BooleanField(default=False,db_index=True)
    owner=models.ForeignKey('Users.employees',on_delete=models.CASCADE)
    user=models.ForeignKey('Users.employees',on_delete=models.CASCADE,related_name='user_follow_notification')