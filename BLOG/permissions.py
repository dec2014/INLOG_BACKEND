from rest_framework.permissions import BasePermission
from follow.service import user_following_list_exists,organization_following_list_exists

class Blog_access_permission(BasePermission):
    def has_object_permission(self, request, view, obj):
        if obj.organization.type=='Pvt':
            following_exists=user_following_list_exists(request.user.id,obj.organization_id)
            organizationfollowing_exists=organization_following_list_exists(request.user.organization_id, obj.organization_id)
            if request.user.organization==obj.organization or following_exists or organizationfollowing_exists :
                return True
            else :
                self.message=f'you must belong to or follow the organization {obj.organization.Name} to read a blog '
                return False
            
        elif obj.organization.type=='Pub':
            return True


class blog_update_destroy_permission(BasePermission):
    def has_object_permission(self, request, view, obj):
        if obj.organization_id==request.user.organization_id or obj.organization.founder_id==request.user.id:
            return True
        self.message='you donot have the permission to update or destroy the blog as you are not owner of blog or founder of the organization the blog belong to.'
        return False
        