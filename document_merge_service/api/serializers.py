import json
from functools import singledispatch

from django.conf import settings
from django.urls import reverse
from generic_permissions.validation import ValidatorMixin
from rest_framework import exceptions, serializers

from . import engines, models


class CustomFileField(serializers.FileField):
    """
    Custom FileField.

    `to_representation()` of this FileField returns the file object instead of just the
    filename.
    """

    def to_representation(self, value):
        return value or None


class TemplateFileField(serializers.FileField):
    def get_attribute(self, instance):
        # Hacky workaround - we need the instance in `to_representation()`,
        # not the field value.
        # We cannot use `parent.instance`, as that won't be set to
        # the current instance in a list view
        return instance

    def to_representation(self, value):
        if value and value.pk and value.template:
            return reverse("template-download", args=[value.pk])


class AvailablePlaceholdersField(serializers.ListField):
    """A list field type that also accepts JSON lists.

    Instead of multiple fields with the same name (traditional
    form-data lists), we also accept a JSON list for the available
    placeholders. This helps reduce the number of fields in the
    request, which WAF, Django, and possibly other server-side
    web components don't appreciate.
    """

    def to_internal_value(self, data):
        data = data if isinstance(data, list) else [data]
        all_values = []
        for value in data:
            if value.startswith("["):
                # looks like JSON, parse it
                all_values.extend(json.loads(value))
            else:
                all_values.append(value)

        return all_values


class TemplateSerializer(ValidatorMixin, serializers.ModelSerializer):
    disable_template_validation = serializers.BooleanField(
        allow_null=True, default=False
    )
    available_placeholders = AvailablePlaceholdersField(allow_null=True, required=False)
    sample_data = serializers.JSONField(allow_null=True, required=False)
    files = serializers.ListField(
        child=CustomFileField(write_only=True, allow_empty_file=False), required=False
    )
    template = TemplateFileField()

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
        user = self.context["request"].user

        if self.instance is None:
            data["created_by_user"] = user.username
            data["created_by_group"] = user.group
        data["modified_by_user"] = user.username
        data["modified_by_group"] = user.group

        if data.pop("disable_template_validation", False):
            # Some template structures cannot be validated automatically,
            # or it would be impossible or too much effort to provide accurate
            # sample data. For those cases, we allow disabling the validation.
            return data

        engine = data.get("engine", self.instance and self.instance.engine)
        template = data.get("template", self.instance and self.instance.template)

        available_placeholders = data.pop("available_placeholders", None)
        sample_data = data.pop("sample_data", None)
        files = data.pop("files", None)

        if sample_data and available_placeholders:
            raise exceptions.ValidationError(
                "Only one of available_placeholders and sample_data is allowed"
            )
        elif files and engine != models.Template.DOCX_TEMPLATE:
            raise exceptions.ValidationError(
                f'Files are only accepted with the "{models.Template.DOCX_TEMPLATE}"'
                f" engine"
            )
        elif sample_data:
            if files:
                for file in files:
                    sample_data[file.name] = file

            available_placeholders = self._sample_to_placeholders(sample_data)
        elif files:
            raise exceptions.ValidationError(
                "Files are only accepted when also providing sample_data"
            )

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
            "available_placeholders",
            "sample_data",
            "files",
            "disable_template_validation",
            "meta",
            "created_at",
            "created_by_user",
            "created_by_group",
            "modified_at",
            "modified_by_user",
            "modified_by_group",
        )
        extra_kwargs = {
            "created_at": {"read_only": True},
            "created_by_user": {"read_only": True},
            "created_by_group": {"read_only": True},
            "modified_at": {"read_only": True},
            "modified_by_user": {"read_only": True},
            "modified_by_group": {"read_only": True},
        }


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

    class Meta:
        model = models.Template


class ConvertSerializer(serializers.Serializer):
    file = CustomFileField(required=True, allow_empty_file=False)
    target_format = serializers.ChoiceField(
        allow_null=False,
        required=True,
        choices=[("pdf", "PDF")],
        help_text="The target format of the conversion. Currently only 'pdf' is supported.",
    )
