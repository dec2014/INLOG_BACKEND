from django.shortcuts import render
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import permissions,generics,mixins
from Users.permissions import is_Founder
from .serializers import BlogSerializer
from Users.permissions import is_Founder,Founder_Set_Up,BlogCreater,SameOrganizatoin,followPermissions,unfollowPermissions,BlogReadPermission,BlogUpdatePermissions,CommentsUpdatePermission,BlogDeletePermissions,employeeDeletePermission,delete_pin_permissions
from .consumers import organization
from .models import Blog,Tag,BlogLike,BlogRead,PinBlog
from channels.layers import get_channel_layer
from organization.models import Organization
from asgiref.sync import async_to_sync
from Users.models import NewUser,UserFollowing
from django.shortcuts import get_object_or_404
from django.db.models import Q,F,Count
from django.utils import timezone
from rest_framework.viewsets import ModelViewSet
from .service import blog_create,blog_permissions,get_blog__organization__user_all,blog_read,blog_update,filter_blog__organization__user,list_permission
from organization.service import get_all_organization
# Create your views here.





class BlogViewSet(ModelViewSet):
    serializer_class=BlogSerializer
    authentication_classes=[JWTAuthentication]
    lookup_field='pk'


    def get_queryset(self):
        if self.action=='retrieve' or self.action=='update' or self.action=='partial_update' or self.action=='destroy':
            return get_blog__organization__user_all()
        elif self.action=='create':
            return get_all_organization()
        else:
            return filter_blog__organization__user(self.kwargs.get('pk'))

    
    def get_permissions(self):
        return blog_permissions(self)
    
    def create(self, request, *args, **kwargs):
        self.obj=self.get_object()
        return super().create(request, *args, **kwargs)

    
    def perform_create(self, serializer):
        blog_create(self,serializer)
    
    def retrieve(self, request, *args, **kwargs):
        self.blog=self.get_object()
        blog_read(self,request,*args,**kwargs)

    def perform_update(self, serializer):
        blog_update(self,serializer)
    
    def list(self, request, *args, **kwargs):
        list_permission(self,request,*args,**kwargs)
    


class blogLike(generics.GenericAPIView):
    authentication_classes=[JWTAuthentication]
    permission_classes=[permissions.IsAuthenticated,BlogCreater]
    def post(self,request,*args,**kwargs):
        blog=Blog.objects.select_related('organization').get(id=kwargs.get('pk'))
        userfollowing=UserFollowing.objects.select_related('following').filter(user_id=request.user.id,following_id=blog.organization_id).exists()
        organizationfollowing=OrganizationFollowing.objects.filter(organization_id=request.user.organization_id,following_id=blog.organization_id).exists()
        if blog.organization_id==request.user.organization_id or userfollowing or organizationfollowing or blog.organization.type == Organization.types.PUBLIC:
            obj,created=BlogLike.objects.update_or_create(
                blog=blog,
                like_user_id=request.user.id,
            )
            if not created:
                obj.like= not obj.like
                obj.save()


            streak=Streak.objects.get(user_streak_id=request.user.id)
            time_now=timezone.now().date()
            if streak.last_activity_date is None:
                streak.last_activity_date=time_now
                streak.count=1
                if streak.max_streak<streak.count:
                    streak.max_streak=streak.count
                streak.save()
            else:
                last_acitivity=streak.last_activity_date.date()
                differnce=time_now-last_acitivity
                if differnce.days==0:
                    pass
                elif differnce.days==1:
                    streak.last_activity_date=time_now
                    streak.count+=1
                    if streak.max_streak<streak.count:
                        streak.max_streak=streak.count
                    streak.save()
                else:
                    streak.last_activity_date=time_now
                    streak.count=0
                    streak.save()

            return Response({'like':obj.like,'created':created})
        return Response('error not given permission')













class EmployeeAnalytics(generics.RetrieveAPIView):
    queryset=Blog.objects.all()
    serializer_class=BlogReadSerialization
    authentication_classes=[JWTAuthentication]
    permission_classes=[permissions.IsAuthenticated,BlogCreater]
    def get(self, request, *args, **kwargs):
        total_post=Blog.objects.select_related('organization').filter(created_by_id=kwargs.get('pk')).count()
        total_comments=Comments.objects.filter(owner_id=kwargs.get('pk')).count()
        total_likes=BlogLike.objects.filter(like_user_id=kwargs.get('pk'),like=True).count()
        total_reads=BlogRead.objects.filter(read_by_id=kwargs.get('pk')).count()
        streak=Streak.objects.get(user_streak_id=kwargs.get('pk'))
        count=streak.count
        max_streak=streak.max_streak
        return Response({'total_post':total_post,'total_comments':total_comments,'total_likes':total_likes,'total_reads':total_reads,'count':count,'max_streak':max_streak})
    


class OrganizationAnalytics(generics.RetrieveAPIView):
    queryset=Organization.objects.all()
    serializer_class=OrganizatoinSerializers
    authentication_classes=[JWTAuthentication]
    permission_classes=[permissions.IsAuthenticated,BlogCreater]
    def get(self, request, *args, **kwargs):
        from Users.models import NewUser
        total_employee=NewUser.objects.filter(organization_id=kwargs.get('pk')).count()
        total_blog=Blog.objects.filter(organization_id=kwargs.get('pk')).count()
        total_read=BlogRead.objects.select_related('blog').filter(blog__organization_id=kwargs.get('pk')).count()
        total_followers=OrganizationFollower.objects.filter(organization_id=kwargs.get('pk')).count()
        top_employee=Streak.objects.select_related('user_streak').filter(user_streak__organization_id=kwargs.get('pk')).order_by('-count').first().user_streak.user_name
        top_post_id=BlogLike.objects.filter(blog__organization_id=kwargs.get('pk'),like=True).values('blog').annotate(total=Count('blog')).order_by('-total').first()
        if top_post_id:
            top_post_id=top_post_id['blog']
            top_post=Blog.objects.get(id=top_post_id)
            serializer=BlogReadSerialization(top_post)
            return Response({'total_employee':total_employee,'total_blog':total_blog,'total_read':total_read,'total_followers':total_followers,'top_employee':top_employee,'top_post':serializer.data})
        return Response({'total_employee':total_employee,'total_blog':total_blog,'total_read':total_read,'total_followers':total_followers,'top_employee':top_employee,'top_post':'no likes'})



    





class employeeDelete(generics.DestroyAPIView):
    queryset=NewUser.objects.all()
    lookup_field='pk'
    authentication_classes=[JWTAuthentication]
    permission_classes=[permissions.IsAuthenticated,BlogCreater,employeeDeletePermission]




class Pin_Blog(generics.CreateAPIView):
    authentication_classes=[JWTAuthentication]
    permission_classes=[permissions.IsAuthenticated,BlogCreater]
    def create(self, request, *args, **kwargs):
        blog=Blog.objects.get(id=kwargs.get('pk'))
        if request.user.organization_id==blog.organization_id and request.user.role=='F':
            PinBlog.create(blog=blog)
            return Response('pinned Blog')
        return Response('no permission')
    
    
class unPinBlog(generics.DestroyAPIView):
    queryset=PinBlog.objects.all()
    lookup_field='pk'
    authentication_classes=[JWTAuthentication]
    permission_classes=[permissions.IsAuthenticated,BlogCreater,delete_pin_permissions]
    def get_queryset(self):
        return PinBlog.objects.select_related('blog').all()
        