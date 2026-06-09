from .models import Blog
from rest_framework.exceptions import ValidationError
from django.db import IntegrityError


def get_blog__organization(id):
    try:
        blog= Blog.objects.select_related('organization').get(id=id)
        return blog
    except IntegrityError as e:
        raise ValidationError({
            'error':'blog could not be found',
            'detail':str(e)
        })