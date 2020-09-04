from functools import singledispatch

from django.conf import settings
from django.utils.translation import ugettext as _
from rest_framework import exceptions, serializers

from . import engines, models


class CurrentGroupDefault:
    requires_context = True

    def __call__(self, serializer_field):
        return serializer_field.context["request"].user.group


class TemplateSerializer(serializers.ModelSerializer):
    group = serializers.CharField(allow_null=True, default=CurrentGroupDefault())
    available_placeholders = serializers.ListField(allow_null=True, required=False)
    sample_data = serializers.JSONField(allow_null=True, required=False)

    def validate_group(self, group):
        request = self.context["request"]
        if group and group not in request.user.groups:
            raise exceptions.ValidationError(_(f"User is not member of group {group}"))

        return group

    def _sample_to_placeholders(self, sample_doc):
        @singledispatch
        def _doc(doc):
            return ""

        @_doc.register(dict)
        def _(doc):
            return [f"{k}.{name}" for k, v in doc.items() for name in _doc(v)] + [
                k for k in doc.keys()
            ]

        @_doc.register(list)
        def _(doc):
            res = []
            for item in doc:
                res.extend([f"[].{var}" if var else "[]" for var in _doc(item)])
                res.append("[]")
            return list(set(res))

        return sorted([x.replace(".[]", "[]") for x in _doc(sample_doc)])

    def validate(self, data):
        engine = data.get("engine", self.instance and self.instance.engine)
        template = data.get("template", self.instance and self.instance.template)

        available_placeholders = data.pop("available_placeholders", None)
        sample_data = data.pop("sample_data", None)

        if sample_data and available_placeholders:
            raise exceptions.ValidationError(
                "Only one of available_placeholders and sample_data is allowed"
            )
        elif sample_data:
            available_placeholders = self._sample_to_placeholders(sample_data)

        engine = engines.get_engine(engine, template)
        engine.validate(
            available_placeholders=available_placeholders, sample_data=sample_data
        )

        return data

    class Meta:
        model = models.Template
        fields = (
            "slug",
            "description",
            "template",
            "engine",
            "group",
            "available_placeholders",
            "sample_data",
        )


class CustomFileField(serializers.FileField):
    """
    Custom FileField.

    `to_representation()` of this FileField returns the file object instead of just the
    filename.
    """

    def to_representation(self, value):
        return value or None


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
    files = serializers.ListField(
        child=CustomFileField(write_only=True, allow_empty_file=False), required=False
    )
