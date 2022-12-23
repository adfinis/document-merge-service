import mimetypes
from pathlib import Path
from tempfile import NamedTemporaryFile

import jinja2
from django.conf import settings
from django.http import HttpResponse
from django.utils.encoding import smart_str
from generic_permissions.permissions import PermissionViewMixin
from generic_permissions.visibilities import VisibilityViewMixin
from rest_framework import exceptions, viewsets
from rest_framework.decorators import action
from rest_framework.generics import RetrieveAPIView

from . import engines, models, serializers
from .unoconv import Unoconv


class TemplateView(VisibilityViewMixin, PermissionViewMixin, viewsets.ModelViewSet):
    queryset = models.Template.objects
    serializer_class = serializers.TemplateSerializer
    filterset_fields = {"slug": ["exact"], "description": ["icontains", "search"]}
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
        extension = mimetypes.guess_extension(content_type)

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
            dir = Path(settings.DATABASE_DIR, "tmp")
            dir.mkdir(parents=True, exist_ok=True)
            with NamedTemporaryFile("wb", dir=dir) as tmp:
                tmp.write(response.content)
                unoconv = Unoconv(
                    pythonpath=settings.UNOCONV_PYTHON,
                    unoconvpath=settings.UNOCONV_PATH,
                )
                result = unoconv.process(tmp.name, convert)
            extension = convert
            status = 500
            if result.returncode == 0:
                status = 200
            response = HttpResponse(
                content=result.stdout, status=status, content_type=result.content_type
            )

        filename = f"{template.slug}.{extension}"
        response["Content-Disposition"] = f'attachment; filename="{filename}"'
        return response


class DownloadTemplateView(RetrieveAPIView):
    queryset = models.Template.objects
    lookup_field = "pk"

    def retrieve(self, request, **kwargs):
        template = self.get_object()

        mime_type, _ = mimetypes.guess_type(template.template.name)
        extension = mimetypes.guess_extension(mime_type)
        content_type = mime_type or "application/force-download"

        response = HttpResponse(content_type=content_type)
        response["Content-Disposition"] = 'attachment; filename="%s"' % smart_str(
            template.slug + extension
        )
        response["Content-Length"] = template.template.size
        response.write(template.template.read())
        return response
