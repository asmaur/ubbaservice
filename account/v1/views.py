import traceback
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.views import APIView
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.permissions import AllowAny
from account.v1.serializers import UserSerializer
from .serializers import RegistrationSerializer
from rest_framework import permissions
import re
# from drf_with_firebase.settings import auth
from django.contrib.auth.hashers import check_password
from ..firebase_auth import FirebaseAuthentication
from ..models import User
# from .firebase_auth.firebase_authentication import auth as firebase_admin_auth
# from .utils.custom_email_verification_link import (
#     generate_custom_email_from_firebase
# )


class CreateAccount(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        try:
            reg_serializer = RegistrationSerializer(data=request.data)
            if reg_serializer.is_valid():
                new_user = reg_serializer.save()
                if new_user:
                    return Response(status=status.HTTP_201_CREATED)
        except Exception:
            return Response()


class LoginOrCreateAccount(APIView):

    def post(self, request):
        serializer = None
        try:
            data = request.data
            if data is None:
                raise Exception
            if data.get("uid", None) is None:
                raise Exception

            serializer = UserSerializer(
                data={
                    "uid": data.get("uid"),
                    "name": data.get("name"),
                    "email": data.get("email"),
                    # "role": data.get("role", "user"),
                    # "auth_provider": data.get("providerId")
                }
            )
            if serializer.is_valid(raise_exception=True):
                serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        except Exception as e:
            traceback.print_exception(e)
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class SocialLogin(APIView):
    permission_classes = [FirebaseAuthentication]

    def get(self, request):
        return Response(status=status.HTTP_200_OK)


# class AuthCreateNewUserView(APIView):
#     permission_classes = [AllowAny]
#     authentication_classes = []

#     @swagger_auto_schema(
#         operation_summary="Create a new user",
#         operation_description="Create a new user by \
#             providing the required fields.",
#         tags=["User Management"],
#         request_body=UserSerializer,
#         responses={
#             201: UserSerializer(many=False),
#             400: "User creation failed."}
#     )
#     def post(self, request, format=None):
#         data = request.data
#         email = data.get('email')
#         password = data.get('password')
#         first_name = data.get('first_name')
#         last_name = data.get('last_name')
#         name = f"{first_name} {last_name}"
#         included_fields = [email, password, name, first_name, last_name]
#         # Check if any of the required fields are missing
#         if not all(included_fields):
#             bad_response = {
#                 'status': 'failed',
#                 'message': 'All fields are required.'
#             }
#         return Response(bad_response, status=status.HTTP_400_BAD_REQUEST)
#         # Check if email is valid
#         if email and not re.match(r'[^@]+@[^@]+\.[^@]+', email):
#             bad_response = {
#                 'status': 'failed',
#                 'message': 'Enter a valid email address.'
#             }
#         return Response(bad_response, status=status.HTTP_400_BAD_REQUEST)
#         # Check if password is less than 8 characters
#         if len(password) < 8:
#             bad_response = {
#                 'status': 'failed',
#                 'message': 'Password must be at least 8 characters long.'
#             }
#             return Response(bad_response, status=status.HTTP_400_BAD_REQUEST)
#         # Check if password contains at least one uppercase
#         # letter, one lowercase letter, one digit, and one special character
#         if password and not re.match(r"^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[!@#$%^&*()_+{}\[\]:;<>,.?~\\-]).{8,}$", password):
#             bad_response = {
#                 "status": "failed",
#                 "message": "Password must contain at least one \
#                     uppercase letter, one lowercase letter, \
#                         one digit, and one special character."}
#             return Response(bad_response, status=status.HTTP_400_BAD_REQUEST)
#         try:
#             # create user on firebase
#             user = auth.create_user_with_email_and_password(email, password)
#             # create user on django database
#             uid = user['localId']
#             data['firebase_uid'] = uid
#             data['is_active'] = True
#         # sending custom email verification link
#             try:
#                 user_email = email
#                 display_name = first_name.capitalize()
#                 generate_custom_email_from_firebase(user_email, display_name)
#             except Exception as e:
#                 # delete user from firebase if email 
#                 # verification link could not be sent
#                 firebase_admin_auth.delete_user(uid)
#                 bad_response = {
#                     "status": "failed",
#                     "message": str(e)
#                 }
#                 return Response(
#                     bad_response,
#                     status=status.HTTP_400_BAD_REQUEST)

#             serializer = UserSerializer(data=data)
#             if serializer.is_valid():
#                 serializer.save()
#                 response = {
#                     "status": "success",
#                     "message": "User created successfully.",
#                     "data": serializer.data
#                 }
#                 return Response(response, status=status.HTTP_201_CREATED)
#             else:
#                 auth.delete_user_account(user["idToken"])
#                 bad_response = {
#                     "status": "failed",
#                     "message": "User signup failed.",
#                     "data": serializer.errors
#                 }
#                 return Response(
#                     bad_response,
#                     status=status.HTTP_400_BAD_REQUEST)
#         except Exception:
#             bad_response = {
#                 "status": "failed",
#                 "message": "User with this email already exists."
#             }
#             return Response(bad_response, status=status.HTTP_400_BAD_REQUEST)


# class AuthLoginExisitingUserView(APIView):
#     permission_classes = [AllowAny]
#     authentication_classes = []

#     @swagger_auto_schema(
#         operation_summary="Login an existing user",
#         operation_description="Login an existing user \
#         by providing the required fields.",
#         tags=["User Management"],
#         request_body=openapi.Schema(
#             type=openapi.TYPE_OBJECT,
#             properties={
#                 "email": openapi.Schema(
#                     type=openapi.TYPE_STRING,
#                     description="Email of the user"),
#                 "password": openapi.Schema(
#                     type=openapi.TYPE_STRING,
#                     description="Password of the user")
#             }
#         ),
#         responses={
#             200: UserSerializer(many=False),
#             404: "User does not exist."}
#     )
#     def post(self, request: Request):
#         data = request.data
#         email = data.get("email")
#         password = data.get("password")
#         try:
#             user = auth.sign_in_with_email_and_password(email, password)
#         except Exception:
#             bad_response = {
#                 "status": "failed",
#                 "message": "Invalid email or password."
#             }
#             return Response(bad_response, status=status.HTTP_400_BAD_REQUEST)

#         try:
#             existing_user = User.objects.get(email=email)
#             # update password if it is not the same as the one in the database
#             if not check_password(password, existing_user.password):
#                 existing_user.set_password(password)
#                 existing_user.save()
#                 serializer = UserSerializer(existing_user)
#                 extra_data = {
#                     "firebase_id": user["localId"],
#                     "firebase_access_token": user["idToken"],
#                     "firebase_refresh_token": user["refreshToken"],
#                     "firebase_expires_in": user["expiresIn"],
#                     "firebase_kind": user["kind"],
#                     "user_data": serializer.data
#                 }
#             response = {
#                 "status": "success",
#                 "message": "User logged in successfully.",
#                 "data": extra_data
#             }
#             return Response(response, status=status.HTTP_200_OK)
#         except User.DoesNotExist:
#             auth.delete_user_account(user["idToken"])
#             bad_response = {
#                 "status": "failed",
#                 "message": "User does not exist."
#             }
#             return Response(bad_response, status=status.HTTP_404_NOT_FOUND)

class UserViewset(viewsets.ViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly, UpdateOwnPet]
    # authentication_classes = [FirebaseAuthentication]
    # parser_classes = [MultiPartParser, JSONParser]

    
