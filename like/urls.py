
from django.urls import path
from .views import blogLike,liked_blog_by_user

urlpatterns=[


    path('blog-like/<int:pk>/',blogLike.as_view()),
    path('blog-like-all/',liked_blog_by_user.as_view())
]