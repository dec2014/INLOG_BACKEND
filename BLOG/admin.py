from django.contrib import admin
from .models import Blog,FollowUnNotification,OrganizationFollowing,OrganizationFollower,Tag,Streak
from organization.models import Organization
from Users.models import UserFollowing


admin.site.register(Organization)
admin.site.register(Blog)
admin.site.register(UserFollowing)
admin.site.register(FollowUnNotification)
admin.site.register(OrganizationFollower)
admin.site.register(OrganizationFollowing)
admin.site.register(Tag)
admin.site.register(Streak)
# Register your models here.
