
from rest_framework import generics
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from Users.permissions import employee_verification
from .service import employee_analytics,organization_analytics
from BLOG.service import get_all_blog

# Create your views here.
class EmployeeAnalytics(generics.RetrieveAPIView):
    queryset=get_all_blog()
    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated,employee_verification]
    def get(self, request, *args, **kwargs):
        return employee_analytics(self, request, *args, **kwargs)
        
    


class OrganizationAnalytics(generics.RetrieveAPIView):
    queryset=get_all_blog()
    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated,employee_verification]
    def get(self, request, *args, **kwargs):
        return organization_analytics(self, request, *args, **kwargs)
