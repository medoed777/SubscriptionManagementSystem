from unittest.mock import patch

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from materials.models import Course, Lesson
from users.models import Subscription, User
import os


os.environ['CELERY_TASK_ALWAYS_EAGER'] = 'True'

from celery import current_app
current_app.conf.task_always_eager = True
current_app.conf.task_eager_propagates = True


class LessonTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email="admin@sky.pro")
        self.course = Course.objects.create(
            title="python", description="backend", owner=self.user
        )
        self.lesson = Lesson.objects.create(
            title="циклы", course=self.course, owner=self.user
        )
        self.client.force_authenticate(user=self.user)

    def test_lesson_retriewe(self):
        url = reverse("materials:lessons-detail", args=(self.lesson.pk,))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )
        self.assertEqual(data.get("title"), self.lesson.title)

    def test_lesson_valid_create(self):
        url = reverse("materials:lessons-list")
        data = {
            "title": "Списки",
            "description": "good",
            "link": "youtube.com",
        }
        response = self.client.post(url, data)
        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )
        self.assertEqual(
            Lesson.objects.all().count(),
            2,
        )

    def test_lesson_invalid_create(self):
        url = reverse("materials:lessons-list")
        data = {
            "title": "Функции",
            "description": "good",
        }
        response = self.client.post(url, data)
        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

    def test_lesson_update(self):
        url = reverse("materials:lessons-detail", args=(self.lesson.pk,))
        data = {
            "title": "Списки",
            "description": "good",
            "link": "youtube.com",
        }
        response = self.client.patch(url, data)
        data = response.json()
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )
        self.assertEqual(data.get("title"), "Списки")

    def test_lesson_delete(self):
        url = reverse("materials:lessons-detail", args=(self.lesson.pk,))
        response = self.client.delete(url)
        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT,
        )
        self.assertEqual(
            Lesson.objects.all().count(),
            0,
        )

    def test_lesson_list(self):
        url = reverse("materials:lessons-list")
        response = self.client.get(url)
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

    def test_subscribe_course(self):
        url = reverse("users:subscribe")
        data = {"course_id": self.course.id}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "Подписка добавлена")
        self.assertTrue(
            Subscription.objects.filter(user=self.user, course=self.course).exists()
        )

    @patch("materials.tasks.send_course_update_email.delay")
    def test_unsubscribe_course(self, mock_send_email):
        Subscription.objects.create(user=self.user, course=self.course)
        url = reverse("users:subscribe")
        data = {"course_id": self.course.id}
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "Подписка удалена")
        self.assertFalse(
            Subscription.objects.filter(user=self.user, course=self.course).exists()
        )
