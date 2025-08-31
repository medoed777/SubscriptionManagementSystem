from materials import models
from rest_framework.viewsets import ModelViewSet
from materials.serialaiserz import CourseSerialaizer, LessonSerialaizer
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView


class CourseViewSet(ModelViewSet):
    queryset = models.Course.objects.all()
    serializer_class = CourseSerialaizer


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
