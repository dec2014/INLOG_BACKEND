from .models import Organization
from rest_framework.exceptions import ValidationError,APIException
from rest_framework.permissions import IsAuthenticated
from .permissions import organizaition_creation_permission,organization_update_permission
from Users.permissions import employee_verification
from django.db import transaction

def get_all_organization():
    return Organization.objects.all()

@transaction.atomic
def organization_create(self,serializer):
    try:
        user=self.request.user
        organization=serializer.save(founder=self.request.user)
        user.created_organization=True
        user.organization_id=organization.id
        user.save()
    except Exception as e :
        raise ValidationError(
        {   
            'error':'organization not created',
            'details':str(e)
        }
        )


def organization_permissions(self):
    permission_map = {

    'list': [IsAuthenticated,employee_verification],

    'retrieve': [IsAuthenticated,employee_verification],

    'create': [IsAuthenticated,employee_verification,organizaition_creation_permission],

    'update': [IsAuthenticated,employee_verification,organization_update_permission],

    'partial_update': [IsAuthenticated,employee_verification,organization_update_permission],

    'destroy': [IsAuthenticated,employee_verification,organization_update_permission],
    }
    permissions=permission_map.get(self.action,[IsAuthenticated])
    return [permission() for permission in permissions]

@transaction.atomic
def organization_delete(self,instance):
    try:
        user=self.request.user
        user.created_organization=False
        user.organization_id=None
        user.save()
        return super().perform_destroy(instance)
    except Exception as e:
        raise ValidationError({
            'error':'organization not deleted',
            'detail': str(e)
        })