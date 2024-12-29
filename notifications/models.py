from django.contrib.auth import get_user_model
from django.db import models


class NotificationSubscription(models.Model):
    NOTIFICATION_TYPES = [
        ('MusicianVacancy', 'Вакансии музыкантов'),
        ('BandVacancy', 'Вакансии групп'),
        ('OrganizerVacancy', 'Вакансии организаторов'),
        ('Messages', 'Сообщения'),
        ('News', 'Новости'),
    ]

    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, verbose_name="Пользователь")
    notification_type = models.CharField(max_length=50, choices=NOTIFICATION_TYPES, verbose_name='Тип уведомления')

    class Meta:
        unique_together = ('user', 'notification_type')
        verbose_name = 'Подписка на уведомления'
        verbose_name_plural = 'Подписки на уведомления'

    def __str__(self):
        return f'{self.user} - {self.notification_type}'
