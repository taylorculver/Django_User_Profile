from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.exceptions import ValidationError


# Create your models here.
def min_length_validator(value):
    if len(value) < 10:
        raise ValidationError(
            message='Your Bio must be more than 10 characters!',
            params={'value': value},
        )


class Profile(models.Model):
    username = models.OneToOneField(User, on_delete=models.CASCADE)
    DOB = models.DateField(null=True, blank=True)
    bio = models.TextField(validators=[min_length_validator])
    avatar = models.ImageField(upload_to='avatars/')

    def __str__(self):
        return str(self.username)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(username=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
