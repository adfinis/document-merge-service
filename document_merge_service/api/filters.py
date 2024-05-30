import json

from django.db.models.fields import TextField
from django.db.models.fields.json import KT
from django.db.models.functions import Cast
from django_filters import Filter, FilterSet
from django_filters.constants import EMPTY_VALUES
from rest_framework.exceptions import ValidationError

from . import models


# TODO: refactor into reusable package later
class JSONValueFilter(Filter):
    def filter(self, qs, value):
        if value in EMPTY_VALUES:
            return qs

        valid_lookups = self._valid_lookups(qs)

        try:
            value = json.loads(value)
        except json.decoder.JSONDecodeError:
            raise ValidationError("JSONValueFilter value needs to be json encoded.")

        if isinstance(value, dict):
            # be a bit more tolerant
            value = [value]

        for expr in value:
            if expr in EMPTY_VALUES:  # pragma: no cover
                continue
            if not all(("key" in expr, "value" in expr)):
                raise ValidationError(
                    'JSONValueFilter value needs to have a "key" and "value" and an '
                    'optional "lookup" key.'
                )

            lookup_expr = expr.get("lookup", self.lookup_expr)
            if lookup_expr not in valid_lookups:
                raise ValidationError(
                    f'Lookup expression "{lookup_expr}" not allowed for field '
                    f'"{self.field_name}". Valid expressions: '
                    f'{", ".join(valid_lookups.keys())}'
                )
            # "contains" behaves differently on JSONFields as it does on TextFields.
            # That's why we annotate the queryset with the value.
            # Some discussion about it can be found here:
            # https://code.djangoproject.com/ticket/26511
            if isinstance(expr["value"], str):
                qs = qs.annotate(
                    field_val=Cast(
                        KT(f"{self.field_name}__{expr['key']}"),
                        output_field=TextField(),
                    )
                )
                lookup = {f"field_val__{lookup_expr}": expr["value"]}
            else:
                lookup = {
                    f"{self.field_name}__{expr['key']}__{lookup_expr}": expr["value"]
                }
            qs = qs.filter(**lookup)
        return qs

    def _valid_lookups(self, qs):
        # We need some traversal magic in case field name is a related lookup
        traversals = self.field_name.split("__")
        actual_field = traversals.pop()

        model = qs.model
        for field in traversals:  # pragma: no cover
            model = model._meta.get_field(field).related_model

        return model._meta.get_field(actual_field).get_lookups()


class TemplateFilterSet(FilterSet):
    meta = JSONValueFilter(field_name="meta")

    class Meta:
        model = models.Template
        fields = {
            "slug": ["exact"],
            "description": ["icontains", "search"],
        }
