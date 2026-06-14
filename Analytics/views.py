
from rest_framework import generics
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from Users.permissions import employee_verification
from .service import employee_analytics,organization_analytics

# Create your views here.
class EmployeeAnalytics(generics.RetrieveAPIView):
    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated,employee_verification]
    def get(self, request, *args, **kwargs):
        return employee_analytics(self, request, *args, **kwargs)
        
    


class OrganizationAnalytics(generics.RetrieveAPIView):
    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated,employee_verification]
    def get(self, request, *args, **kwargs):
        return organization_analytics(self, request, *args, **kwargs)
