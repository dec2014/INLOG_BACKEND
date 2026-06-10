from .models import BlogRead
from rest_framework.exceptions import ValidationError
from django.db import IntegrityError

def get_or_create_blogread(blog,user):
    try:
        return BlogRead.objects.get_or_create(blog=blog,read_by=user)

    except IntegrityError as e:
        raise ValidationError('could not mark the blog as read')