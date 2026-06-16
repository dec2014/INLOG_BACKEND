from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.authentication import JWTAuthentication
from .service import get_all_organization,organization_create,organization_delete,organization_permissions
from .serializers import OrganizationSerializers,OrganizationRetrieveSerializers

# Create your views here.
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter, OpenApiResponse

# Configure custom overrides for the comprehensive CRUD viewset actions
@extend_schema_view(
    list=extend_schema(
        summary="List all Organizations",
        description="Returns an array catalog of all active organization networks currently tracked in the database architecture.",
        tags=["Organization Architecture"],
        responses={200: OpenApiResponse(response=OrganizationSerializers(many=True), description="Array list of corporate environments parsed successfully.")}
    ),
    create=extend_schema(
        summary="Register a new Organization Profile",
        description=(
            "Creates an institutional workspace network record. This binds the requesting founder user profile context "
            "as the administrative head of the generated platform instance."
        ),
        tags=["Organization Architecture"],
        request=OrganizationSerializers,
        responses={
            201: OpenApiResponse(response=OrganizationSerializers, description="Corporate organization profile instance generated cleanly."),
            400: OpenApiResponse(description="Structural execution conflicts. Often validation drops or duplicate domain name entry collisions.")
        }
    ),
    retrieve=extend_schema(
        summary="Fetch detailed Organization metadata",
        description="Retrieves granular overview fields, membership tracking profiles, and full payload metadata metrics for a specific workspace profile card.",
        tags=["Organization Architecture"],
        parameters=[
            OpenApiParameter(name="id", type=int, location=OpenApiParameter.PATH, description="The unique database primary key identification integer tracking the organization system profile.")
        ],
        responses={
            200: OpenApiResponse(response=OrganizationRetrieveSerializers, description="Deep profile schema payload successfully resolved and compiled."),
            404: OpenApiResponse(description="Target institutional index record does not exist or has been dropped from systemic tracking.")
        }
    ),
    update=extend_schema(
        summary="Overhaul Organization parameters (Complete)",
        description="Allows total dictionary attribute overrides across the targeted system workspace record metadata properties.",
        tags=["Organization Architecture"],
        request=OrganizationSerializers,
        responses={200: OpenApiResponse(response=OrganizationSerializers, description="Comprehensive object configuration updated.")}
    ),
    partial_update=extend_schema(
        summary="Patch Organization details (Incremental)",
        description="Update single or selective field strings (like altering text details or modifying structural text labels) on the system record profile.",
        tags=["Organization Architecture"],
        request=OrganizationSerializers,
        responses={200: OpenApiResponse(response=OrganizationSerializers, description="Targeted model parameters cleanly modified.")}
    ),
    destroy=extend_schema(
        summary="Dismantle / Delete an Organization Environment",
        description="Permanently drops the specified corporate environment cluster along with cascade tracking records cleanly from database registers.",
        tags=["Organization Architecture"],
        parameters=[
            OpenApiParameter(name="id", type=int, location=OpenApiParameter.PATH, description="The sequential database storage tracking tracking index ID targeted for record removal.")
        ],
        responses={
            204: OpenApiResponse(description="Workspace profile structure completely removed from systemic cluster nodes."),
            403: OpenApiResponse(description="Operation rejected. Requesting entity profile missing explicit founder authority boundaries to drop this corporate node.")
        }
    )
)
class OrganizationViewset(ModelViewSet):

    lookup_field='pk'
    authentication_classes=[JWTAuthentication]
    def get_serializer_class(self, *args, **kwargs):
        if self.action!='retrieve':
            return OrganizationSerializers
        return OrganizationRetrieveSerializers
    def get_queryset(self):
        return get_all_organization()
        
    
    def get_permissions(self):
        return organization_permissions(self)
       
    
    def perform_create(self, serializer):
        organization_create(self,serializer)
        

    def perform_destroy(self, instance):
        organization_delete(self,instance)
    
    