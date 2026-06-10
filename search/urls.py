from django.urls import path
from .views import filter_blog

urlpatterns=[
    path('search-blog/',filter_blog.as_view()),

]