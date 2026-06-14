from django.contrib import admin
from BLOG.models import Blog
from organization.models import Organization
from streak.models import Streak
from follow.models import UserFollowing,OrganizationFollower,OrganizationFollowing
from Read.models import BlogRead
from like.models import BlogLike
from comments.models import Comments
from notifications.models import BlogNotification,FollowNotification
from tag.models import Tag
from organization.models import Organization



admin.site.register(Organization)
admin.site.register(Blog)
admin.site.register(UserFollowing)
admin.site.register(BlogRead)
admin.site.register(OrganizationFollower)
admin.site.register(OrganizationFollowing)
admin.site.register(Tag)
admin.site.register(BlogLike)
admin.site.register(Comments)
admin.site.register(BlogNotification)
admin.site.register(FollowNotification)
admin.site.register(Streak)

# Register your models here.
