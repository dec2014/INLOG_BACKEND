from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.authentication import JWTAuthentication
from .serializers import commentsSerialization
from .service import get_all_comments,comment_permissions,comment_create_permission,comment_create,comment_update,comment_delete,get_comment_blog__organization_user,get_all_comment_of_blog,comment_get_list_permission

# Create your views here.
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter, OpenApiResponse
@extend_schema_view(
    list=extend_schema(
        summary="List all Comments for a specific Blog",
        description=(
            "Retrieves an array catalog payload of all comments linked directly to a targeted blog "
            "post instance. Expects the blog primary key ID to be supplied inside the URL path variables."
        ),
        tags=["Comment Operations"],
        parameters=[
            OpenApiParameter(
                name="pk", 
                type=int, 
                location=OpenApiParameter.PATH, 
                description="The unique database tracking primary key ID integer of the parent blog post to query comments for."
            )
        ],
        responses={
            200: OpenApiResponse(response=commentsSerialization(many=True), description="Array list of comment entities parsed successfully."),
            403: OpenApiResponse(description="Access restricted. Profile lacks contextual authorization to inspect discussion streams on this post.")
        }
    ),
    create=extend_schema(
        summary="Post a new Comment",
        description="Creates a new text comment node thread attached to a target organizational blog entry post.",
        tags=["Comment Operations"],
        request=commentsSerialization,
        responses={
            201: OpenApiResponse(response=commentsSerialization, description="Comment generated and posted cleanly into discussion registries."),
            400: OpenApiResponse(description="Validation drop anomalies or invalid payload configurations encountered."),
            403: OpenApiResponse(description="Operational permissions fallback. Posting access rejected by security interceptors.")
        }
    ),
    retrieve=extend_schema(
        summary="Fetch explicit Comment record details",
        description="Retrieves a singular comment record metadata instance using its explicit database tracking ID element.",
        tags=["Comment Operations"],
        parameters=[
            OpenApiParameter(name="id", type=int, location=OpenApiParameter.PATH, description="The unique database primary key identification integer tracking the target comment instance.")
        ],
        responses={
            200: OpenApiResponse(response=commentsSerialization, description="Single comment schema structure successfully compiled and resolved."),
            440: OpenApiResponse(description="Action restricted. Target identity verification layers are incomplete.")
        }
    ),
    update=extend_schema(
        summary="Modify Comment payload (Complete Overhaul)",
        description="Completely replaces data parameters on a specified comment instance. Restricted by ownership parameters managed via custom service interceptors.",
        tags=["Comment Operations"],
        request=commentsSerialization,
        responses={200: OpenApiResponse(response=commentsSerialization, description="Comment body completely overhauled successfully.")}
    ),
    partial_update=extend_schema(
        summary="Edit Comment content (Incremental Patch)",
        description="Allows minor inline textual patches or incremental field data manipulation actions on an existing comment entry.",
        tags=["Comment Operations"],
        request=commentsSerialization,
        responses={200: OpenApiResponse(response=commentsSerialization, description="Comment properties cleanly patched.")}
    ),
    destroy=extend_schema(
        summary="Remove / Delete a Comment",
        description="Permanently drops a targeted comment record entity tracking entry directly from organizational comment systems.",
        tags=["Comment Operations"],
        parameters=[
            OpenApiParameter(name="id", type=int, location=OpenApiParameter.PATH, description="The sequential database tracking tracking index ID targeted for record removal.")
        ],
        responses={
            204: OpenApiResponse(description="Comment entity successfully removed from system workspace layers."),
            403: OpenApiResponse(description="Deletion rejected. Requesting profile lacks appropriate authority or structural authorship tracking vectors to drop this comment.")
        }
    )
)
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
        val=comment_create_permission(self,request,*args,**kwargs)
        if val:
            return super().create(request, *args, **kwargs)
        else:
            return val

    def perform_create(self, serializer):
        comment_create(self,serializer)

    def perform_update(self, serializer):
        comment_update(self,serializer)

    def perform_destroy(self, instance):
        comment_delete(self,instance)

    def list(self, request, *args, **kwargs):
        val=comment_get_list_permission(self,request,*args,**kwargs)
        if val:
            return super().list(request, *args, **kwargs)
        else:
            return val


    
        
    