import mimetypes
from os.path import splitext
from pathlib import Path

import jinja2
from django.http import FileResponse, HttpResponse
from generic_permissions.permissions import PermissionViewMixin
from generic_permissions.visibilities import VisibilityViewMixin
from rest_framework import exceptions, viewsets
from rest_framework.decorators import action
from rest_framework.generics import RetrieveAPIView
from rest_framework.views import APIView

from . import engines, filters, models, serializers
from .file_converter import FileConverter


class TemplateView(VisibilityViewMixin, PermissionViewMixin, viewsets.ModelViewSet):
    queryset = models.Template.objects
    serializer_class = serializers.TemplateSerializer
    filterset_class = filters.TemplateFilterSet
    ordering_fields = ("slug", "description")
    ordering = ("slug",)

    @action(
        methods=["post"],
        detail=True,
        serializer_class=serializers.TemplateMergeSerializer,
    )
    def merge(self, request, pk=None):
        template = self.get_object()
        engine = engines.get_engine(template.engine, template.template)

        content_type, _ = mimetypes.guess_type(template.template.name)
        response = HttpResponse(
            content_type=content_type or "application/force-download"
        )

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.data["data"]
        files = serializer.data.get("files")

        if files is not None:
            for file in files:
                data[file.name] = file

        try:
            response = engine.merge(serializer.data["data"], response)
        except jinja2.UndefinedError as exc:
            raise exceptions.ValidationError(
                f"Placeholder from template not found in data: {exc}"
            )

        convert = serializer.data.get("convert")

        if convert:
            response = FileConverter.convert(response.content, convert)

        filename = f"{template.slug}.{convert}"
        response["Content-Disposition"] = f'attachment; filename="{filename}"'
        return response


class DownloadTemplateView(RetrieveAPIView):
    queryset = models.Template.objects
    lookup_field = "pk"

    def retrieve(self, request, **kwargs):
        template = self.get_object()

        return FileResponse(
            template.template.file,
            filename=f"{template.slug}{Path(template.template.name).suffix}",
        )


class ConvertView(APIView):
    def post(self, request, **kwargs):
        serializer = serializers.ConvertSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        file = serializer.data["file"]
        target_format = serializer.data["target_format"]

        content_type, foo = mimetypes.guess_type(file.name)

        if content_type not in [
            "application/vnd.oasis.opendocument.text",
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        ]:
            raise exceptions.ValidationError(
                "Incorrect file format. Only docx and odt files are supported for conversion."
            )

        response = FileConverter.convert(file.read(), target_format)

        filename = f"{splitext(file.name)[0]}.{target_format}"
        response["Content-Disposition"] = f'attachment; filename="{filename}"'
        return response
