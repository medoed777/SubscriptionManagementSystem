from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets, generics
from rest_framework.permissions import IsAuthenticated

from materials.models import Course, Lesson
from materials.paginators import CustomPagination
from materials.serializers import CourseSerializer, LessonSerializer
from materials.tasks import send_course_update_email
from users.permissions import IsOwner, ModeratorPermissions


class CoursesViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    ordering_fields = ["title"]
    ordering = ["-title"]
    serializer_class = CourseSerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        qs = super().get_queryset()
        user = self.request.user

        if user.is_authenticated:
            if user.groups.filter(name="moders").exists():
                return qs
            return qs.filter(owner=user)

        return qs.none()

    def perform_create(self, serializer):
        course = serializer.save(owner=self.request.user)

    def get_permissions(self):
        if self.action == "create":
            self.permission_classes = [IsAuthenticated, ~ModeratorPermissions]
        elif self.action in ["update", "partial_update", "retrieve"]:
            self.permission_classes = [IsAuthenticated, ModeratorPermissions | IsOwner]
        elif self.action == "destroy":
            self.permission_classes = [IsAuthenticated, IsOwner]
        return super().get_permissions()


class CourseUpdateAPIView(generics.UpdateAPIView):
    serializer_class = CourseSerializer
    queryset = Course.objects.all()

    def perform_update(self, serializer):
        instance = serializer.save()
        subscribers = instance.subscription.filter(is_active=True)

        for subscriber in subscribers:
            send_course_update_email.delay(instance.title, subscriber.user.email)


class LessonsViewSet(viewsets.ModelViewSet):
    queryset = Lesson.objects.all()
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    ordering_fields = ["title"]
    ordering = ["-title"]
    serializer_class = LessonSerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        qs = super().get_queryset()
        user = self.request.user
        if user.is_authenticated and user.groups.filter(name="moders").exists():
            return qs

        if user.is_authenticated:
            return qs.filter(owner=user)

        return qs.none()

    def perform_create(self, serializer):
        lesson = serializer.save()
        lesson.owner = self.request.user
        lesson.save()

    def get_permissions(self):
        if self.action == "create":
            self.permission_classes = (
                IsAuthenticated,
                ~ModeratorPermissions,
            )
        elif self.action in ["update", "partial_update", "retrieve"]:
            self.permission_classes = (
                IsAuthenticated,
                ModeratorPermissions | IsOwner,
            )
        elif self.action == "destroy":
            self.permission_classes = (
                IsAuthenticated,
                IsOwner,
            )
        return super().get_permissions()
