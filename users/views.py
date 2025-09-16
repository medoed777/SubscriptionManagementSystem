from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets
from rest_framework.generics import CreateAPIView, get_object_or_404
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from materials.models import Course
from users.filters import PaymentFilter
from users.models import Payment, Subscription, User
from users.serializers import (
    PaymentCreateSerializer,
    PaymentSerializer,
    UserCreateSerializer,
    UserDetailViewSerializer,
    UserViewSerializer,
)
from users.services import create_stripe_price_amount, create_stripe_session


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


class SubscriptionAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        course_id = request.data.get("course_id")
        course_item = get_object_or_404(Course, id=course_id)
        subs_item = Subscription.objects.filter(user=request.user, course=course_item)

        if subs_item.exists():
            subs_item.delete()
            message = "Подписка удалена"
        else:
            Subscription.objects.create(user=request.user, course=course_item)
            message = "Подписка добавлена"

        return Response({"message": message})


class PaymentCreateAPIView(CreateAPIView):
    serializer_class = PaymentCreateSerializer
    queryset = Payment.objects.all()

    def perform_create(self, serializer):
        payment = serializer.save(user=self.request.user)
        amount = create_stripe_price_amount(payment.name_product, payment.amount)
        session_id, link = create_stripe_session(amount)
        payment.session_id = session_id
        payment.link = link
        payment.save()
