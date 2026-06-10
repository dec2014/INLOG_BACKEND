from rest_framework.permissions import BasePermission
from follow.service import user_following_list_exists,organization_following_list_exists

class Comment_access_permission(BasePermission):
    def has_object_permission(self, request, view, obj):
        if obj.blog.organization.type=='Pvt':
            following_exists=user_following_list_exists(request.user.id,obj.blog.organization_id)
            organizationfollowing_exists=organization_following_list_exists(request.user.organization_id, obj.blog.organization_id)
            if request.user.organization==obj.organization or following_exists or organizationfollowing_exists :
                return True
            else :
                self.message=f'you must belong to or follow the organization {obj.blog.organization.Name} to read a blog '
                return False
            
        elif obj.organization.type=='Pub':
            return True

class Comments_update_permission(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.id==obj.owner_id or obj.blog.organization.founder_id==request.user.id:
            return True
        else:
            self.message='you must be the creater of the comment or be the founder of organization the creater belongs to,to update the comment'
            return False

