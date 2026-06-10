from django.db import models
from BLOG.models import Blog

# Create your models here.
class BlogRead(models.Model):
    blog=models.ForeignKey(Blog,on_delete=models.CASCADE,related_name='blog_read')
    read_by=models.ForeignKey('Users.employees',on_delete=models.CASCADE)
    class Meta:
        unique_together=['blog','read_by']
