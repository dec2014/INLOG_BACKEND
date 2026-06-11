
from django.urls import path
from .views import blogLike

urlpatterns=[


    path('blog-like/<int:pk>/',blogLike.as_view())
]