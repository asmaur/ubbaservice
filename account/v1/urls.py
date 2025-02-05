from django.urls import path
from rest_framework.routers import SimpleRouter
from .views import (
    # CreateAccount,
    SocialLogin,
    LoginOrCreateAccount,
    UserViewset
    # AuthCreateNewUserView,
    # AuthLoginExisitingUserView,
)


app_name = 'users'

router = SimpleRouter()

router.register('users', UserViewset)

urlpatterns = [
    path(
        'users/register/',
        LoginOrCreateAccount.as_view(),
        name="login_create_user"
    ),
    path(
        'users/social_login/',
        SocialLogin.as_view(),
        name="user_social_login"
    ),
    # path('auth/sign-up/', AuthCreateNewUserView.as_view(), name="auth-create-user"),
    # path('auth/sign-in/', AuthLoginExisitingUserView.as_view(), name="auth-login-user"),
]
