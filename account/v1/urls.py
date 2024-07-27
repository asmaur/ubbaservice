from django.urls import path
from .views import CreateAccount


app_name = 'users'

urlpatterns = [
    path('register/', CreateAccount.as_view(), name="create_user"),
]
