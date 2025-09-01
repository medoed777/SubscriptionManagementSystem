from rest_framework.serializers import ModelSerializer, SerializerMethodField

from materials.models import Course, Lesson


class CourseSerialaizer(ModelSerializer):
    class Meta:
        model = Course
        fields = "__all__"


class CourseCountSerializer(ModelSerializer):
    lessons = LessonSerializer(many=True, read_only=True)  # Вложенный сериализатор
    lesson_count = serializers.SerializerMethodField()

    def get_lesson_count(self, obj):
        return obj.lessons.count()

    class Meta:
        model = Course
        fields = ['id', 'title', 'description', 'lesson_count', 'lessons']


class LessonSerialaizer(ModelSerializer):
    class Meta:
        model = Lesson
        fields = "__all__"
