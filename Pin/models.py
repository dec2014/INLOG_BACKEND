from django.db import models
from BLOG.models import Blog
# Create your models here.
class PinBlog(models.Model):
    pin_by=models.ForeignKey('Users.employees',on_delete=models.CASCADE)
    blog=models.ForeignKey(Blog,on_delete=models.CASCADE,related_name='pinnedblog')
    pin=models.BooleanField(default=True,db_index=True)
    founder_pin=models.BooleanField(default=False,db_index=True)
    class Meta:
        unique_together=['blog','pin_by']

