from django.contrib.auth import get_user_model
from django.db import models

class Band(models.Model):
    name = models.CharField(max_length=50, unique=True, db_index=True, verbose_name="Название")
    members = models.ManyToManyField(get_user_model(), related_name='band_members', verbose_name="Участники")
    leader = models.OneToOneField(get_user_model(), on_delete=models.CASCADE, related_name='band_leader',
                                  verbose_name="Лидер")
    city = models.CharField(max_length=50, verbose_name="Город")
    image = models.ImageField(upload_to='media/photos/bands/%Y/%m/%d/', blank=True, null=True, verbose_name="Фото")

    class Meta:
        verbose_name = "Музыкальная группа"
        verbose_name_plural = "Музыкальные группы"


    def __str__(self):
        return self.name
