from django.apps import AppConfig
from django.conf import settings
from django.db.models import TextField
from django.db.models.lookups import IContains


class DefaultConfig(AppConfig):
    name = "document_merge_service.api"

    def ready(self):
        if "sqlite3" in settings.DATABASES["default"]["ENGINE"]:  # pragma: no cover
            TextField.register_lookup(IContains, lookup_name="search")
        mitigate_docxtpl_corruption_bug()


def mitigate_docxtpl_corruption_bug():
    # This is basically monkey-patching this PR:
    # https://github.com/python-openxml/python-docx/pull/1436

    # Hold my beer!
    from docx.opc.constants import RELATIONSHIP_TYPE

    if hasattr(RELATIONSHIP_TYPE, "CORE_PROPERTIES_OFFICEDOCUMENT"):  # pragma: no cover
        raise Exception(
            "The docxtpl mitigation is no longer required, please remove the monkeypatch code"
        )

    RELATIONSHIP_TYPE.CORE_PROPERTIES_OFFICEDOCUMENT = (
        "http://schemas.openxmlformats.org/officedocument/2006/relationships"
        "/metadata/core-properties"
    )

    from docx.opc.package import RT, CorePropertiesPart, OpcPackage, cast

    @property
    def _core_properties_part(self) -> CorePropertiesPart:
        """|CorePropertiesPart| object related to this package.

        Creates a default core properties part if one is not present (not common).
        """
        try:
            return cast(CorePropertiesPart, self.part_related_by(RT.CORE_PROPERTIES))
        except KeyError:
            try:
                office_document_part = self.part_related_by(
                    RT.CORE_PROPERTIES_OFFICEDOCUMENT  # type: ignore
                )
                rel = self.relate_to(
                    office_document_part,
                    RT.CORE_PROPERTIES_OFFICEDOCUMENT,  # type: ignore
                )
                self.rels[rel].reltype = RT.CORE_PROPERTIES
                return cast(CorePropertiesPart, office_document_part)
            except KeyError:
                core_properties_part = CorePropertiesPart.default(self)
                self.relate_to(core_properties_part, RT.CORE_PROPERTIES)
                return core_properties_part

    OpcPackage._core_properties_part = _core_properties_part

    from docx.opc.rel import _Relationship

    @_Relationship.reltype.setter
    def reltype(self, value: str):
        self._reltype = value

    _Relationship.reltype = reltype
