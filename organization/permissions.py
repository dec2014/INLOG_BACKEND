from rest_framework.permissions import BasePermission

class organizaition_creation_permission(BasePermission):
    def has_permission(self, request, view):
        if request.user.role != 'F':
            self.message = "Only founders can create organizations."
            return False
        if request.user.is_verified != True:
            self.message='you must verify yourself to create the organization.'
            return False
        return True

class organization_update_permission(BasePermission):
   
    def has_object_permission(self, request, view, obj):
        if request.user.role != 'F':
            self.message = "Only founders can update organizations."
            return False

        if request.user.organization_id!=obj.id:
            self.message="you are not the founder of organization. Only founder has the permission to edit the organization settings"
            return False
        return True
        
class belong_to_same_organization(BasePermission):
    def has_object_permission(self, request, view, obj):
        if obj.id!=request.user.organization_id:
            self.message='you cannot create the blog for this organization as you do not belong to it.'
            return False
        return True