import uuid
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.http import Http404

# Create your models here.

class UserManager(BaseUserManager):
    def get_object_by_public_id(self,public_id):
        try:
            return self.get(public_id=public_id)
        except (ObjectDoesNotExist, ValueError, TypeError):
            raise Http404
    
    def create_user(self, username, email, password=None, **kwargs):
        if username is None:
            raise TypeError("username must not be empty")
        if email is None:
            raise TypeError("email must not be empty")
        if password is None:
            raise TypeError("password must not be empty")
        user = self.model(
            username = username, 
            email = self.normalize_email(email), 
            **kwargs)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, username, email, password=None, **kwargs):
        if username is None:
            raise TypeError("username must not be empty")
        if email is None:
            raise TypeError("email must not be empty")
        if password is None:
            raise TypeError("password must not be empty")
        user = self.create_user(username, email, password, **kwargs)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user



class User(AbstractBaseUser, PermissionsMixin):
    public_id = models.UUIDField(
        db_index=True,
        unique=True,
        editable=False,
        default=uuid.uuid4
    )
    username = models.CharField(
        max_length=100,
        unique=True,
        db_index=True
    )
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(db_index=True, unique=True)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()

    def __str__(self) -> str:
        return f'{self.email}'

    @property
    def name(self):
        return f'{self.first_name} {self.last_name}'