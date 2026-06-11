from django.db import models
from organization.models import Organization
from tag.models import Tag
# Create your models here.




class Blog(models.Model):
    title=models.CharField(max_length=255)
    content=models.TextField()
    pictures=models.ImageField(upload_to='blog_profiles',null=True,blank=True)
    created_by=models.ForeignKey('Users.employees',on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now=True)
    organization=models.ForeignKey(Organization,on_delete=models.CASCADE)
    tag=models.ManyToManyField(Tag)








