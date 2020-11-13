from django.db import models
from django.contrib.auth.models import AbstractBaseUser,\
    BaseUserManager, PermissionsMixin

from django.conf import settings


class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a new User"""
        if not email:
            raise ValueError("you must have an email address!!!")
        # normalize is a helper function that come with the base user managere 
        user = self.model(email = self.normalize_email(email), **extra_fields)
        user.set_password(password)
        # useign=self._db ----> it's just required for supporting multipale databases, 
        # but in here it's not 
        # not our concern but it's good practice to keep it. 
        user.save(using=self._db)
        
        return user

    def create_superuser(self,email, password):
        user = self.create_user(email, password)
        user.is_staff= True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    """Custome User model that support email instead of username"""
    email = models.EmailField(max_length=255, unique=True)
    name  = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    is_staff  = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'


class Tag(models.Model):
    """Tag to be used for a recipe"""
    name = models.CharField(max_length=255)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.name
