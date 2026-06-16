
from rest_framework_simplejwt.authentication import JWTAuthentication
from .serializers import BlogSerializer,BlogCreateSerializer,BlogListSerializer
from rest_framework.viewsets import ModelViewSet
from .service import blog_create,blog_permissions,get_blog__organization__user_all,blog_read,blog_update,filter_blog__organization__user,list_permission
from organization.service import get_all_organization
# Create your views here.

from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter, OpenApiResponse

# Create your views here.

@extend_schema_view(
    list=extend_schema(
        summary="List all Blogs within a specific Organization Context",
        description=(
            "Retrieves an array catalog of blog entries associated with a targeted organizational workspace. "
            "Requires the organization primary key ID to be provided inside the URL path string layout context."
        ),
        tags=["Main Blog Repository"],
        parameters=[
            OpenApiParameter(
                name="pk", 
                type=int, 
                location=OpenApiParameter.PATH, 
                description="The unique database primary key ID integer of the target parent organization to filter blogs by."
            )
        ],
        responses={
            200: OpenApiResponse(response=BlogListSerializer(many=True), description="Organizational blog list array successfully compiled and returned."),
            403: OpenApiResponse(description="Access restricted. Profile lacks explicit authorization clearance to browse this workspace index.")
        }
    ),
    create=extend_schema(
        summary="Publish a new Blog Post",
        description=(
            "Generates a new textual blog post entity record. Internally references and connects the workspace "
            "context boundaries derived from your custom organization lookups."
        ),
        tags=["Main Blog Repository"],
        request=BlogSerializer,
        responses={
            201: OpenApiResponse(response=BlogSerializer, description="Blog post generated successfully and broadcast parameters queued."),
            400: OpenApiResponse(description="Validation dropped or invalid JSON properties encountered.")
        }
    ),
    retrieve=extend_schema(
        summary="Fetch detailed Blog Post metadata",
        description="Reads granular overview parameters and body content metadata structures for an isolated corporate blog entry.",
        tags=["Main Blog Repository"],
        parameters=[
            OpenApiParameter(name="id", type=int, location=OpenApiParameter.PATH, description="The unique database primary key tracking ID of the targeted blog post.")
        ],
        responses={
            200: OpenApiResponse(response=BlogCreateSerializer, description="Granular blog entry configuration resolved and parsed cleanly."),
            404: OpenApiResponse(description="Target article instance index missing or dropped from active registers.")
        }
    ),
    update=extend_schema(
        summary="Overhaul Blog parameters (Complete Update)",
        description="Replaces every core parameter payload on the targeted corporate blog post. Restricted by employee author security policies.",
        tags=["Main Blog Repository"],
        request=BlogCreateSerializer,
        responses={200: OpenApiResponse(response=BlogCreateSerializer, description="Blog post data attributes completely rewritten.")}
    ),
    partial_update=extend_schema(
        summary="Patch Blog metadata fields (Incremental Update)",
        description="Applies partial updates to selective fields (such as updating only a title or changing text bodies) on an existing blog entry.",
        tags=["Main Blog Repository"],
        request=BlogCreateSerializer,
        responses={200: OpenApiResponse(response=BlogCreateSerializer, description="Targeted blog properties patched successfully.")}
    ),
    destroy=extend_schema(
        summary="Delete a Blog Post",
        description="Permanently drops a targeted corporate article record completely from organization systems alongside related comment and like arrays.",
        tags=["Main Blog Repository"],
        parameters=[
            OpenApiParameter(name="id", type=int, location=OpenApiParameter.PATH, description="The sequential database tracking index ID targeted for record removal.")
        ],
        responses={
            204: OpenApiResponse(description="Blog entry successfully dropped from active databases."),
            403: OpenApiResponse(description="Operation rejected. Profile lacks explicit workspace authority matrices to delete this record.")
        }
    )
)
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
    




    








