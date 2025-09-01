from django.db import models


class Course(models.Model):

    title = models.CharField(
        max_length=100, verbose_name="Название", help_text="Введите название курса"
    )

    description = models.TextField(
        verbose_name="Описание", help_text="Введите описание курса"
    )

    preview = models.ImageField(
        upload_to="preview/",
        blank="True",
        null="True",
        verbose_name="Превью",
        help_text="Установите картинку",
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"


class Lesson(models.Model):

    title = models.CharField(
        max_length=100, verbose_name="Название", help_text="Введите название урока"
    )

    description = models.TextField(
        verbose_name="Описание", help_text="Введите описание урока"
    )

    preview = models.ImageField(
        upload_to="preview/", blank="True", null="True", verbose_name="Превью"
    )

    link = models.CharField(
        max_length=150,
        blank="True",
        null="True",
        verbose_name="Ссылка",
        help_text="Введите ссылку на урок",
    )

    course = models.ForeignKey(
        Course,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Курс",
        help_text="Выберите курс",
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"
