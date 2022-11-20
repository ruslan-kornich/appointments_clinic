import jwt
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.models import User
from django.shortcuts import render
from rest_framework import status, viewsets
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from accounts.send_mails import send_activation_mail, send_random_password_mail
from .serializers import (LoginSerializer,
                          RegisterSerializer)


class LoginViewSet(viewsets.ModelViewSet, TokenObtainPairSerializer):
    serializer_class = LoginSerializer
    permission_classes = [
        AllowAny,
    ]
    http_method_names = ["post"]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])
        return Response(serializer.validated_data, status=status.HTTP_200_OK)


class RegistrationViewSet(viewsets.ModelViewSet, TokenObtainPairView):
    serializer_class = RegisterSerializer
    permission_classes = [
        AllowAny,
    ]
    http_method_names = ["post"]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save(is_active=False)
        password = User.objects.make_random_password()
        user.set_password(password)
        user.save()
        user_data = serializer.data
        user_data["password"] = password
        send_activation_mail(user_data, request)
        send_random_password_mail(user_data, user_data["password"], request)
        refresh = RefreshToken.for_user(user)
        res = {"refresh": str(refresh), "access": str(refresh.access_token)}
        return Response(
            {
                "user": serializer.data,
                "refresh": res["refresh"],
                "token": res["access"],
            },
            status=status.HTTP_201_CREATED,
        )


def verify_email(request):
    token = request.GET.get("token")
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms="HS256")
        user = User.objects.get(id=payload["user_id"])
        if not user.is_active:
            user.is_active = True
            user.save()
            messages.success(request, "Account was Successfully Verified.")
        else:
            messages.info(
                request,
                """Your Account has already been activated.
                          You can now login and
                          book an appointment today.
                        """,
            )
    except jwt.ExpiredSignatureError as identifier:
        messages.warning(request, "The Activation Link Expired!")
    except jwt.exceptions.DecodeError as identifier:
        messages.warning(request, "Invalid Activation Link!")
    context = {}
    return render(request, "accounts/verify.html", context)


class RefreshViewSet(viewsets.ViewSet, TokenRefreshView):
    permission_classes = (AllowAny,)
    http_method_names = ["post"]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])

        return Response(serializer.validated_data, status=status.HTTP_200_OK)
