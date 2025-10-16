from celery import shared_task
from django.core.mail import send_mail


@shared_task
def send_course_update_email(course_title, user_email):
    subject = f"Обновление курса: {course_title}"
    message = f'Курс "{course_title}" был обновлен. Проверьте изменения!'
    from_email = "your_email@example.com"
    recipient_list = [user_email]
    send_mail(subject, message, from_email, recipient_list)
