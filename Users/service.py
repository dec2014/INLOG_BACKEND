from .models import employees
from rest_framework.exceptions import ValidationError
from django.db import IntegrityError

def current_user_logined(id):
    try:
        current_user=employees.objects.select_related('organization').get(pk=id)
        return current_user
    except IntegrityError as e:
        raise ValidationError('cannot find the user')
    