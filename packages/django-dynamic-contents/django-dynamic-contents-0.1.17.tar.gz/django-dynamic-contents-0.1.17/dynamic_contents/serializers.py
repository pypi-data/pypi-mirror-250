from rest_framework import serializers
from .models import Format, Part
from django.utils.translation import get_language


class FormatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Format
        fields = ['type', 'subtype', 'content']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        current_language = get_language()

        # 현재 언어에 맞는 content 필드 선택
        content_field = f"content_{current_language}"
        if hasattr(instance, content_field):
            representation['content'] = getattr(instance, content_field)

        return representation


class PartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Part
        fields = ['field', 'content', 'link', 'instance_id']


class DynamicContentSerializerMixin:
    format = FormatSerializer(read_only=True)
    parts = PartSerializer(many=True, read_only=True)

    class Meta:
        fields = ['id', 'format', 'parts', 'content_text', 'content_html']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['text'] = instance.get_text()
        representation['html'] = instance.get_html()
        return representation

