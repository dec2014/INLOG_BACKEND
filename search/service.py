from follow.service import get_organization_following_list,get_user_following_list
from django.db.models import Q,F
from BLOG.service import search_blogs
def filter_blog(self):
    following=get_user_following_list(self.request.user.id)
    organizationfollowing=get_organization_following_list(self.request.user.organization_id)
    search=self.request.query_params.get('search',None)
    return search_blogs(self,search,organizationfollowing,following)
    