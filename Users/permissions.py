from rest_framework.permissions import BasePermission
from follow.service import user_following_list_exists,organization_following_list_exists
from .models import employees

class is_temp_pass(BasePermission):
    def has_permission(self, request, view):
        # return (request.user.is_password_temp==True and request.user.role=='E')
        if request.user.role == employees.roles.EMPLOYEE:
            
            if request.user.is_password_temp == False:
                self.message = "you do not have permission to reset your password.please contact the admin"
                return False
            return True
        return True
    

class employee_verification(BasePermission):
    def has_permission(self, request, view):
        if request.user.role == employees.roles.FOUNDER:
            
            if not request.user.is_verified:
                self.message = "Please verify your account"
                return False

            if not request.user.created_organization:
                self.message = "You must create an organization."
                return False

            return True
        
        elif request.user.role==employees.roles.EMPLOYEE:
            
            if request.user.is_password_temp==True:
                self.message('you must change your password once after login before you can perform any activity')
                return False
            
            return True
        
class Founder_Set_Up(BasePermission):
    def has_permission(self, request, view):
        if request.user.role != employees.roles.FOUNDER:
            self.message='you must be a founder.'
            return False
            
        if not request.user.is_verified:
            self.message = "Please verify your account"
            return False

        if not request.user.created_organization:
            self.message = "You must create an organization."
            return False

        return True

    



class employee_view_permission(BasePermission):
    def has_object_permission(self, request, view, obj):
        if obj.organization.type=='Pvt':
            following_exists=user_following_list_exists(request.user.id,obj.organization.id)
            organizationfollowing_exists=organization_following_list_exists(request.user.organization_id, obj.organization.id)
            if request.user.organization==obj.organization or following_exists or organizationfollowing_exists :
                return True
            else :
                self.message=f'you must belong to or follow the organization {obj.blog.organization.Name} to get the employee '
                return False
            
        elif obj.organization.type=='Pub':
            return True




class employeeDeletePermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.role !=employees.roles.FOUNDER:
            self.message='you cannot perform the action as you are not the founder of the organizaiton'
            return False

        if request.user.id==obj.id:
            self.message='you cannot delete the account of yourself .'
            return False

        if request.user.organization_id!=obj.organization_id:
            self.message='you can only delete employees who belong to your organization'
            return False

        
        return True

        
