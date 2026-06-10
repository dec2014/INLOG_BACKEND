# from django.urls import path
# from . import views

# urlpatterns=[


#     path('blog-like/<str:pk>/',views.blogLike.as_view()),

#     path('employee-analytics/<str:pk>/',views.EmployeeAnalytics.as_view()),
#     path('organization-analytics/<str:pk>/',views.OrganizationAnalytics.as_view()),

#     path('employee-delete/<str:pk>/',views.employeeDelete.as_view()),
#     path('pin-blog/<str:pk>/',views.Pin_Blog.as_view()),
#     path('unpin-blog/<str:pk>/',views.unPinBlog.as_view()),
# ]



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