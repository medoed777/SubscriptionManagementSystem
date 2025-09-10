from rest_framework import serializers

valid_url = 'youtube.com'

def validation_url(value: str):
    if valid_url not in value:
        raise serializers.ValidationError(f"Корректная ссылка на ресурс - {valid_url}")
