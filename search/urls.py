from django.urls import path
from .views import SearchingBlogs

urlpatterns=[
    path('search-blog/',SearchingBlogs.as_view()),

]