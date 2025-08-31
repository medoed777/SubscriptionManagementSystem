from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    username = None

    email = models.EmailField(
        unique=True, verbose_name="Email", help_text="Введите почту"
    )
    avatar = models.ImageField(
        upload_to="avatar/", blank=True, null=True, verbose_name="Аватар", help_text="Установите аватар"
    )
    phone_number = models.CharField(
        max_length=30, blank=True, null=True, verbose_name="Номер телефона", help_text="Укажите номер телефона"
    )
    city = models.CharField(max_length=50, blank=True, null=True, verbose_name="Город", help_text="Укажите город")

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
