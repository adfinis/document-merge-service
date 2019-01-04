import mimetypes

import requests
from django.conf import settings
from django.http import HttpResponse
from django.utils.encoding import smart_str
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.generics import RetrieveAPIView

from . import engines, models, serializers


class TemplateView(viewsets.ModelViewSet):
    queryset = models.Template.objects
    serializer_class = serializers.TemplateSerializer
    filterset_fields = {"slug": ["exact"], "description": ["icontains"]}
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

        response = HttpResponse()
        mime_type, _ = mimetypes.guess_type(template.template.name)
        extension = mimetypes.guess_extension(mime_type)
        filename = f"{template.slug}.{extension}"
        response["Content-Disposition"] = f'attachment; filename="{filename}"'
        response["Content-Type"] = mimetypes.guess_type(filename)[0]

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        response = engine.merge(serializer.data["data"], response)
        convert = serializer.data.get("convert")
        if convert:
            url = f"{settings.UNOCONV_URL}/unoconv/{convert}"
            requests_response = requests.post(url, files={"file": response.content})
            return HttpResponse(
                content=requests_response.content,
                status=requests_response.status_code,
                content_type=requests_response.headers["Content-Type"],
            )

        return response


class DownloadTemplateView(RetrieveAPIView):
    queryset = models.Template.objects
    lookup_field = "template"

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
