from django.urls import path,include
from rest_framework.routers import DefaultRouter
from . import views

router=DefaultRouter()
router.register(
    r'organizations',
    views.OrganizationViewset,
    basename='organization'
)
urlpatterns=[
    path('',include(router.urls))
    ]
