from django.db import models
# from django.contrib.auth.models import User

from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
     
    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(max_length=50)
  



class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    auth_token = models.CharField(max_length=100)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username
    
