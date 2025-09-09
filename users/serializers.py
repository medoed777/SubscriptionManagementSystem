from rest_framework import serializers

from users.models import Payment, User


class UserDetailViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["email", "password", "phone_number"]


class UserViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["email", "phone_number"]


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["email", "password"]


class PaymentSerializer(serializers.ModelSerializer):
    user_email = serializers.EmailField(source="user.email", read_only=True)
    course_name = serializers.CharField(
        source="course.name", read_only=True, allow_null=True
    )
    lesson_name = serializers.CharField(
        source="lesson.name", read_only=True, allow_null=True
    )

    class Meta:
        model = Payment
        fields = [
            "id",
            "user_email",
            "date_pay",
            "course_name",
            "lesson_name",
            "money",
            "type_pay",
        ]
