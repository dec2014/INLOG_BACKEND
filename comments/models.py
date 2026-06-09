from django.db import models
from BLOG.models import Blog

# Create your models here.

class Comments(models.Model):
    text=models.TextField()
    owner=models.ForeignKey('Users.employees',on_delete=models.CASCADE)
    blog=models.ForeignKey(Blog,on_delete=models.CASCADE)


