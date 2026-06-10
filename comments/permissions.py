from rest_framework.permissions import BasePermission



class Comments_update_permission(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.id==obj.owner_id or obj.blog.organization.founder_id==request.user.id:
            return True
        else:
            self.message='you must be the creater of the comment or be the founder of organization the creater belongs to,to update the comment'
            return False

