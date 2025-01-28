from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Bio(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, default=1)
    title = models.CharField(max_length=200)
    updated_on = models.DateTimeField(auto_now=True)
    content = models.TextField()

    def __str__(self):
        return self.title

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.URLField(max_length=200, default='/static/images/default-profile.png')

    def __str__(self):
        return self.user.username