from django.core.mail import send_mail
from django.conf import settings
import random
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from rest_framework.exceptions import ValidationError

def EmailVerification(request,email,user):
    try:
        uuid=urlsafe_base64_encode(force_bytes(user.pk))
        token =default_token_generator.make_token(user)
        link = request.build_absolute_uri(
        f"/verify/{uuid}/{token}/"
    )
        subject='verification mail'
        body=f'your link is {link}'
        email_from=settings.EMAIL_HOST_USER
        reciptent_list=[email]
    
        send_mail(subject,body,email_from,reciptent_list)
    except Exception as e:
        raise ValidationError(f'the email could not be sent.{str(e)}')




def TempEmployeeCredentials(email,password):
    try:
        subject='Login credentials'
        body=f'your credentials are email:{email},password:{password}'
        email_from=settings.EMAIL_HOST_USER
        reciptent_list=[email]
    
        send_mail(subject,body,email_from,reciptent_list)
    except Exception as e:
        raise ValidationError(f'the email could not be sent.{str(e)}')

