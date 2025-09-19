from django.contrib.auth.models import AbstractUser
from django.db import models

from materials.models import Course, Lesson


class User(AbstractUser):
    username = None

    email = models.EmailField(
        unique=True,
        verbose_name="Email",
        help_text="Введите почту",
        blank=False,
        null=False,
    )
    avatar = models.ImageField(
        upload_to="avatar/",
        blank=True,
        null=True,
        verbose_name="Аватар",
        help_text="Установите аватар",
    )
    phone_number = models.CharField(
        max_length=30,
        blank=True,
        null=True,
        verbose_name="Номер телефона",
        help_text="Укажите номер телефона",
    )
    city = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name="Город",
        help_text="Укажите город",
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"


class Payment(models.Model):
    PAYMENT_METHODS = [
        ("cash", "Наличные"),
        ("transfer", "Перевод на счет"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    payment_date = models.DateTimeField(auto_now_add=True)
    session_id = models.TextField(
        max_length=255, null=True, blank=True, verbose_name="ID сессии"
    )
    link = models.TextField(verbose_name="Ссылка на оплату", null=True, blank=True)
    course = models.ForeignKey(Course, null=True, blank=True, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, null=True, blank=True, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField(default=0, verbose_name="Сумма оплаты")
    payment_method = models.CharField(max_length=10, choices=PAYMENT_METHODS)

    class Meta:
        verbose_name = "Платеж"
        verbose_name_plural = "Платежи"

    def __str__(self):
        return f"Платеж от {self.user.email} на сумму {self.amount} руб."


class Subscription(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name="Пользователь"
    )
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, verbose_name="Подписка на курс"
    )
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Подписка"
        verbose_name_plural = "Подписки"

    def __str__(self):
        return f"{self.user.email} подписан на {self.course.title}"
