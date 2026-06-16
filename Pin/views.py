from django.shortcuts import render
from rest_framework import generics
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from BLOG.service import get_blog__organization_all,blog_pinned_by_organization,blog_pinned_by_user,get_all_blog
from BLOG.permissions import Blog_access_permission
from .service import pin_blog
from BLOG.serializers import BlogSerializer
from Users.permissions import employee_verification
from rest_framework.exceptions import ValidationError

# Create your views here.

from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter, OpenApiResponse

# Create your views here.

@extend_schema_view(
    post=extend_schema(
        summary="Toggle Pin / Unpin State on a Blog",
        description=(
            "Toggles the pinned tracking state of an organizational blog post instance for "
            "the requesting profile context. Relies on internal service rules to record "
            "either regular employee pins or specialized company founder pins."
        ),
        tags=["Pin Operations"],
        parameters=[
            OpenApiParameter(
                name="id", 
                type=int, 
                location=OpenApiParameter.PATH, 
                description="The sequential database primary key tracking ID of the specific blog post to pin/unpin."
            )
        ],
        responses={
            200: OpenApiResponse(description="Pin status state updated successfully."),
            201: OpenApiResponse(description="Blog pinning entry record created successfully."),
            400: OpenApiResponse(description="Action broken. Target context object tracking matches or operational failures."),
            401: OpenApiResponse(description="Authentication credentials missing, malformed, or expired."),
            403: OpenApiResponse(description="Access restricted. Profile lacks explicit authorization parameters to manage this post entry.")
        }
    )
)
class Pin_unpin_blog(generics.CreateAPIView):

    authentication_classes=[JWTAuthentication]
    lookup_field='pk'
    permission_classes=[IsAuthenticated,employee_verification,Blog_access_permission]
    
    def get_queryset(self):
        return get_blog__organization_all()
    
    def create(self, request, *args, **kwargs):
        try:
            self.blog=self.get_object()
        except Exception as e:
            raise ValidationError(f'could not create the pin.{str(e)}')
        return pin_blog(self,request,*args,**kwargs)

@extend_schema_view(
    get=extend_schema(
        summary="List Blogs pinned by Current User",
        description="Returns an array catalog payload of all blog posts explicitly pinned by the individual authenticated worker account.",
        tags=["Pin Operations"],
        responses={
            200: OpenApiResponse(response=BlogSerializer(many=True), description="User pin array listings parsed successfully.")
        }
    )
)
class pinned_blog_by_user(generics.ListAPIView):

    serializer_class=BlogSerializer
    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]
    def get_queryset(self):
        return blog_pinned_by_user(self.request.user)
    

@extend_schema_view(
    get=extend_schema(
        summary="List Pinned Corporate-Wide Blogs",
        description="Fetches the collection of blog entries pinned on an administrative, organization-wide scale by company founders.",
        tags=["Pin Operations"],
        responses={
            200: OpenApiResponse(response=BlogSerializer(many=True), description="Corporate organizational pinned list collection parsed successfully.")
        }
    )
)
class pinned_blog_by_organization(generics.ListAPIView):

    serializer_class=BlogSerializer
    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]
    def get_queryset(self):
        return blog_pinned_by_organization(self.request.user)