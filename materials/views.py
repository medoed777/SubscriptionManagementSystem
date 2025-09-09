from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets

from rest_framework.generics import (
    CreateAPIView,
    DestroyAPIView,
    ListAPIView,
    RetrieveAPIView,
    UpdateAPIView,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from materials import models
from materials.models import Course, Lesson
from materials.serialiserz import (
    CourseCountSerializer,
    CourseSerializer,
    LessonSerializer,
)
from users.permissions import IsOwner, ModeratorPermissions


class CoursesViewSet(viewsets.ModelViewSet):

    queryset = Course.objects.all()
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    ordering_fields = ["name"]
    ordering = ["-name"]
    serializer_class = CourseCountSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        user = self.request.user
        if user.groups.filter(name="moders").exists():
            return qs
        return qs.filter(owner=user)

    def perform_create(self, serializer):
        course = serializer.save()
        course.owner = self.request.user
        course.save()

    def get_permissions(self):
        if self.action == "create":
            self.permission_classes = (
                IsAuthenticated,
                ~ModeratorPermissions,
            )
        elif self.action in ["update", "partial_update", "retrieve"]:
            self.permission_classes = (
                IsAuthenticated,
                ModeratorPermissions | IsOwner,
            )
        elif self.action == "destroy":
            self.permission_classes = (
                IsAuthenticated,
                IsOwner,
            )
        return super().get_permissions()


from materials.models import Course, Lesson
from materials.serialiserz import (CourseSerializer,
                                   LessonSerializer)
from users.filters import PaymentFilter
from users.models import Payment


class LessonsViewSet(viewsets.ModelViewSet):


class CoursesViewSet(viewsets.ModelViewSet):

    queryset = Course.objects.all()
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    ordering_fields = ["name"]
    ordering = ["-name"]
    serializer_class = CourseSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        user = self.request.user
        if user.groups.filter(name="moders").exists():
            return qs
        return qs.filter(owner=user)

    def perform_create(self, serializer):
        course = serializer.save()
        course.owner = self.request.user
        course.save()


class LessonsViewSet(viewsets.ModelViewSet):

    queryset = Lesson.objects.all()
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    ordering_fields = ["name"]
    ordering = ["-name"]
    serializer_class = LessonSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        user = self.request.user
        if user.groups.filter(name="moders").exists():
            return qs
        return qs.filter(owner=user)

    def perform_create(self, serializer):
        lesson = serializer.save()
        lesson.owner = self.request.user
        lesson.save()


class PymentViewSet:
    queryset = Payment.objects.all()
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filtered_class = PaymentFilter
    ordering_fields = ["date_pay"]
    ordering = ["-date_pay"]
=======
    queryset = Lesson.objects.all()
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    ordering_fields = ["name"]
    ordering = ["-name"]
    serializer_class = LessonSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        user = self.request.user
        if user.groups.filter(name="moders").exists():
            return qs
        return qs.filter(owner=user)

    def perform_create(self, serializer):
        lesson = serializer.save()
        lesson.owner = self.request.user
        lesson.save()

    def get_permissions(self):
        if self.action == "create":
            self.permission_classes = (
                IsAuthenticated,
                ~ModeratorPermissions,
            )
        elif self.action in ["update", "partial_update", "retrieve"]:
            self.permission_classes = (
                IsAuthenticated,
                ModeratorPermissions | IsOwner,
            )
        elif self.action == "destroy":
            self.permission_classes = (
                IsAuthenticated,
                IsOwner,
            )
        return super().get_permissions()
