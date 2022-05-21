from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
# Create your models here.

# funcion que genera token
# @receiver(post_save, sender=settings.AUTH_USER_MODEL)
# def create_auth_token(sender, instance=None, created=False, **kwargs):
#     if created:
#         Token.objects.create(user=instance)

class MyAccountManager(BaseUserManager):
    def create_user(self, name, username, email, password=None):
        if not email:
            raise ValueError('El usuario debe tener email.')
        
        if not username:
            raise ValueError('El usuario debe tener username.')
        
        user = self.model(
            email = self.normalize_email(email),
            username = username,
            name = name,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, name, username, email, password):
        user = self.create_user(
            email = self.normalize_email(email),
            username = username,
            password = password,
            name = name,
        )
        
        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superadmin = True
        user.save(using=self._db)
        return user


class Account(AbstractBaseUser):
    name = models.CharField(max_length=50)
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    
    date_joined = models.DateTimeField(auto_now_add=True)
    last_join = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superadmin = models.BooleanField(default=False)
    
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'name']
    
    objects = MyAccountManager()
    
    def __str__(self):
        return self.name
    
    def has_perm(self, perm, obj=None):
        return self.is_admin
    
    def has_module_perms(self, add_label):
        return True