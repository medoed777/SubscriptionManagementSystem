from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, SerializerMethodField

from materials.models import Course, Lesson
from materials.validators import validation_url
from users.models import Subscription


class LessonSerializer(ModelSerializer):
    link = serializers.CharField(validators=[validation_url])

    class Meta:
        model = Lesson
        fields = ["id", "title", "description", "preview", "link"]


class LessonDetailSerializer(ModelSerializer):

    class Meta:
        model = Lesson
        fields = ["id", "title", "description", "link"]


class CourseSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = ["id", "title", "description", "is_subscribed"]

    def get_is_subscribed(self, obj):
        request = self.context.get("request")
        if request and request.user.is_authenticated:
            return Subscription.objects.filter(user=request.user, course=obj).exists()
        return False


class CourseCountSerializer(ModelSerializer):

    lessons = LessonDetailSerializer(many=True, read_only=True)
    lesson_count = SerializerMethodField()

    def get_lessons_count(self, obj):
        return obj.lessons.count()

    class Meta:
        model = Course
        fields = ["id", "title", "description", "lesson_count", "lessons"]
