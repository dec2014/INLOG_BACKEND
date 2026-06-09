from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import ValidationError
from .permissions import organizaition_creation_permission,organization_update_permission
from .service import get_all_organization,organization_create,organization_delete,organization_permissions
from django.db import transaction
from .serializers import OrganizationSerializers

# Create your views here.

class OrganizationViewset(ModelViewSet):
    serializer_class=OrganizationSerializers
    lookup_field='pk'
    authentication_classes=[JWTAuthentication]
    def get_queryset(self):
        return get_all_organization()
    
    def get_permissions(self):
        organization_permissions(self)
       
    
    def perform_create(self, serializer):
        organization_create(self,serializer)
        

    def perform_destroy(self, instance):
        organization_delete(self,instance)
    
    