import uuid
import os 

from django.db import models
from django.contrib.auth.models import AbstractBaseUser,\
    BaseUserManager, PermissionsMixin

from django.conf import settings


def recipe_image_file_path(instance, filename):
    """Generate file path for new recipe image"""
    # return the extention of image
    ext = filename.split('.')[-1]
    filename = f'{uuid.uuid4()}.{ext}'

    return os.path.join('uploads/recipe/', filename)


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


class Ingredient(models.Model):
    """Ingredient to be use in recipe"""
    name = models.CharField(max_length=200)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.name

        
class Recipe(models.Model):
    """Recipe object"""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    title = models.CharField(max_length=255)
    time_minutes = models.IntegerField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    # in this charfield you can a singed to be null but tis isn't recommended 
    # because then multiple state then you need to check for link that it has a valueset 
    # or not. if you wanna make it optional i recommended using 'blank=True' 
    # because if you create a new object if you omits the link, then it's simply said 
    # blank string in all cases. the benifate of this is if you wanna check if there a link set 
    # you simply check whether the link is blank or not.
    # if you allow this to be null filed then you also have to check if the link is 'nun blank or has a value'
    link = models.CharField(max_length=255, blank=True)
    ingredients = models.ManyToManyField('Ingredient')
    tags = models.ManyToManyField('Tag')
    # i don't wanna call the recipe_image_file_path because we just wanna pass a refrance to the function
    # so it can be called every time we upload and it's gonna called in the background by django
    # imaged filed feature.
    image = models.ImageField(null=True, upload_to=recipe_image_file_path)

    def __str__(self):
        return self.title