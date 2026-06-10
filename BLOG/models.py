from django.db import models
from django.db.models import Q,F
from organization.models import Organization
from tag.models import Tag

from datetime import datetime,time

# Create your models here.
from organization.models import Organization



class Blog(models.Model):
    title=models.CharField(max_length=255)
    content=models.TextField()
    pictures=models.ImageField(upload_to='blog_profiles',null=True,blank=True)
    created_by=models.ForeignKey('Users.employees',on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now=True)
    organization=models.ForeignKey(Organization,on_delete=models.CASCADE)
    tag=models.ManyToManyField(Tag)


class PinBlog(models.Model):
    pin_by=models.ForeignKey('Users.employees',on_delete=models.CASCADE)
    blog=models.OneToOneField(Blog,on_delete=models.CASCADE,related_name='pinnedblog')








