from django.shortcuts import render
from rest_framework import generics,permissions
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.authentication import JWTAuthentication
from .serializers import commentsSerialization
from .service import get_all_comments,comment_permissions,comment_create_permission,comment_create,comment_update,comment_delete,get_comment_blog__organization_user,get_all_comment_of_blog,comment_get_list_permission

# Create your views here.
class CommentsViewSet(ModelViewSet):
    serializer_class=commentsSerialization
    authentication_classes=[JWTAuthentication]
    def get_queryset(self):
        if self.action=='create' or self.action=='update' or self.action=='partial_update' or self.action=='destroy' or self.action == 'retrieve':
            return get_comment_blog__organization_user()
        if self.action == 'list':
            return get_all_comment_of_blog(self.kwargs.get('pk'))

        return get_all_comments()

    def get_permissions(self):
        return comment_permissions(self)
    
    def create(self, request, *args, **kwargs):
        comment_create_permission(self,request,*args,**kwargs)

    def perform_create(self, serializer):
        comment_create(self,serializer)

    def perform_update(self, serializer):
        comment_update(self,serializer)

    def perform_destroy(self, instance):
        comment_delete(self,instance)

    def list(self, request, *args, **kwargs):
        comment_get_list_permission(self,request,*args,**kwargs)

    
        
    