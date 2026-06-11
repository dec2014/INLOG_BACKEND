from django.urls import path
from .views import Pin_unpin_blog,pinned_blog_by_organization,pinned_blog_by_user

urlpatterns=[
    path('pin-blog/<int:pk>/',Pin_unpin_blog.as_view()),
    path('pin-blog-user/<int:pk>/',pinned_blog_by_user.as_view()),
    path('pin-blog-organization/<int:pk>/',pinned_blog_by_organization.as_view())
]