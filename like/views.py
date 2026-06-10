from django.shortcuts import render
from rest_framework import generics
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from Users.permissions import employee_verification
from BLOG.permissions import Blog_access_permission
from BLOG.service import get_blog__organization_all
from .service import like_unlike_blog
# Create your views here.
class blogLike(generics.CreateAPIView):
    lookup_field='pk'
    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated,employee_verification,Blog_access_permission]
    

    def get_queryset(self):
        return get_blog__organization_all()
    
    def create(self,request,*args,**kwargs):
        self.blog=self.get_object()
        like_unlike_blog(self,request,*args,**kwargs)

        