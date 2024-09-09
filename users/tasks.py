from datetime import timedelta, datetime

from celery import shared_task
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import send_mail


@shared_task
def send_email_test_task():
    send_mail(
        subject='Test email',
        message='Test email',
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=["iliyaign1231@gmail.com", ]
    )

@shared_task(bind=True, max_retries=3)
def send_welcome_email(self, user_email):
    try:
        send_mail(
            subject='Welcome',
            message=f'Welcome to our website, {user_email}',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user_email, ],
            fail_silently=False
        )
    except Exception as e:
        raise self.retry(exc=e, countdown=60)


@shared_task
def send_daily_email_if_user_inactive_for_year():
    inactive_users = get_user_model().objects.filter(is_active=True,
                                                     date_joined__lt=datetime.now() - timedelta(days=365))
    if inactive_users.exists():
        send_mail(
            subject='Inactive users',
            message=f'Your account will be blocked if you will not log in next 3 months',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user.email for user in inactive_users]
        )


@shared_task
def test_schedule_task():
    print('Its test task!')