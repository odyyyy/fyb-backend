from datetime import timedelta, datetime

from celery import shared_task, Celery
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import send_mail

app = Celery()


@shared_task
def send_welcome_email(user_id):
    user = get_user_model().objects.get(id=user_id)
    send_mail(
        subject='Welcome',
        message=f'Добро пожаловать, {user.email}',
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[user.email, ],
    )


@app.task
def send_email_if_user_inactive_for_year():
    inactive_users = get_user_model().objects.filter(is_active=True,
                                                     date_joined__lt=datetime.now() - timedelta(days=365))

    send_mail(
        subject='Inactive users',
        message=f'Your account will be blocked if you are inactive for 1 year',
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[user.email for user in inactive_users]
    )

