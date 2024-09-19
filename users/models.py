import enum

from django.contrib.auth.models import AbstractUser
from django.db import models

from users.tasks import send_welcome_email


class User(AbstractUser):
    email = models.EmailField(unique=True, verbose_name="Электронная почта")
    image = models.ImageField(upload_to='media/photos/users/%Y/%m/%d/', blank=True, null=True, verbose_name="Фото")

    def save(self, *args, **kwargs):
        send_welcome_email.delay(self.username)
        super().save(*args, **kwargs)
