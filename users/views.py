from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response

from users.filters import PaymentFilter
from users.models import Payment, User
from users.serializers import (
    PaymentSerializer,
    UserCreateSerializer,
    UserDetailViewSerializer,
    UserViewSerializer,
)


class UserCreateAPIView(CreateAPIView):
    serializer_class = UserCreateSerializer
    queryset = User.objects.all()
    permission_classes = (AllowAny,)

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    ordering_fields = ["email"]
    ordering = ["-email"]

    def get_serializer_class(self):
        if self.action == "retrieve":
            return UserDetailViewSerializer
        return UserViewSerializer


class PaymentViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Payment.objects.all()
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filtered_class = PaymentFilter
    ordering_fields = ["date_pay"]
    ordering = ["-date_pay"]
    serializer_class = PaymentSerializer


def notify_user(request: Request):
    if request.method == "POST":
        course_id = request.POST.get("course_id")
        user = request.user
        course_item = get_object_or_404(Course, pk=course_id)
        notify_item: NotifyUser = NotifyUser.objects.filter(user=user, course=course_item).first()

        if subs_item:
            notify_item.delete()
            message = "Подписка удалена"
        else:
            NotifyUser.objects.create(user=user, course=course_item)
            message = "Подписка оформлена"

        return Response({"message": message})
