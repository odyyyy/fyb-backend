from datetime import timedelta, datetime

from celery import shared_task
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.db.models import QuerySet


@shared_task(bind=True, max_retries=3)
def send_welcome_email(self, user_nickname):
    try:
        send_mail(
            subject='Welcome',
            message=f'Welcome to our website, {user_nickname}',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user_nickname, ],
            fail_silently=False
        )
    except Exception as e:
        raise self.retry(exc=e, countdown=60)


@shared_task
def send_daily_email_if_user_inactive_for_year():
    inactive_users = get_user_model().objects.filter(last_login__lte=datetime.now() - timedelta(days=365))
    print(inactive_users)
    print(datetime.now() - timedelta(days=365))
    print(datetime.now() - timedelta(days=365) < datetime.now())
    if inactive_users.exists():
        send_mail(
            subject='Inactive users',
            message='Your account will be blocked if you will not log in next 3 months',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user.email for user in inactive_users]
        )


@shared_task
def delete_account_if_user_inactive_long_time():
    users_to_delete: QuerySet = get_user_model().objects.filter(last_login__lte=datetime.now() -
                                                                                (timedelta(days=365) + timedelta(
                                                                                    days=90)))
    if not users_to_delete.exists():
        return users_to_delete.delete()
