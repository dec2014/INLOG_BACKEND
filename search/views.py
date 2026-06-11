from django.shortcuts import render
from rest_framework import generics
from BLOG.models import Blog
from BLOG.serializers import BlogSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from Users.permissions import employee_verification
from .service import filter_blog

# Create your views here.
class SearchingBlogs(generics.ListAPIView):
    queryset=Blog.objects.all()
    serializer_class=BlogSerializer
    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated,employee_verification]
    def get_queryset(self):
        return filter_blog(self)
   
