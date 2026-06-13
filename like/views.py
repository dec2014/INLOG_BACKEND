from django.shortcuts import render
from rest_framework import generics
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from Users.permissions import employee_verification
from BLOG.permissions import Blog_access_permission
from BLOG.service import get_blog__organization_all,like_blog_by_users
from .service import like_unlike_blog
from BLOG.serializers import BlogSerializer
# Create your views here.
class blogLike(generics.CreateAPIView):
    lookup_field='pk'
    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated,employee_verification,Blog_access_permission]
    

    def get_queryset(self):
        return get_blog__organization_all()
    
    def create(self,request,*args,**kwargs):
        self.blog=self.get_object()
        return like_unlike_blog(self,request,*args,**kwargs)

        

class liked_blog_by_user(generics.ListAPIView):
    serializer_class=BlogSerializer
    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]
    def get_queryset(self):
        return like_blog_by_users(self.request.user)