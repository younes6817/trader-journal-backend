from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.validators import RegexValidator
from django.db import models


class UserManager(BaseUserManager):

    def _create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email is required")

        user = self.model(
            username=email,
            email=self.normalize_email(email),
            **extra_fields
        )

        if password:
            user.set_password(password)

        user.save(using=self._db)
        return user


    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)

        return self._create_user(
            email,
            password,
            **extra_fields
        )


    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        return self._create_user(
            email,
            password,
            **extra_fields
        )


class User(AbstractUser):
    image_profile = models.ImageField()
    phone = models.CharField(
        max_length=11,
        unique=True,
        validators=[
            RegexValidator(
                regex=r'09\d{9}$'
            )
        ]
    )
    USERNAME_FIELD = "email"
    objects = UserManager()