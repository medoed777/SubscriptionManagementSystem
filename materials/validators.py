from rest_framework.serializers import ValidationError

valid_url = "youtube.com"


def validation_url(value: str):
    if valid_url not in value:
        raise ValidationError(f"Корректная ссылка на ресурс - {valid_url}")
