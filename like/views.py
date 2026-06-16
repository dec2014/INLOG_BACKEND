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

from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter, OpenApiResponse

# Create your views here.

@extend_schema_view(
    post=extend_schema(
        summary="Toggle Like / Unlike State on a Blog",
        description=(
            "Toggles the interactive liking state of an organizational blog post for "
            "the requesting authenticated employee profile. Relies on internal service structures "
            "to register new likes or reverse existing record entries dynamically."
        ),
        tags=["Like Operations"],
        parameters=[
            OpenApiParameter(
                name="id", 
                type=int, 
                location=OpenApiParameter.PATH, 
                description="The unique database primary key identification integer tracking the target blog post."
            )
        ],
        responses={
            200: OpenApiResponse(description="Like entry inverted successfully (Blog Unliked)."),
            201: OpenApiResponse(description="Like record generated successfully (Blog Liked)."),
            401: OpenApiResponse(description="Authentication credentials missing, malformed, or expired."),
            403: OpenApiResponse(description="Access denied. Profile lacks valid permission parameters to interact with this post instance.")
        }
    )
)
class blogLike(generics.CreateAPIView):
    lookup_field='pk'
    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated,employee_verification,Blog_access_permission]
    

    def get_queryset(self):
        return get_blog__organization_all()
    
    def create(self,request,*args,**kwargs):
        self.blog=self.get_object()
        return like_unlike_blog(self,request,*args,**kwargs)

        
@extend_schema_view(
    get=extend_schema(
        summary="List Blogs Liked by Current User",
        description="Returns an array list of all corporate blog entries that the currently authenticated employee has explicitly liked.",
        tags=["Like Operations"],
        responses={
            200: OpenApiResponse(
                response=BlogSerializer(many=True), 
                description="Array collection of liked blog records successfully retrieved and parsed."
            ),
            401: OpenApiResponse(description="Token identification validation failed.")
        }
    )
)
class liked_blog_by_user(generics.ListAPIView):
    serializer_class=BlogSerializer
    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]
    def get_queryset(self):
        return like_blog_by_users(self.request.user)