from rest_framework.permissions import BasePermission
from follow.service import get_organization_following_list,get_user_following_list

class Blog_access_permission(BasePermission):
    def has_object_permission(self, request, view, obj):
        if obj.blog.organization.type=='Pvt':
            following=get_user_following_list(request.user.id)
            organizationfollowing=get_organization_following_list(request.user.organization_id)
            if request.user.organization==obj.organization or obj.organization.Name in following or obj.organization.Name in organizationfollowing :
                return True
            else :
                self.message=f'you must belong to or follow the organization {obj.blog.organization.Name} to read a blog '
                return False
            
        elif self.obj.organization.type=='Pub':
            return True

class blog_update_destroy_permission(BasePermission):
    def has_object_permission(self, request, view, obj):
        if obj.organization_id==request.user.organization_id or obj.organization.founder_id==request.user.id:
            return True
        self.message='you donot have the permission to update or destroy the blog as you are not owner of blog or founder of the organization the blog belong to.'
        return False
        