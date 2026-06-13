
from rest_framework_simplejwt.authentication import JWTAuthentication
from .serializers import BlogSerializer,BlogCreateSerializer,BlogListSerializer
from rest_framework.viewsets import ModelViewSet
from .service import blog_create,blog_permissions,get_blog__organization__user_all,blog_read,blog_update,filter_blog__organization__user,list_permission
from organization.service import get_all_organization
# Create your views here.





class BlogViewSet(ModelViewSet):
    serializer_class=BlogSerializer
    authentication_classes=[JWTAuthentication]
    lookup_field='pk'

    def get_serializer_class(self, *args, **kwargs):
        if self.action=='retrieve' or self.action=='update' or self.action=='partial_update' or self.action=='destroy':
            return BlogCreateSerializer
        elif self.action=='create':
            return BlogSerializer
        else:
            return BlogListSerializer
    def get_queryset(self):
        print('called')
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
        return blog_read(self,request,*args,**kwargs)

    def perform_update(self, serializer):
        blog_update(self,serializer)
        return super().perform_update(serializer)
    
    def list(self, request, *args, **kwargs):
        val= list_permission(self,request,*args,**kwargs)
        if val:
            return super().list(request, *args, **kwargs)
        else:
            return val
    




    








