from rest_framework.generics import (CreateAPIView, DestroyAPIView,
                                     ListAPIView, RetrieveAPIView,
                                     UpdateAPIView)
from rest_framework.viewsets import ModelViewSet

from materials import models
from materials.serialaiserz import CourseSerialaizer, LessonSerialaizer, CourseCountSerializer


class CourseViewSet(ModelViewSet):
    queryset = models.Course.objects.all()

    def get_serializer_class(self):
        if self.action == "retrieve":
            return serializers.CourseCountSerializer
        return serializers.CourseSerialize


class LessonListAPIView(ListAPIView):
    queryset = models.Lesson.objects.all()
    serializer_class = LessonSerialaizer


class LessonCreateAPIView(CreateAPIView):
    queryset = models.Lesson.objects.all()
    serializer_class = LessonSerialaizer


class LessonRetrieveAPIView(RetrieveAPIView):
    queryset = models.Lesson.objects.all()
    serializer_class = LessonSerialaizer


class LessonUpdateAPIView(UpdateAPIView):
    queryset = models.Lesson.objects.all()
    serializer_class = LessonSerialaizer


class LessonDestroyAPIView(DestroyAPIView):
    queryset = models.Lesson.objects.all()
    serializer_class = LessonSerialaizer
