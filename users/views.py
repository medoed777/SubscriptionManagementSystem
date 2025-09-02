from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets

from users.filters import PaymentFilter
from users.models import Payment
from users.serializers import PaymentSerializer


class PaymentViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Payment.objects.all()
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filtered_class = PaymentFilter
    ordering_fields = ["date_pay"]
    ordering = ["-date_pay"]

    serializer_class = PaymentSerializer
