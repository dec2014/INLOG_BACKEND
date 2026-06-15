from .models import PinBlog
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from django.db import transaction

def pin_by_user(user,blog):
    return PinBlog.objects.filter(pin_by_id=user,blog_id=blog,pin=True).exists()

def blog_pin_create_update(blog,user):
    if user.role=='F':
        obj_pin,created=PinBlog.objects.update_or_create(
            blog=blog,
            pin_by=user
        )
        if not created:
            obj_pin.pin= not obj_pin.pin
            obj_pin.founder_pin=not obj_pin.founder_pin
            obj_pin.save()
        else:
            obj_pin.founder_pin=True
    else:
        obj_pin,created=PinBlog.objects.update_or_create(
            blog=blog,
            pin_by=user
        )
        if not created:
            obj_pin.pin= not obj_pin.pin
            obj_pin.save()

    return obj_pin,created

@transaction.atomic
def pin_blog(self,request,*args,**kwargs):
    try:
        obj_pin,created=blog_pin_create_update(self.blog,request.user)


        return Response({'pin':obj_pin.pin,'created':created})
    except Exception as e:
        raise ValidationError({
            'error':'could not pin the blog',
            'details':str(e)
        })