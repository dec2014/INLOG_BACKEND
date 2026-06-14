from django.shortcuts import render
from rest_framework import generics
from .service import follow,unfollow
from rest_framework_simplejwt.authentication import JWTAuthentication
from organization.models import Organization
from organization.serializers import OrganizationSerializers
from .permissions import followPermissions,unfollowPermissions
from rest_framework import permissions
# Create your views here.

class following(generics.CreateAPIView):
    queryset=Organization.objects.all()
    serializer_class=OrganizationSerializers
    lookup_field='Name'
    authentication_classes=[JWTAuthentication]
    permission_classes=[permissions.IsAuthenticated,followPermissions]
    def create(self, request, *args, **kwargs):
        obj=self.get_object()
        return follow(request,obj)
        
        


        


class unfollowing(generics.CreateAPIView):
    queryset=Organization.objects.all()
    serializer_class=OrganizationSerializers
    lookup_field='Name'
    authentication_classes=[JWTAuthentication]
    permission_classes=[permissions.IsAuthenticated,unfollowPermissions]
    def create(self, request, *args, **kwargs):
        obj=self.get_object()
        return unfollow(request,obj)