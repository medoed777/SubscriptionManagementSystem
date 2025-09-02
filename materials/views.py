from rest_framework.generics import (
    CreateAPIView,
    DestroyAPIView,
    ListAPIView,
    RetrieveAPIView,
    UpdateAPIView,
)
from rest_framework.viewsets import ModelViewSet

from materials import models
from materials.serialiserz import (
    CourseCountSerializer,
    CourseSerializer,
    LessonSerializer,
)


class CourseViewSet(ModelViewSet):
    queryset = models.Course.objects.all()

    def get_serializer_class(self):
        if self.action == "retrieve":
            return CourseCountSerializer
        return CourseSerializer


class LessonListAPIView(ListAPIView):
    queryset = models.Lesson.objects.all()
    serializer_class = LessonSerializer


class LessonCreateAPIView(CreateAPIView):
    queryset = models.Lesson.objects.all()
    serializer_class = LessonSerializer


class LessonRetrieveAPIView(RetrieveAPIView):
    queryset = models.Lesson.objects.all()
    serializer_class = LessonSerializer


class LessonUpdateAPIView(UpdateAPIView):
    queryset = models.Lesson.objects.all()
    serializer_class = LessonSerializer


class LessonDestroyAPIView(DestroyAPIView):
    queryset = models.Lesson.objects.all()
    serializer_class = LessonSerializer
