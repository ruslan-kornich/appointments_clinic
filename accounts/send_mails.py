import datetime

from django.contrib.auth.models import User
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.utils.encoding import smart_bytes
from django.utils.http import urlsafe_base64_encode
from rest_framework.reverse import reverse
from rest_framework_simplejwt.tokens import RefreshToken


def send_activation_mail(user_data, request):
    user = User.objects.get(email=user_data['email'])
    current_site = get_current_site(request).domain
    mail_subject = "Verify Your Account."
    to_mail = user.email
    token = RefreshToken.for_user(user).access_token
    relative_link = reverse('api:email-verify')
    absolute_url = "http://" + current_site + relative_link + "?token=" + str(token)
    message = f"""
Welcome to our Clinic,

Hi {user.username},
Click on the link below to verify your account,
{absolute_url}

This is an automatically generated email. Please do not reply.
@{datetime.date.today()}
    """
    email = EmailMessage(
        subject=mail_subject,
        body=message,
        to=[to_mail]
    )
    email.send()


def send_random_password_mail(user, password, request):
    to_mail = user["email"]
    current_site = get_current_site(request).domain
    mail_subject = "Account Random Password"

    message = f"""
Hello {user["first_name"]} {user["last_name"]},

Your registration was successful, Credentials
are as follows:
User: {user["username"]}
Password: {password}

Kindly, activate your account and reset your password.

Thank you!
    """
    email = EmailMessage(
        subject=mail_subject,
        body=message,
        to=[to_mail]
    )
    email.send()


