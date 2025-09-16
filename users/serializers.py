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
        source="course.title", read_only=True, allow_null=True
    )
    lesson_name = serializers.CharField(
        source="lesson.title", read_only=True, allow_null=True
    )

    class Meta:
        model = Payment
        fields = [
            "id",
            "user_email",
            "payment_date",
            "course_name",
            "lesson_name",
            "amount",
            "payment_method",
        ]


class PaymentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ["__all__"]
