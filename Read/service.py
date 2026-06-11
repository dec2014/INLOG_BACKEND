from .models import BlogRead
from rest_framework.exceptions import ValidationError
from django.db import IntegrityError

def all_read_organization(id):
    return BlogRead.objects.select_related('blog').filter(blog__organization_id=id).count()

def all_read_user(id):
    return BlogRead.objects.filter(read_by_id=id).count()

def get_or_create_blogread(blog,user):
    try:
        return BlogRead.objects.get_or_create(blog=blog,read_by=user)

    except IntegrityError as e:
        raise ValidationError('could not mark the blog as read')