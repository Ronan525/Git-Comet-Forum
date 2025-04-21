from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.


class Bio(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    updated_on = models.DateTimeField(auto_now=True)
    content = models.TextField()

    def __str__(self):
        return self.title


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.URLField(
        max_length=200,
        default='/static/images/default-profile.png'
    )

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_user_bio(sender, instance, created, **kwargs):
    if created:
        Bio.objects.create(user=instance)
