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
    data = serializers.JSONField(required=True)
