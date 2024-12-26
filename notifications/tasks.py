import logging

from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail

from notifications.models import NotificationSubscription

logger = logging.getLogger(__name__)


@shared_task
def send_new_vacancy_notification(vacancy_model_name: str):

    print('send_new_vacancy_notification:', vacancy_model_name)
    subscriptions = NotificationSubscription.objects.filter(
        notification_type=vacancy_model_name)

    recipient_list = [subscription.user.email for subscription in subscriptions if subscription.user.email]

    logger.debug(f"Sending email notification to {len(recipient_list)} users")
    print(recipient_list)

    send_mail(
        subject=f'Новое {vacancy_model_name}!',
        message=f'New {vacancy_model_name} was created',
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=recipient_list,
        fail_silently=False)

    logger.debug("Email notification was sent successfully")
