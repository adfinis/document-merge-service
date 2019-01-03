from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from rest_framework import serializers

from . import engines, models


class TemplateSerializer(serializers.ModelSerializer):
    def validate(self, data):
        engine = data.get("engine", self.instance and self.instance.engine)
        template = data.get("template", self.instance and self.instance.template)

        engine = engines.get_engine(engine, template)
        engine.validate()

        return data

    class Meta:
        model = models.Template
        fields = ("slug", "description", "template", "engine")


class TemplateMergeSerializer(serializers.Serializer):
    data = serializers.JSONField(
        required=True, help_text="Data as json used for merging"
    )
    convert = serializers.ChoiceField(
        allow_null=True,
        required=False,
        choices=settings.UNOCONV_ALLOWED_TYPES,
        help_text="Optionally convert result document to this type.",
    )

    def validate_convert(self, value):
        if not settings.UNOCONV_URL:
            raise ImproperlyConfigured(
                f"To use conversion you need to configure `UNOCONV_URL`"
            )

        return value
