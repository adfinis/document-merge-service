""".

Modified version of https://github.com/elapouya/python-docx-template/blob/082a1c6ad133809ed0039627cc8dbdd6d309feda/docxtpl/inline_image.py

Original Copyright (c) Eric Lapouyade and python-docx-template contributors

Modified in 2026 to:
- prevent access to the template in sandboxed jinja (`tpl` -> `_tpl`)
- dropped `anchor` functionality as it's not used by us

Distributed under/with the original LICENSE. (LGPL-2.1-only)
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from docxtpl.template import DocxTemplate


class InlineImage:
    """Class to generate an inline image.

    This is much faster than using Subdoc class.
    """

    def __init__(
        self,
        tpl: DocxTemplate,
        image_descriptor,
        width=None,
        height=None,
    ):
        self._tpl = tpl
        self.image_descriptor = image_descriptor
        self.width, self.height = width, height

    def _insert_image(self):
        assert self._tpl.current_rendering_part is not None
        pic = self._tpl.current_rendering_part.new_pic_inline(
            self.image_descriptor,
            self.width,
            self.height,
        ).xml
        return (
            "</w:t></w:r><w:r><w:drawing>%s</w:drawing></w:r><w:r>"
            '<w:t xml:space="preserve">' % pic
        )

    def __unicode__(self):
        return self._insert_image()

    def __str__(self):
        return self._insert_image()

    def __html__(self):
        return self._insert_image()
