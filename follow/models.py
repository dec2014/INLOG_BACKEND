from django.db import models
from organization.models import Organization
from django.db.models import Q,F

# Create your models here.
class OrganizationFollower(models.Model):
    organization=models.ForeignKey(Organization,on_delete=models.CASCADE,related_name='organization_follower')
    follower=models.ForeignKey(Organization,on_delete=models.CASCADE,null=True)
    class Meta:
        unique_together=['organization','follower'],

        constraints=[
            models.CheckConstraint(
                check=~Q(organization=F('follower')),
                name='organization_cannot_become_follower_of_itself'
            )
        ]



class OrganizationFollowing(models.Model):
    organization=models.ForeignKey(Organization,on_delete=models.CASCADE,related_name='organization_following')
    following=models.ForeignKey(Organization,on_delete=models.CASCADE,null=True)
    class Meta:
        unique_together=['organization','following']
        constraints=[
            models.CheckConstraint(
                check=~Q(organization=F('following')),
                name='organization_cannot_follow_itself'
            )
        ]


class UserFollowing(models.Model):
    following=models.ForeignKey(Organization,on_delete=models.CASCADE)
    user=models.ForeignKey('Users.employees',on_delete=models.CASCADE,related_name='user_following')
    class Meta:
        unique_together=['following','user']