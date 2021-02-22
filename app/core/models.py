from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


class UserManager(BaseUserManager):  # This is the manager class that manager creation of user models

    def create_user(self, email, password=None, **extra_fields):
        '''Creates and saves a new user'''
        if not email:
            raise ValueError('users must have an email address')
        user = self.model(email=self.normalize_email(email), **extra_fields)  # This creates a new usermodel
        user.set_password(password)  # This creates the password
        user.save(using=self._db)  # This saves the model

        return user  # This returns the new user that has just been created

    def create_superuser(self, email, password):
        """Creates and saves a new superuser"""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    '''Custom usermodel that supports using email instead of username'''
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
