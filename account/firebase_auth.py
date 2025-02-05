from django.db import IntegrityError
from rest_framework import authentication
from .firebase_exceptions import (
    NoAuthToken,
    FirebaseError,
    InvalidAuthToken,
    EmailVerification
)
from firebase_admin import auth
from account.models import User


class FirebaseAuthentication(authentication.BasicAuthentication):
    keyword = "Bearer"

    def authenticate(self, request):
        auth_header = request.META.get('HTTP_AUTHORIZATION')
        if not auth_header:
            raise NoAuthToken("No user found.")
        id_token = auth_header.split(" ").pop()
        decoded_token = None
        try:
            decoded_token = auth.verify_id_token(id_token)
        except Exception:
            raise InvalidAuthToken("Invalid token provided")
        if not id_token or not decoded_token:
            return None
        # email_verified = decoded_token.get("email_verified")
        # if not email_verified:
        #     raise EmailVerification(
        #         "Email not verified. Please verify your email"
        #     )
        try:
            uid = decoded_token.get("uid")
        except Exception:
            raise FirebaseError(
                "Unregistered user. Register to create a new account"
            )
        try:
            user, _ = User.objects.get_or_create(
                uid=uid,
                email=decoded_token.get("email"),
                # name=decoded_token.get("name")
            )
        except IntegrityError as e:
            raise FirebaseError(f"Error creating or accessing user data: {e}")
        except Exception as e:
            raise FirebaseError(f"Error accessing user data: {e}")
        return user, None
