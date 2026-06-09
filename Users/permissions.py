from rest_framework.permissions import BasePermission
from Users.models import UserFollowing
from BLOG.models import OrganizationFollowing


class is_temp_pass(BasePermission):
    def has_permission(self, request, view):
        return (request.user.is_password_temp==True and request.user.role=='E')
    

class employee_verification(BasePermission):
    def has_permission(self, request, view):
        if request.user.role == 'F':
            
            if not request.user.is_verified:
                self.message = "Please verify your account"
                return False

            if not request.user.created_organization:
                self.message = "You must create an organization."
                return False

            return True
        
        elif request.user.role=='E':
            
            if request.user.is_password_temp==True:
                self.message('you must change your password once after login before you can perform any activity')
                return False
            
            return True
        
class Founder_Set_Up(BasePermission):
    def has_permission(self, request, view):
        return (request.user.role=='F' and request.user.is_verified==True and request.user.created_organization==True)
    

class is_Founder(BasePermission):
    def has_permission(self, request, view):
        return (request.user.role=='F' and request.user.is_verified==True and request.user.created_organization==False)
    

class BlogCreater(BasePermission):
    def has_permission(self, request, view):
        if request.user.role=='F':
            return (request.user.created_organization==True and request.user.is_verified==True)
        else:
            return (request.user.is_password_temp==False)
        

class SameOrganizatoin(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.organization==obj and request.user.role=='F'
    



class BlogReadPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        if obj.organization.type=='Pvt':
            following=UserFollowing.objects.select_related('following').filter(user_id=request.user.id).values_list('following__Name',flat=True)
            organizationfollowing=OrganizationFollowing.objects.select_related('following').filter(organization_id=request.user.organization_id).values_list('following__Name',flat=True)
            if request.user.organization==obj.organization:
                return True
            elif obj.organization.Name in following:
                return True
            elif obj.organization.Name in organizationfollowing :
                return True
            else:
                return False
        elif obj.organization.type=='Pub':
            return True
        else:
            return False
        

class BlogUpdatePermissions(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.id == obj.created_by_id
    


class BlogDeletePermissions(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.id == obj.created_by_id or obj.organization.founder_id==request.user.id
    

class CommentsUpdatePermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.id==obj.owner_id or obj.blog.organization.founder_id==request.user.id
    
class employeeDeletePermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.organization_id==obj.organization_id and request.user.role=='F' and request.user!=obj:
            return True
        return False
        
class delete_pin_permissions(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.organization_id==obj.blog.organization_id and request.user.role=='F':
            return True
        return False
