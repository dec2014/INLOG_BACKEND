from rest_framework.permissions import BasePermission
from .service import user_following_list_exists,organization_following_list_exists


class followPermissions(BasePermission):
    def has_object_permission(self, request, view, obj):
        user=request.user
        following_exists=user_following_list_exists(user.id,obj.id)

        if following_exists:
            self.message('you are already following the organization.')
            return False
            
        if obj.id==user.organization_id:
            self.message('you can not follow your own organization')
            return False
        
        if user.role=='F':
            return True
            
            

        elif user.role=='E':

            organizationfollowing_exists=organization_following_list_exists(user.organization_id,obj.id)
            if organizationfollowing_exists:
                self.message(f'the organization you belong to ,already follows the organization {obj.Name}')
                return False
            
            return True



class unfollowPermissions(BasePermission):
    def has_object_permission(self, request, view, obj):
        user=request.user
        following_exists=user_following_list_exists(user.id,obj.id)

        if not following_exists:
            self.message('you are not following the organization already.')
            return False
        
        if obj.id==user.organization_id:
            self.message('you can not follow your own organization')
            return False
      
        if user.role=='F':
            return True
            
        elif user.role=='E':
            organizationfollowing_exists=organization_following_list_exists(user.organization_id,obj.id)
            if organizationfollowing_exists:
                self.message(f'you cannot unfollow the organization {obj.Name} as you are not the founder of your organization')
                return False
            
            return True
