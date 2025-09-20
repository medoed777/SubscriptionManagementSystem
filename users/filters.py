import django_filters

from materials.models import Course, Lesson
from users.models import Payment


class PaymentFilter(django_filters.FilterSet):
    lesson = django_filters.ModelChoiceFilter(
        field_name="lesson", queryset=Lesson.objects.all(), label="Урок"
    )
    course = django_filters.ModelChoiceFilter(
        field_name="course", queryset=Course.objects.all(), label="Курс"
    )
    type_pay = django_filters.ChoiceFilter(
        field_name="type_pay", choices=Payment.PAYMENT_METHODS, label="Вид оплаты"
    )

    class Meta:
        model = Payment
        fields = ["course", "lesson", "type_pay"]
