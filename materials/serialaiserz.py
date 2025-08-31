from materials.models import Course, Lesson
from rest_framework.serializers import ModelSerializer


class CourseSerialaizer(ModelSerializer):
    class Meta:
        model = Course
        fields = "__all__"


class LessonSerialaizer(ModelSerializer):
    class Meta:
        model = Lesson
        fields = "__all__"
