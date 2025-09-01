from rest_framework.serializers import ModelSerializer, SerializerMethodField

from materials.models import Course, Lesson


class CourseSerialaizer(ModelSerializer):
    class Meta:
        model = Course
        fields = "__all__"


class CourseCountSerializer(ModelSerializer):
    lesson_count = SerializerMethodField()

    def get_lesson_count(self, obj):
        return obj.lessons.count()


    class Meta:
        model = Course
        fields = ["title", "description", "lesson_count"]


class LessonSerialaizer(ModelSerializer):
    class Meta:
        model = Lesson
        fields = "__all__"
