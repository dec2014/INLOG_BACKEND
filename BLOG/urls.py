


from django.urls import path
from .views import BlogViewSet

urlpatterns=[
    path(
        'organization/<int:pk>/blogs/',
        BlogViewSet.as_view({'get': 'list', 'post': 'create'})
    ),
    path(
        'blogs/<int:pk>/',
        BlogViewSet.as_view({
            'get': 'retrieve',
            'put': 'update',
            'patch': 'partial_update',
            'delete': 'destroy',
        })
    ),
]