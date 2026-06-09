from rest_framework.permissions import BasePermission
from follow.permissions import get_organization_following_list,get_user_following_list


class Comments_update_permission(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.id==obj.owner_id or obj.blog.organization.founder_id==request.user.id:
            return True
        else:
            self.message='you must be the creater of the comment or be the founder of organization the creater belongs to,to update the comment'
            return False

class comment_access_permission(BasePermission):
    def has_object_permission(self, request, view, obj):
        if obj.blog.organization.type=='Pvt':
            following=get_user_following_list(request.user)
            organizationfollowing=get_organization_following_list(request.user)
            if request.user.organization==self.obj.organization or self.obj.organization.Name in following or self.obj.organization.Name in organizationfollowing :
                return True
            else :
                self.message=f'you must belong to or follow the organization {obj.blog.organization.Name} to comment on it'
            
        elif self.obj.organization.type=='Pub':
            return True