from rest_framework.permissions import BasePermission

class organizaition_creation_permission(BasePermission):
    def has_permission(self, request, view):
        if request.user.role != 'F':
            self.message = "Only founders can create organizations."
            return False

        return True
    
class organization_update_permission(BasePermission):
   
    def has_object_permission(self, request, view, obj):
        if request.user.role != 'F':
            self.message = "Only founders can create organizations."
            return False

        if request.user.organization_id!=obj.id:
            self.message="you are not the founder of organization. Only founder has the permission to edit the organization settings"
            return False
        return True
        
