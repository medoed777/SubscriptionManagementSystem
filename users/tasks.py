from datetime import datetime, timedelta

from celery import shared_task
from django.core.mail import send_mail

from config.settings import EMAIL_HOST_USER
from users.models import User


@shared_task
def user_active_period():
    now = datetime.now()
    inactive_users = User.objects.filter(
        is_superuser=False, last_login__lt=now - timedelta(days=30)
    )
    inactive_users.update(is_active=False)


@shared_task
def send_subscribe_user_course(theme: str, message: str, email: str):
    send_mail(
        subject=theme,
        message=message,
        recipient_list=[email],
        from_email=EMAIL_HOST_USER,
    )
