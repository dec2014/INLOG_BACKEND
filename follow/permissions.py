from rest_framework.permissions import BasePermission
from .service import get_user_following_list,get_organization_following_list


class followPermissions(BasePermission):
    def has_object_permission(self, request, view, obj):
        user=request.user
        following=get_user_following_list(user.id)

        if obj.Name in following:
            self.message('you are already following the organization.')
            return False
            
        if obj.id==user.organization_id:
            self.message('you can not follow your own organization')
            return False
        
        if user.role=='F':
            return True
            
            

        elif user.role=='E':

            organizationfollowing=get_organization_following_list(user.organization_id)
            if obj.Name in organizationfollowing:
                self.message(f'the organization you belong to ,already follows the organization {obj.Name}')
                return False
            
            return True



class unfollowPermissions(BasePermission):
    def has_object_permission(self, request, view, obj):
        user=request.user
        following=get_user_following_list(user.id)

        if obj.Name not in following:
            self.message('you are not following the organization already.')
            return False
        
        if obj.id==user.organization_id:
            self.message('you can not follow your own organization')
            return False
      
        if user.role=='F':
            return True
            
        elif user.role=='E':
            organizationfollowing=get_organization_following_list(user)
            if obj.Name in organizationfollowing:
                self.message(f'you cannot unfollow the organization {obj.Name} as you are not the founder of your organization')
                return False
            
            return True
