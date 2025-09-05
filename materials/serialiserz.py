from rest_framework.serializers import ModelSerializer, SerializerMethodField

from materials.models import Course, Lesson


class LessonSerializer(ModelSerializer):
    class Meta:
        model = Lesson
        fields = "__all__"


class LessonDetailSerializer(ModelSerializer):
    class Meta:
        model = Lesson
        fields = ["id", "title", "description"]


class CourseSerializer(ModelSerializer):
    class Meta:
        model = Course
        fields = "__all__"


class CourseCountSerializer(ModelSerializer):
    lessons = LessonDetailSerializer(many=True, read_only=True)
    lesson_count = SerializerMethodField()

    def get_lesson_count(self, obj):
        return obj.lessons.count()

    class Meta:
        model = Course
        fields = ["id", "title", "description", "lesson_count", "lessons"]
