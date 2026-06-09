from django.db import models

# Create your models here.
class Streak(models.Model):
    user_streak=models.OneToOneField('Users.employees',on_delete=models.CASCADE)
    count=models.IntegerField(default=0,db_index=True)
    last_activity_date=models.DateTimeField(null=True,blank=True)
    max_streak=models.IntegerField(default=0,db_index=True)