
from rest_framework import generics
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from Users.permissions import employee_verification
from .service import employee_analytics,organization_analytics
from BLOG.service import get_all_blog

# Create your views here.

from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiResponse

# Create your views here.

@extend_schema_view(
    get=extend_schema(
        summary="Retrieve Individual Employee Analytics",
        description=(
            "Compiles and returns performance metrics, post counts, total engagement weights (likes/comments), "
            "and activity tracking data for the individual authenticated employee context."
        ),
        tags=["Analytics & Metrics Dashboard"],
        responses={
            200: OpenApiResponse(
                description="Personal engagement data and activity metrics compiled successfully."
            ),
            401: OpenApiResponse(description="Authentication credentials missing, malformed, or expired."),
            440: OpenApiResponse(description="Access restricted. Target account email verification status incomplete.")
        }
    )
)
class EmployeeAnalytics(generics.RetrieveAPIView):
    queryset=get_all_blog()
    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated,employee_verification]
    def get(self, request, *args, **kwargs):
        return employee_analytics(self, request, *args, **kwargs)
        
    

@extend_schema_view(
    get=extend_schema(
        summary="Retrieve Workspace Organization Analytics",
        description=(
            "Aggregates system-wide analytics records, community health percentages, overall publication "
            "metrics, and macro engagement statistics across the entire organization environment cluster."
        ),
        tags=["Analytics & Metrics Dashboard"],
        responses={
            200: OpenApiResponse(
                description="Workspace macro tracking indices and organizational metrics compiled successfully."
            ),
            401: OpenApiResponse(description="Authentication credentials dropped."),
            403: OpenApiResponse(description="Access denied. Requesting identity lacks workspace authority scope rules.")
        }
    )
)
class OrganizationAnalytics(generics.RetrieveAPIView):
    queryset=get_all_blog()
    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated,employee_verification]
    def get(self, request, *args, **kwargs):
        return organization_analytics(self, request, *args, **kwargs)
