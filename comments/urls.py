from django.urls import path
from .views import CommentsViewSet

urlpatterns=[
    path(
        'blogs/<int:pk>/comments/',
        CommentsViewSet.as_view({'get': 'list', 'post': 'create'})
    ),
    path(
        'comments/<int:pk>/',
        CommentsViewSet.as_view({
            'get': 'retrieve',
            'put': 'update',
            'patch': 'partial_update',
            'delete': 'destroy',
        })
    ),
]