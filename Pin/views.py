from django.shortcuts import render
from rest_framework import generics
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from BLOG.service import get_blog__organization_all,blog_pinned_by_organization,blog_pinned_by_user
from BLOG.permissions import Blog_access_permission
from .service import pin_blog
from BLOG.serializers import BlogSerializer
from Users.permissions import employee_verification

# Create your views here.

class Pin_unpin_blog(generics.CreateAPIView):
    authentication_classes=[JWTAuthentication]
    lookup_field='pk'
    permission_classes=[IsAuthenticated,employee_verification,Blog_access_permission]
    
    def get_queryset(self):
        return get_blog__organization_all()
    
    def create(self, request, *args, **kwargs):
        self.blog=self.get_object()
        pin_blog(self,request,*args,**kwargs)


class pinned_blog_by_user(generics.ListAPIView):
    serializer_class=BlogSerializer
    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]
    def get_queryset(self):
        return blog_pinned_by_user(self.user)
    


class pinned_blog_by_organization(generics.ListAPIView):
    serializer_class=BlogSerializer
    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]
    def get_queryset(self):
        return blog_pinned_by_organization(self.user)