from rest_framework.serializers import ModelSerializer, SerializerMethodField
from rest_framework import serializers
from materials.models import Course, Lesson
from materials.validators import validation_url


class LessonSerializer(ModelSerializer):
    link = serializers.CharField(validators=[validation_url])

    class Meta:
        model = Lesson
        fields = ["id", "title", "description", "preview", "link"]


class LessonDetailSerializer(ModelSerializer):
    link = serializers.CharField(validators=[validation_url])

    class Meta:
        model = Lesson
        fields = ["id", "title", "description", "link"]


class CourseSerializer(ModelSerializer):
    class Meta:
        model = Course
        fields = "__all__"


class CourseCountSerializer(ModelSerializer):

    lessons = LessonDetailSerializer(many=True, read_only=True)
    lesson_count = SerializerMethodField()

    def get_lessons_count(self, obj):
        return obj.lessons.count()

    class Meta:
        model = Course
        fields = ["id", "title", "description", "lesson_count", "lessons"]
