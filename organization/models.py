from django.db import models

# Create your models here.


class Organization(models.Model):
    class types(models.TextChoices):
        PRIVATE='Pvt','Private'
        PUBLIC= 'Pub','Public'
    Name=models.CharField(max_length=255,unique=True)
    founder=models.OneToOneField('Users.employees',on_delete=models.CASCADE,related_name='founder')
    bio_pitcure=models.ImageField(upload_to='organizationProfile/',null=True,blank=True)
    type=models.CharField(choices=types.choices,default=types.PRIVATE,max_length=3)
    body=models.TextField()
