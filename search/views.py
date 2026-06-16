from django.shortcuts import render
from rest_framework import generics
from BLOG.models import Blog
from BLOG.serializers import BlogSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from Users.permissions import employee_verification
from .service import filter_blog

# Create your views here.


from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter, OpenApiResponse

# Configure the Swagger documentation layer for the search endpoint
@extend_schema_view(
    get=extend_schema(
        summary="Search and Filter Blog Posts",
        description=(
            "Retrieve a filtered list of organizational blog posts. This endpoint evaluates "
            "incoming query parameters processed by the underlying service layer to return "
            "relevant entries matching your search parameters."
        ),
        tags=["Blog Operations"],
        parameters=[
            OpenApiParameter(
                name="search", 
                type=str, 
                location=OpenApiParameter.QUERY, 
                description="The text keyword string to query against blog titles, contents, or tags."
            ),
        ],
        responses={
            200: OpenApiResponse(
                response=BlogSerializer(many=True), 
                description="An array list of matching blog post records successfully retrieved."
            ),
            401: OpenApiResponse(
                description="Authentication credentials (Bearer JWT token) missing, malformed, or expired."
            ),
            440: OpenApiResponse(
                description="Access locked. Employee profile has not completed email verification requirements."
            )
        }
    )
)
class SearchingBlogs(generics.ListAPIView):
    queryset=Blog.objects.all()
    serializer_class=BlogSerializer
    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated,employee_verification]
    def get_queryset(self):
        return filter_blog(self)
   
