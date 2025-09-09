from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets


from materials.models import Course, Lesson
from materials.serialiserz import (CourseSerializer,
                                   LessonSerializer)
from users.filters import PaymentFilter
from users.models import Payment


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
