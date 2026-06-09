from django.urls import path
from . import views

urlpatterns=[
    path('follow/<str:Name>/',views.following.as_view()),
    path('unfollow/<str:Name>/',views.unfollowing.as_view()),
]