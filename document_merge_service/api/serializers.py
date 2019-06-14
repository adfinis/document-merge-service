from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.utils.translation import ugettext as _
from rest_framework import exceptions, serializers

from . import engines, models


class CurrentGroupDefault:
    def set_context(self, serializer_field):
        self.user = serializer_field.context["request"].user

    def __call__(self):
        return self.user.group

    def __str__(self):
        return self.user.group


class TemplateSerializer(serializers.ModelSerializer):
    group = serializers.CharField(allow_null=True, default=CurrentGroupDefault())

    def validate_group(self, group):
        request = self.context["request"]
        if group and group not in request.user.groups:
            raise exceptions.ValidationError(_(f"User is not member of group {group}"))

        return group

    def validate(self, data):
        engine = data.get("engine", self.instance and self.instance.engine)
        template = data.get("template", self.instance and self.instance.template)

        engine = engines.get_engine(engine, template)
        engine.validate()

        return data

    class Meta:
        model = models.Template
        fields = ("slug", "description", "template", "engine", "group")


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
        if not settings.UNOCONV_URL and not settings.UNOCONV_LOCAL:
            raise ImproperlyConfigured(
                "To use conversion you need to configure `UNOCONV_URL`"
            )

        return value
