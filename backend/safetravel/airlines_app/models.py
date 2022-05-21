from django.db import models
from django.contrib.auth.models import User
from user_app.models import Account

# Create your models here.

class Airline(models.Model):
    code = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    description = models.TextField(max_length=255)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    soft_deleted = models.BooleanField(default=False)
    
    def __str__(self):
        return self.title
    

class Plane(models.Model):
    airline = models.ForeignKey(Airline, on_delete=models.CASCADE, related_name="Has_Plane")
    code = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    description = models.TextField(max_length=255)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    soft_deleted = models.BooleanField(default=False)
    
    def __str__(self):
        return self.code
    
    
class Pilot(models.Model):
    plane = models.ForeignKey(Plane, on_delete=models.CASCADE, related_name="Has_Pilot")
    code = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    description = models.TextField(max_length=255)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    soft_deleted = models.BooleanField(default=False)
    
    def __str__(self):
        return self.title