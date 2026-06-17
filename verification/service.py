from django.core.mail import send_mail
from django.conf import settings
import random
import os
import requests
import mailtrap as mt
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from rest_framework.exceptions import ValidationError
import json


def EmailVerification(request,email,user):
    try:
        uuid=urlsafe_base64_encode(force_bytes(user.pk))
        token =default_token_generator.make_token(user)
        link = request.build_absolute_uri(
        f"/verify/{uuid}/{token}/"
    )
        subject='verification mail'
        body=f'your link is {link}'
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [email]   
        try:
            url='https://email-microservice-flame.vercel.app/send-mail/'
            data={
                'subject':subject,
                'body':body,
                'email_from':email_from,
                'recipient_list':recipient_list
            }
            data_json=json.dumps(data)
            status=requests.post(url,data=data_json)
            print(status)
        except Exception as e:
            raise ValidationError(f'the microservice for email is not workning.{str(e)}')
    except Exception as e:
        raise ValidationError(f'the email could not be sent.{str(e)}')




def TempEmployeeCredentials(email,password):
    try:
        subject='Login credentials'
        body=f'your credentials are email:{email},password:{password}'
        email_from=settings.DEFAULT_FROM_EMAIL
        reciptent_list=[email]
        try:
            url='https://email-microservice-flame.vercel.app/mail-employee-details/'
            data={
                'subject':subject,
                'body':body,
                'email_from':email_from,
                'recipient_list':reciptent_list
            }
            data_json=json.dumps(data)
            status=requests.post(url,data=data_json)
            print(status)
        except Exception as e:
            raise ValidationError(f'the microservice for email is not workning.{str(e)}')
    except Exception as e:
        raise ValidationError(f'the email could not be sent.{str(e)}')

