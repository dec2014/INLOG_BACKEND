from django.shortcuts import render
from rest_framework import generics
from .service import follow,unfollow
from rest_framework_simplejwt.authentication import JWTAuthentication
from organization.models import Organization
from organization.serializers import OrganizationSerializers
from .permissions import followPermissions,unfollowPermissions
from rest_framework import permissions
# Create your views here.


from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter, OpenApiResponse

# Create your views here.

@extend_schema_view(
    post=extend_schema(
        summary="Follow an Organization",
        description=(
            "Establishes a tracking follow status record between the authenticated context "
            "and a targeted system organization. The target organization entity is looked up "
            "directly using its unique corporate Name string identifier."
        ),
        tags=["Network Connections & Following"],
        parameters=[
            OpenApiParameter(
                name="Name", 
                type=str, 
                location=OpenApiParameter.PATH, 
                description="The unique, case-sensitive string Name identifier of the organization to follow."
            )
        ],
        responses={
            200: OpenApiResponse(description="Organization followed successfully."),
            201: OpenApiResponse(description="Follower record relationship created successfully."),
            401: OpenApiResponse(description="Authentication credentials missing or expired."),
            403: OpenApiResponse(description="Action restricted. You do not possess the required permission clearance to follow this node."),
            404: OpenApiResponse(description="No organization with the specified name string was found in the network registers.")
        }
    )
)
class following(generics.CreateAPIView):
    queryset=Organization.objects.all()
    serializer_class=OrganizationSerializers
    lookup_field='Name'
    authentication_classes=[JWTAuthentication]
    permission_classes=[permissions.IsAuthenticated,followPermissions]
    def create(self, request, *args, **kwargs):
        obj=self.get_object()
        return follow(request,obj)
        
        


        

@extend_schema_view(
    post=extend_schema(
        summary="Unfollow an Organization",
        description="Terminates an active following connection status record targeting a specific corporate node using its name identifier.",
        tags=["Network Connections & Following"],
        parameters=[
            OpenApiParameter(
                name="Name", 
                type=str, 
                location=OpenApiParameter.PATH, 
                description="The unique string Name identifier of the organization to unfollow."
            )
        ],
        responses={
            200: OpenApiResponse(description="Successfully unfollowed target organization node."),
            401: OpenApiResponse(description="Authentication token identification validation dropped."),
            404: OpenApiResponse(description="Target organization matching specified string was not found.")
        }
    )
)
class unfollowing(generics.CreateAPIView):
    queryset=Organization.objects.all()
    serializer_class=OrganizationSerializers
    lookup_field='Name'
    authentication_classes=[JWTAuthentication]
    permission_classes=[permissions.IsAuthenticated,unfollowPermissions]
    def create(self, request, *args, **kwargs):
        obj=self.get_object()
        return unfollow(request,obj)