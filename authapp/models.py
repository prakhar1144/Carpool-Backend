from django.db import models
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import  PermissionsMixin
# from django.core.validators import MinLengthValidator

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None):
        if email is None:
            raise ValueError("Email is required")
        if password is None:
            raise ValueError("Password is required")

        user = self.model(email=self.normalize_email(email))
        user.set_password(password)
        user.save()

        return user
    
    def create_superuser(self, email, password=None):
        user = self.create_user(email=email, password=password)
        user.is_staff = True
        user.is_superuser = True
        user.save()

        return user
        

class User(AbstractBaseUser, PermissionsMixin):
    # username = models.CharField(max_length=12, unique=True, db_index=True, validators=[MinLengthValidator(3,"Minimum Lenth should be 3")])
    email = models.EmailField(unique=True)
    is_verified = models.BooleanField(default=False)

    # Fields used by the Django admin.
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'

    objects = CustomUserManager()

    def get_token(self):
        refresh = RefreshToken.for_user(self)
        return {'refresh': str(refresh), 'access': str(refresh.access_token)}