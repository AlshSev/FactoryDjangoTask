from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import uuid

class Message(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.body

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    token = models.TextField()
    telegram_id = models.TextField()

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance, token=uuid.uuid4())

@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()