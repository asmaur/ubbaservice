from typing import Any
from django.db import models
from django.contrib.auth.models import (AbstractBaseUser,
                                        PermissionsMixin,
                                        UserManager)
from django.utils import timezone
import uuid

# Create your models here.


class CustomUserManager(UserManager):

    def _create_user(self, name, email, password, **extra_fields):
        if not email:
            raise ValueError("You have not provided a valid email")
        email = self.normalize_email(email)
        user = self.model(email=email, name=name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_user(self, name: str, email: str | None = ...,
                    password: str | None = ..., **extra_fields: Any) -> Any:
        return super()._create_user(name, email, password, **extra_fields)

    def create_superuser(self, name: str, email: str | None,
                         password: str | None, **extra_fields: Any) -> Any:
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self._create_user(name, email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    AGENT = 'agent'
    USER = 'user'
    MANAGER = 'manager'
    PETSITTER = 'petsitter'
    VETERINARIAN = 'veterinarian'
    
    GOOGLE_AUTH = "google",
    FACEBOOK_AUTH = "facebook",
    TWITTER_AUTH = "twiter",
    EMAIL_AUTH = "email",
    TIKTOK_AUTH = "tiktok",
    APPLE_AUTH = "apple",
    

    ROLES_CHOICES = (
        (AGENT, 'Agent'),
        (USER, 'User'),
        (MANAGER, 'Manager'),
        (PETSITTER, 'Petsitter'),
        (VETERINARIAN, 'Veterinarian')
    )
    AUTH_PROVIDERS = (
        (GOOGLE_AUTH, "Google"),
        (FACEBOOK_AUTH, "Facebook"),
        (TWITTER_AUTH, "Twitter"),
        (EMAIL_AUTH, "Email"),
        (TIKTOK_AUTH, "Tiktok"),
        (APPLE_AUTH, "Apple"),
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=255, blank=True, default='')
    role = models.CharField(max_length=20,
                            choices=ROLES_CHOICES,
                            default=USER)
    auth_provider = models.CharField(max_length=50, default=EMAIL_AUTH)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    joined_date = models.DateTimeField(default=timezone.now)
    last_login = models.DateTimeField(blank=True, null=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['name']
