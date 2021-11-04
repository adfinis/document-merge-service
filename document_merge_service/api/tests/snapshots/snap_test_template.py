# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot

snapshots = Snapshot()

snapshots[
    'test_merge_expression[{{NAME and ", represents " + NAME}}-template_content1] 1'
] = """<w:body xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" xmlns:o="urn:schemas-microsoft-com:office:office" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" xmlns:v="urn:schemas-microsoft-com:vml" xmlns:w10="urn:schemas-microsoft-com:office:word" xmlns:wp="http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing" xmlns:wps="http://schemas.microsoft.com/office/word/2010/wordprocessingShape" xmlns:wpg="http://schemas.microsoft.com/office/word/2010/wordprocessingGroup" xmlns:mc="http://schemas.openxmlformats.org/markup-compatibility/2006" xmlns:wp14="http://schemas.microsoft.com/office/word/2010/wordprocessingDrawing" xmlns:w14="http://schemas.microsoft.com/office/word/2010/wordml">
  <w:p>
    <w:pPr>
      <w:pStyle w:val="Normal"/>
      <w:rPr/>
    </w:pPr>
    <w:r>
      <w:rPr>
        <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
      </w:rPr>
      <w:t xml:space="preserve">Test</w:t>
    </w:r>
    <w:r>
      <w:rPr>
        <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
      </w:rPr>
      <w:t xml:space="preserve">: , represents foo</w:t>
    </w:r>
  </w:p>
  <w:sectPr>
    <w:type w:val="nextPage"/>
    <w:pgSz w:w="11906" w:h="16838"/>
    <w:pgMar w:left="1134" w:right="1134" w:header="0" w:top="1134" w:footer="0" w:bottom="1134" w:gutter="0"/>
    <w:pgNumType w:fmt="decimal"/>
    <w:formProt w:val="false"/>
    <w:textDirection w:val="lrTb"/>
    <w:docGrid w:type="default" w:linePitch="240" w:charSpace="0"/>
  </w:sectPr>
</w:body>
"""

snapshots[
    'test_merge_expression[{{NAME and ", represents " + NAME}}-template_content2] 1'
] = """<w:body xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" xmlns:o="urn:schemas-microsoft-com:office:office" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" xmlns:v="urn:schemas-microsoft-com:vml" xmlns:w10="urn:schemas-microsoft-com:office:word" xmlns:wp="http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing" xmlns:wps="http://schemas.microsoft.com/office/word/2010/wordprocessingShape" xmlns:wpg="http://schemas.microsoft.com/office/word/2010/wordprocessingGroup" xmlns:mc="http://schemas.openxmlformats.org/markup-compatibility/2006" xmlns:wp14="http://schemas.microsoft.com/office/word/2010/wordprocessingDrawing" xmlns:w14="http://schemas.microsoft.com/office/word/2010/wordml">
  <w:p>
    <w:pPr>
      <w:pStyle w:val="Normal"/>
      <w:rPr/>
    </w:pPr>
    <w:r>
      <w:rPr>
        <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
      </w:rPr>
      <w:t xml:space="preserve">Test</w:t>
    </w:r>
    <w:r>
      <w:rPr>
        <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
      </w:rPr>
      <w:t xml:space="preserve">: </w:t>
    </w:r>
  </w:p>
  <w:sectPr>
    <w:type w:val="nextPage"/>
    <w:pgSz w:w="11906" w:h="16838"/>
    <w:pgMar w:left="1134" w:right="1134" w:header="0" w:top="1134" w:footer="0" w:bottom="1134" w:gutter="0"/>
    <w:pgNumType w:fmt="decimal"/>
    <w:formProt w:val="false"/>
    <w:textDirection w:val="lrTb"/>
    <w:docGrid w:type="default" w:linePitch="240" w:charSpace="0"/>
  </w:sectPr>
</w:body>
"""

snapshots[
    "test_merge_expression[{{blah}}-template_content0] 1"
] = """<w:body xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" xmlns:o="urn:schemas-microsoft-com:office:office" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" xmlns:v="urn:schemas-microsoft-com:vml" xmlns:w10="urn:schemas-microsoft-com:office:word" xmlns:wp="http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing" xmlns:wps="http://schemas.microsoft.com/office/word/2010/wordprocessingShape" xmlns:wpg="http://schemas.microsoft.com/office/word/2010/wordprocessingGroup" xmlns:mc="http://schemas.openxmlformats.org/markup-compatibility/2006" xmlns:wp14="http://schemas.microsoft.com/office/word/2010/wordprocessingDrawing" xmlns:w14="http://schemas.microsoft.com/office/word/2010/wordml">
  <w:p>
    <w:pPr>
      <w:pStyle w:val="Normal"/>
      <w:rPr/>
    </w:pPr>
    <w:r>
      <w:rPr>
        <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
      </w:rPr>
      <w:t xml:space="preserve">Test</w:t>
    </w:r>
    <w:r>
      <w:rPr>
        <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
      </w:rPr>
      <w:t xml:space="preserve">: blub</w:t>
    </w:r>
  </w:p>
  <w:sectPr>
    <w:type w:val="nextPage"/>
    <w:pgSz w:w="11906" w:h="16838"/>
    <w:pgMar w:left="1134" w:right="1134" w:header="0" w:top="1134" w:footer="0" w:bottom="1134" w:gutter="0"/>
    <w:pgNumType w:fmt="decimal"/>
    <w:formProt w:val="false"/>
    <w:textDirection w:val="lrTb"/>
    <w:docGrid w:type="default" w:linePitch="240" w:charSpace="0"/>
  </w:sectPr>
</w:body>
"""

snapshots["test_template_detail 1"] = {
    "available_placeholders": None,
    "description": """Article star very capital morning option. Interesting station story.
Where during teach country talk across drop. Central meeting anyone remember. There today material minute ago get.""",
    "disable_template_validation": False,
    "engine": "docx-mailmerge",
    "group": None,
    "meta": {},
    "sample_data": None,
    "slug": "note-act-source",
    "template": None,
}

snapshots["test_template_list_group_access[None-False-2] 1"] = {
    "count": 2,
    "next": None,
    "previous": None,
    "results": [
        {
            "available_placeholders": None,
            "description": """Article star very capital morning option. Interesting station story.
Where during teach country talk across drop. Central meeting anyone remember. There today material minute ago get.""",
            "disable_template_validation": False,
            "engine": "docx-mailmerge",
            "group": None,
            "meta": {},
            "sample_data": None,
            "slug": "note-act-source",
            "template": None,
        },
        {
            "available_placeholders": None,
            "description": """Various service bank arm. Live by itself writer kitchen develop.
Player foreign idea eye plan third program. Article including take idea.""",
            "disable_template_validation": False,
            "engine": "docx-mailmerge",
            "group": None,
            "meta": {},
            "sample_data": None,
            "slug": "run-too-successful",
            "template": None,
        },
    ],
}

snapshots["test_template_list_group_access[admin-True-2] 1"] = {
    "count": 2,
    "next": None,
    "previous": None,
    "results": [
        {
            "available_placeholders": None,
            "description": """Article star very capital morning option. Interesting station story.
Where during teach country talk across drop. Central meeting anyone remember. There today material minute ago get.""",
            "disable_template_validation": False,
            "engine": "docx-mailmerge",
            "group": "admin",
            "meta": {},
            "sample_data": None,
            "slug": "note-act-source",
            "template": None,
        },
        {
            "available_placeholders": None,
            "description": """Various service bank arm. Live by itself writer kitchen develop.
Player foreign idea eye plan third program. Article including take idea.""",
            "disable_template_validation": False,
            "engine": "docx-mailmerge",
            "group": None,
            "meta": {},
            "sample_data": None,
            "slug": "run-too-successful",
            "template": None,
        },
    ],
}

snapshots["test_template_list_group_access[unknown-False-2] 1"] = {
    "count": 2,
    "next": None,
    "previous": None,
    "results": [
        {
            "available_placeholders": None,
            "description": """Article star very capital morning option. Interesting station story.
Where during teach country talk across drop. Central meeting anyone remember. There today material minute ago get.""",
            "disable_template_validation": False,
            "engine": "docx-mailmerge",
            "group": "unknown",
            "meta": {},
            "sample_data": None,
            "slug": "note-act-source",
            "template": None,
        },
        {
            "available_placeholders": None,
            "description": """Various service bank arm. Live by itself writer kitchen develop.
Player foreign idea eye plan third program. Article including take idea.""",
            "disable_template_validation": False,
            "engine": "docx-mailmerge",
            "group": None,
            "meta": {},
            "sample_data": None,
            "slug": "run-too-successful",
            "template": None,
        },
    ],
}

snapshots["test_template_list_group_access[unknown-True-1] 1"] = {
    "count": 1,
    "next": None,
    "previous": None,
    "results": [
        {
            "available_placeholders": None,
            "description": """Various service bank arm. Live by itself writer kitchen develop.
Player foreign idea eye plan third program. Article including take idea.""",
            "disable_template_validation": False,
            "engine": "docx-mailmerge",
            "group": None,
            "meta": {},
            "sample_data": None,
            "slug": "run-too-successful",
            "template": None,
        }
    ],
}

snapshots[
    "test_template_merge_docx[TestNameMailMerge-docx-mailmerge-template__template1] 1"
] = """<w:body xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" xmlns:wpc="http://schemas.microsoft.com/office/word/2010/wordprocessingCanvas" xmlns:mc="http://schemas.openxmlformats.org/markup-compatibility/2006" xmlns:o="urn:schemas-microsoft-com:office:office" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math" xmlns:v="urn:schemas-microsoft-com:vml" xmlns:wp14="http://schemas.microsoft.com/office/word/2010/wordprocessingDrawing" xmlns:wp="http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing" xmlns:w10="urn:schemas-microsoft-com:office:word" xmlns:w14="http://schemas.microsoft.com/office/word/2010/wordml" xmlns:w15="http://schemas.microsoft.com/office/word/2012/wordml" xmlns:wpg="http://schemas.microsoft.com/office/word/2010/wordprocessingGroup" xmlns:wpi="http://schemas.microsoft.com/office/word/2010/wordprocessingInk" xmlns:wne="http://schemas.microsoft.com/office/word/2006/wordml" xmlns:wps="http://schemas.microsoft.com/office/word/2010/wordprocessingShape">
  <w:p w:rsidR="0083709B" w:rsidRPr="0083709B" w:rsidRDefault="0083709B">
    <w:pPr>
      <w:rPr>
        <w:lang w:val="en-US"/>
      </w:rPr>
    </w:pPr>
    <w:r>
      <w:rPr>
        <w:lang w:val="en-US"/>
      </w:rPr>
      <w:t xml:space="preserve">Test: </w:t>
    </w:r>
    <w:r>
      <w:rPr>
        <w:lang w:val="en-US"/>
      </w:rPr>
      <w:t>Test input</w:t>
    </w:r>
    <w:bookmarkStart w:id="0" w:name="_GoBack"/>
    <w:bookmarkEnd w:id="0"/>
  </w:p>
  <w:sectPr w:rsidR="0083709B" w:rsidRPr="0083709B">
    <w:pgSz w:w="11906" w:h="16838"/>
    <w:pgMar w:top="1417" w:right="1417" w:bottom="1134" w:left="1417" w:header="708" w:footer="708" w:gutter="0"/>
    <w:cols w:space="708"/>
    <w:docGrid w:linePitch="360"/>
  </w:sectPr>
</w:body>
"""

snapshots[
    "test_template_merge_docx[TestNameTemplate-docx-template-template__template0] 1"
] = """<w:body xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" xmlns:o="urn:schemas-microsoft-com:office:office" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" xmlns:v="urn:schemas-microsoft-com:vml" xmlns:w10="urn:schemas-microsoft-com:office:word" xmlns:wp="http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing" xmlns:wps="http://schemas.microsoft.com/office/word/2010/wordprocessingShape" xmlns:wpg="http://schemas.microsoft.com/office/word/2010/wordprocessingGroup" xmlns:mc="http://schemas.openxmlformats.org/markup-compatibility/2006" xmlns:wp14="http://schemas.microsoft.com/office/word/2010/wordprocessingDrawing" xmlns:w14="http://schemas.microsoft.com/office/word/2010/wordml">
  <w:p>
    <w:pPr>
      <w:pStyle w:val="Normal"/>
      <w:rPr/>
    </w:pPr>
    <w:r>
      <w:rPr>
        <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
      </w:rPr>
      <w:t xml:space="preserve">Test</w:t>
    </w:r>
    <w:r>
      <w:rPr>
        <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
      </w:rPr>
      <w:t xml:space="preserve">: Test input</w:t>
    </w:r>
  </w:p>
  <w:sectPr>
    <w:type w:val="nextPage"/>
    <w:pgSz w:w="11906" w:h="16838"/>
    <w:pgMar w:left="1134" w:right="1134" w:header="0" w:top="1134" w:footer="0" w:bottom="1134" w:gutter="0"/>
    <w:pgNumType w:fmt="decimal"/>
    <w:formProt w:val="false"/>
    <w:textDirection w:val="lrTb"/>
    <w:docGrid w:type="default" w:linePitch="240" w:charSpace="0"/>
  </w:sectPr>
</w:body>
"""

snapshots[
    "test_template_merge_jinja_extensions_docx[docx-template-template__template0] 1"
] = """<w:body xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" xmlns:o="urn:schemas-microsoft-com:office:office" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" xmlns:v="urn:schemas-microsoft-com:vml" xmlns:w10="urn:schemas-microsoft-com:office:word" xmlns:wp="http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing" xmlns:wps="http://schemas.microsoft.com/office/word/2010/wordprocessingShape" xmlns:wpg="http://schemas.microsoft.com/office/word/2010/wordprocessingGroup" xmlns:mc="http://schemas.openxmlformats.org/markup-compatibility/2006" xmlns:wp14="http://schemas.microsoft.com/office/word/2010/wordprocessingDrawing" xmlns:w14="http://schemas.microsoft.com/office/word/2010/wordml">
  <w:p>
    <w:pPr>
      <w:pStyle w:val="PreformattedText"/>
      <w:rPr>
        <w:rFonts w:ascii="Consolas;Menlo;Deja Vu Sans Mono;Bitstream Vera Sans Mono;monospace" w:hAnsi="Consolas;Menlo;Deja Vu Sans Mono;Bitstream Vera Sans Mono;monospace"/>
        <w:b w:val="false"/>
        <w:b w:val="false"/>
        <w:i w:val="false"/>
        <w:i w:val="false"/>
        <w:caps w:val="false"/>
        <w:smallCaps w:val="false"/>
        <w:color w:val="3E4349"/>
        <w:spacing w:val="0"/>
      </w:rPr>
    </w:pPr>
    <w:r>
      <w:rPr>
        <w:rFonts w:ascii="Consolas;Menlo;Deja Vu Sans Mono;Bitstream Vera Sans Mono;monospace" w:hAnsi="Consolas;Menlo;Deja Vu Sans Mono;Bitstream Vera Sans Mono;monospace"/>
        <w:b w:val="false"/>
        <w:i w:val="false"/>
        <w:caps w:val="false"/>
        <w:smallCaps w:val="false"/>
        <w:color w:val="B11414"/>
        <w:spacing w:val="0"/>
        <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
      </w:rPr>
      <w:t xml:space="preserve"/>
    </w:r>
  </w:p>
  <w:p>
    <w:pPr>
      <w:pStyle w:val="PreformattedText"/>
      <w:widowControl/>
      <w:shd w:val="clear" w:fill="EEEEEE"/>
      <w:spacing w:before="225" w:after="225"/>
      <w:ind w:left="0" w:right="0" w:hanging="0"/>
      <w:rPr/>
    </w:pPr>
    <w:r>
      <w:rPr>
        <w:rFonts w:ascii="Consolas;Menlo;Deja Vu Sans Mono;Bitstream Vera Sans Mono;monospace" w:hAnsi="Consolas;Menlo;Deja Vu Sans Mono;Bitstream Vera Sans Mono;monospace"/>
        <w:b w:val="false"/>
        <w:i w:val="false"/>
        <w:caps w:val="false"/>
        <w:smallCaps w:val="false"/>
        <w:color w:val="B11414"/>
        <w:spacing w:val="0"/>
        <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
      </w:rPr>
      <w:t xml:space="preserve"/>
    </w:r>
  </w:p>
  <w:p>
    <w:pPr>
      <w:pStyle w:val="PreformattedText"/>
      <w:widowControl/>
      <w:shd w:val="clear" w:fill="EEEEEE"/>
      <w:spacing w:before="225" w:after="225"/>
      <w:ind w:left="0" w:right="0" w:hanging="0"/>
      <w:rPr/>
    </w:pPr>
    <w:r>
      <w:rPr>
        <w:rFonts w:ascii="Consolas;Menlo;Deja Vu Sans Mono;Bitstream Vera Sans Mono;monospace" w:hAnsi="Consolas;Menlo;Deja Vu Sans Mono;Bitstream Vera Sans Mono;monospace"/>
        <w:b w:val="false"/>
        <w:i w:val="false"/>
        <w:caps w:val="false"/>
        <w:smallCaps w:val="false"/>
        <w:color w:val="B11414"/>
        <w:spacing w:val="0"/>
        <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
      </w:rPr>
      <w:t xml:space="preserve">    </w:t>
    </w:r>
    <w:r>
      <w:rPr>
        <w:rFonts w:ascii="Consolas;Menlo;Deja Vu Sans Mono;Bitstream Vera Sans Mono;monospace" w:hAnsi="Consolas;Menlo;Deja Vu Sans Mono;Bitstream Vera Sans Mono;monospace"/>
        <w:b w:val="false"/>
        <w:i w:val="false"/>
        <w:caps w:val="false"/>
        <w:smallCaps w:val="false"/>
        <w:color w:val="B11414"/>
        <w:spacing w:val="0"/>
        <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
      </w:rPr>
      <w:t xml:space="preserve"/>
    </w:r>
  </w:p>
  <w:p>
    <w:pPr>
      <w:pStyle w:val="PreformattedText"/>
      <w:widowControl/>
      <w:shd w:val="clear" w:fill="EEEEEE"/>
      <w:spacing w:before="225" w:after="225"/>
      <w:rPr>
        <w:rFonts w:ascii="Consolas;Menlo;Deja Vu Sans Mono;Bitstream Vera Sans Mono;monospace" w:hAnsi="Consolas;Menlo;Deja Vu Sans Mono;Bitstream Vera Sans Mono;monospace"/>
        <w:b w:val="false"/>
        <w:b w:val="false"/>
        <w:i w:val="false"/>
        <w:i w:val="false"/>
        <w:color w:val="B11414"/>
      </w:rPr>
    </w:pPr>
    <w:r>
      <w:rPr>
        <w:caps w:val="false"/>
        <w:smallCaps w:val="false"/>
        <w:color w:val="3E4349"/>
        <w:spacing w:val="0"/>
      </w:rPr>
      <w:t xml:space="preserve">    </w:t>
    </w:r>
    <w:r>
      <w:rPr>
        <w:rFonts w:ascii="Consolas;Menlo;Deja Vu Sans Mono;Bitstream Vera Sans Mono;monospace" w:hAnsi="Consolas;Menlo;Deja Vu Sans Mono;Bitstream Vera Sans Mono;monospace"/>
        <w:b w:val="false"/>
        <w:i w:val="false"/>
        <w:caps w:val="false"/>
        <w:smallCaps w:val="false"/>
        <w:color w:val="B11414"/>
        <w:spacing w:val="0"/>
      </w:rPr>
      <w:t xml:space="preserve">1</w:t>
    </w:r>
  </w:p>
  <w:p>
    <w:pPr>
      <w:pStyle w:val="PreformattedText"/>
      <w:widowControl/>
      <w:shd w:val="clear" w:fill="EEEEEE"/>
      <w:spacing w:before="225" w:after="225"/>
      <w:rPr>
        <w:rFonts w:ascii="Consolas;Menlo;Deja Vu Sans Mono;Bitstream Vera Sans Mono;monospace" w:hAnsi="Consolas;Menlo;Deja Vu Sans Mono;Bitstream Vera Sans Mono;monospace"/>
        <w:b w:val="false"/>
        <w:b w:val="false"/>
        <w:i w:val="false"/>
        <w:i w:val="false"/>
        <w:caps w:val="false"/>
        <w:smallCaps w:val="false"/>
        <w:color w:val="3E4349"/>
        <w:spacing w:val="0"/>
      </w:rPr>
    </w:pPr>
    <w:r>
      <w:rPr>
        <w:rFonts w:ascii="Consolas;Menlo;Deja Vu Sans Mono;Bitstream Vera Sans Mono;monospace" w:hAnsi="Consolas;Menlo;Deja Vu Sans Mono;Bitstream Vera Sans Mono;monospace"/>
        <w:b w:val="false"/>
        <w:i w:val="false"/>
        <w:caps w:val="false"/>
        <w:smallCaps w:val="false"/>
        <w:color w:val="B11414"/>
        <w:spacing w:val="0"/>
      </w:rPr>
      <w:t xml:space="preserve"/>
    </w:r>
  </w:p>
  <w:p>
    <w:pPr>
      <w:pStyle w:val="PreformattedText"/>
      <w:widowControl/>
      <w:shd w:val="clear" w:fill="EEEEEE"/>
      <w:spacing w:before="225" w:after="225"/>
      <w:ind w:left="0" w:right="0" w:hanging="0"/>
      <w:rPr/>
    </w:pPr>
    <w:r>
      <w:rPr>
        <w:rFonts w:ascii="Consolas;Menlo;Deja Vu Sans Mono;Bitstream Vera Sans Mono;monospace" w:hAnsi="Consolas;Menlo;Deja Vu Sans Mono;Bitstream Vera Sans Mono;monospace"/>
        <w:b w:val="false"/>
        <w:i w:val="false"/>
        <w:caps w:val="false"/>
        <w:smallCaps w:val="false"/>
        <w:color w:val="B11414"/>
        <w:spacing w:val="0"/>
        <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
      </w:rPr>
      <w:t xml:space="preserve">    </w:t>
    </w:r>
    <w:r>
      <w:rPr>
        <w:rFonts w:ascii="Consolas;Menlo;Deja Vu Sans Mono;Bitstream Vera Sans Mono;monospace" w:hAnsi="Consolas;Menlo;Deja Vu Sans Mono;Bitstream Vera Sans Mono;monospace"/>
        <w:b w:val="false"/>
        <w:i w:val="false"/>
        <w:caps w:val="false"/>
        <w:smallCaps w:val="false"/>
        <w:color w:val="B11414"/>
        <w:spacing w:val="0"/>
        <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
      </w:rPr>
      <w:t xml:space="preserve"/>
    </w:r>
  </w:p>
  <w:p>
    <w:pPr>
      <w:pStyle w:val="PreformattedText"/>
      <w:widowControl/>
      <w:shd w:val="clear" w:fill="EEEEEE"/>
      <w:spacing w:before="225" w:after="225"/>
      <w:rPr>
        <w:rFonts w:ascii="Consolas;Menlo;Deja Vu Sans Mono;Bitstream Vera Sans Mono;monospace" w:hAnsi="Consolas;Menlo;Deja Vu Sans Mono;Bitstream Vera Sans Mono;monospace"/>
        <w:b w:val="false"/>
        <w:b w:val="false"/>
        <w:i w:val="false"/>
        <w:i w:val="false"/>
        <w:color w:val="B11414"/>
      </w:rPr>
    </w:pPr>
    <w:r>
      <w:rPr>
        <w:caps w:val="false"/>
        <w:smallCaps w:val="false"/>
        <w:color w:val="3E4349"/>
        <w:spacing w:val="0"/>
      </w:rPr>
      <w:t xml:space="preserve">    </w:t>
    </w:r>
    <w:r>
      <w:rPr>
        <w:rFonts w:ascii="Consolas;Menlo;Deja Vu Sans Mono;Bitstream Vera Sans Mono;monospace" w:hAnsi="Consolas;Menlo;Deja Vu Sans Mono;Bitstream Vera Sans Mono;monospace"/>
        <w:b w:val="false"/>
        <w:i w:val="false"/>
        <w:caps w:val="false"/>
        <w:smallCaps w:val="false"/>
        <w:color w:val="B11414"/>
        <w:spacing w:val="0"/>
      </w:rPr>
      <w:t xml:space="preserve">2</w:t>
    </w:r>
  </w:p>
  <w:p>
    <w:pPr>
      <w:pStyle w:val="PreformattedText"/>
      <w:widowControl/>
      <w:shd w:val="clear" w:fill="EEEEEE"/>
      <w:spacing w:before="225" w:after="225"/>
      <w:rPr>
        <w:rFonts w:ascii="Consolas;Menlo;Deja Vu Sans Mono;Bitstream Vera Sans Mono;monospace" w:hAnsi="Consolas;Menlo;Deja Vu Sans Mono;Bitstream Vera Sans Mono;monospace"/>
        <w:b w:val="false"/>
        <w:b w:val="false"/>
        <w:i w:val="false"/>
        <w:i w:val="false"/>
        <w:caps w:val="false"/>
        <w:smallCaps w:val="false"/>
        <w:color w:val="3E4349"/>
        <w:spacing w:val="0"/>
      </w:rPr>
    </w:pPr>
    <w:r>
      <w:rPr>
        <w:rFonts w:ascii="Consolas;Menlo;Deja Vu Sans Mono;Bitstream Vera Sans Mono;monospace" w:hAnsi="Consolas;Menlo;Deja Vu Sans Mono;Bitstream Vera Sans Mono;monospace"/>
        <w:b w:val="false"/>
        <w:i w:val="false"/>
        <w:caps w:val="false"/>
        <w:smallCaps w:val="false"/>
        <w:color w:val="B11414"/>
        <w:spacing w:val="0"/>
      </w:rPr>
      <w:t xml:space="preserve"/>
    </w:r>
  </w:p>
  <w:p>
    <w:pPr>
      <w:pStyle w:val="PreformattedText"/>
      <w:widowControl/>
      <w:shd w:val="clear" w:fill="EEEEEE"/>
      <w:spacing w:before="225" w:after="225"/>
      <w:ind w:left="0" w:right="0" w:hanging="0"/>
      <w:rPr/>
    </w:pPr>
    <w:r>
      <w:rPr>
        <w:rFonts w:ascii="Consolas;Menlo;Deja Vu Sans Mono;Bitstream Vera Sans Mono;monospace" w:hAnsi="Consolas;Menlo;Deja Vu Sans Mono;Bitstream Vera Sans Mono;monospace"/>
        <w:b w:val="false"/>
        <w:i w:val="false"/>
        <w:caps w:val="false"/>
        <w:smallCaps w:val="false"/>
        <w:color w:val="B11414"/>
        <w:spacing w:val="0"/>
        <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
      </w:rPr>
      <w:t xml:space="preserve">    </w:t>
    </w:r>
    <w:r>
      <w:rPr>
        <w:rFonts w:ascii="Consolas;Menlo;Deja Vu Sans Mono;Bitstream Vera Sans Mono;monospace" w:hAnsi="Consolas;Menlo;Deja Vu Sans Mono;Bitstream Vera Sans Mono;monospace"/>
        <w:b w:val="false"/>
        <w:i w:val="false"/>
        <w:caps w:val="false"/>
        <w:smallCaps w:val="false"/>
        <w:color w:val="B11414"/>
        <w:spacing w:val="0"/>
        <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
      </w:rPr>
      <w:t xml:space="preserve"/>
    </w:r>
  </w:p>
  <w:p>
    <w:pPr>
      <w:pStyle w:val="PreformattedText"/>
      <w:widowControl/>
      <w:shd w:val="clear" w:fill="EEEEEE"/>
      <w:spacing w:before="225" w:after="225"/>
      <w:ind w:left="0" w:right="0" w:hanging="0"/>
      <w:rPr/>
    </w:pPr>
    <w:r>
      <w:rPr>
        <w:rFonts w:ascii="Consolas;Menlo;Deja Vu Sans Mono;Bitstream Vera Sans Mono;monospace" w:hAnsi="Consolas;Menlo;Deja Vu Sans Mono;Bitstream Vera Sans Mono;monospace"/>
        <w:b w:val="false"/>
        <w:i w:val="false"/>
        <w:caps w:val="false"/>
        <w:smallCaps w:val="false"/>
        <w:color w:val="B11414"/>
        <w:spacing w:val="0"/>
        <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
      </w:rPr>
      <w:t xml:space="preserve">        </w:t>
    </w:r>
    <w:r>
      <w:rPr>
        <w:rFonts w:ascii="Consolas;Menlo;Deja Vu Sans Mono;Bitstream Vera Sans Mono;monospace" w:hAnsi="Consolas;Menlo;Deja Vu Sans Mono;Bitstream Vera Sans Mono;monospace"/>
        <w:b w:val="false"/>
        <w:i w:val="false"/>
        <w:caps w:val="false"/>
        <w:smallCaps w:val="false"/>
        <w:color w:val="B11414"/>
        <w:spacing w:val="0"/>
        <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
      </w:rPr>
      <w:t xml:space="preserve"/>
    </w:r>
  </w:p>
  <w:p>
    <w:pPr>
      <w:pStyle w:val="Normal"/>
      <w:rPr/>
    </w:pPr>
    <w:r>
      <w:rPr/>
    </w:r>
  </w:p>
  <w:sectPr>
    <w:type w:val="nextPage"/>
    <w:pgSz w:w="11906" w:h="16838"/>
    <w:pgMar w:left="1134" w:right="1134" w:header="0" w:top="1134" w:footer="0" w:bottom="1134" w:gutter="0"/>
    <w:pgNumType w:fmt="decimal"/>
    <w:formProt w:val="false"/>
    <w:textDirection w:val="lrTb"/>
    <w:docGrid w:type="default" w:linePitch="240" w:charSpace="0"/>
  </w:sectPr>
</w:body>
"""

snapshots[
    "test_template_merge_jinja_filters_docx[docx-template-False-False-200] 1"
] = """<w:body xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" xmlns:o="urn:schemas-microsoft-com:office:office" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" xmlns:v="urn:schemas-microsoft-com:vml" xmlns:w10="urn:schemas-microsoft-com:office:word" xmlns:wp="http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing" xmlns:wps="http://schemas.microsoft.com/office/word/2010/wordprocessingShape" xmlns:wpg="http://schemas.microsoft.com/office/word/2010/wordprocessingGroup" xmlns:mc="http://schemas.openxmlformats.org/markup-compatibility/2006" xmlns:wp14="http://schemas.microsoft.com/office/word/2010/wordprocessingDrawing" xmlns:w14="http://schemas.microsoft.com/office/word/2010/wordml">
  <w:p>
    <w:pPr>
      <w:pStyle w:val="Normal"/>
      <w:rPr/>
    </w:pPr>
    <w:r>
      <w:rPr>
        <w:rFonts w:ascii="DejaVu Sans" w:hAnsi="DejaVu Sans"/>
      </w:rPr>
      <w:t xml:space="preserve">15.09.1984</w:t>
    </w:r>
  </w:p>
  <w:p>
    <w:pPr>
      <w:pStyle w:val="Normal"/>
      <w:rPr/>
    </w:pPr>
    <w:r>
      <w:rPr>
        <w:rFonts w:ascii="DejaVu Sans" w:hAnsi="DejaVu Sans"/>
      </w:rPr>
      <w:t xml:space="preserve">1984</w:t>
    </w:r>
  </w:p>
  <w:p>
    <w:pPr>
      <w:pStyle w:val="Normal"/>
      <w:rPr/>
    </w:pPr>
    <w:r>
      <w:rPr>
        <w:rFonts w:ascii="DejaVu Sans" w:hAnsi="DejaVu Sans"/>
      </w:rPr>
      <w:t xml:space="preserve">23:24</w:t>
    </w:r>
  </w:p>
  <w:p>
    <w:pPr>
      <w:pStyle w:val="Normal"/>
      <w:rPr/>
    </w:pPr>
    <w:r>
      <w:rPr>
        <w:rFonts w:ascii="DejaVu Sans" w:hAnsi="DejaVu Sans"/>
      </w:rPr>
      <w:t xml:space="preserve">15.09.1984, 23:23:00</w:t>
    </w:r>
  </w:p>
  <w:p>
    <w:pPr>
      <w:pStyle w:val="Normal"/>
      <w:rPr/>
    </w:pPr>
    <w:r>
      <w:rPr>
        <w:rFonts w:ascii="DejaVu Sans" w:hAnsi="DejaVu Sans"/>
      </w:rPr>
      <w:t xml:space="preserve">23:23</w:t>
    </w:r>
  </w:p>
  <w:p>
    <w:pPr>
      <w:pStyle w:val="Normal"/>
      <w:rPr/>
    </w:pPr>
    <w:r>
      <w:rPr>
        <w:rFonts w:ascii="DejaVu Sans" w:hAnsi="DejaVu Sans"/>
      </w:rPr>
      <w:t xml:space="preserve"/>
    </w:r>
  </w:p>
  <w:p>
    <w:pPr>
      <w:pStyle w:val="Normal"/>
      <w:rPr/>
    </w:pPr>
    <w:r>
      <w:rPr>
        <w:rFonts w:ascii="DejaVu Sans" w:hAnsi="DejaVu Sans"/>
      </w:rPr>
      <w:t xml:space="preserve"/>
    </w:r>
  </w:p>
  <w:p>
    <w:pPr>
      <w:pStyle w:val="Normal"/>
      <w:rPr/>
    </w:pPr>
    <w:r>
      <w:rPr>
        <w:rFonts w:ascii="DejaVu Sans" w:hAnsi="DejaVu Sans"/>
      </w:rPr>
      <w:t xml:space="preserve">something</w:t>
    </w:r>
  </w:p>
  <w:p>
    <w:pPr>
      <w:pStyle w:val="Normal"/>
      <w:rPr/>
    </w:pPr>
    <w:r>
      <w:rPr>
        <w:rFonts w:ascii="DejaVu Sans" w:hAnsi="DejaVu Sans"/>
      </w:rPr>
      <w:t xml:space="preserve">This is</w:t>
      <w:br/>
      <w:t xml:space="preserve">a test.</w:t>
    </w:r>
  </w:p>
  <w:p>
    <w:pPr>
      <w:pStyle w:val="Normal"/>
      <w:rPr/>
    </w:pPr>
    <w:r>
      <w:rPr>
        <w:rFonts w:ascii="DejaVu Sans" w:hAnsi="DejaVu Sans"/>
      </w:rPr>
      <w:t xml:space="preserve"/>
    </w:r>
    <w:r>
      <w:drawing>
        <wp:inline xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" xmlns:pic="http://schemas.openxmlformats.org/drawingml/2006/picture">
          <wp:extent cx="1800000" cy="1800000"/>
          <wp:docPr id="1001" name="Picture 1"/>
          <wp:cNvGraphicFramePr>
            <a:graphicFrameLocks noChangeAspect="1"/>
          </wp:cNvGraphicFramePr>
          <a:graphic>
            <a:graphicData uri="http://schemas.openxmlformats.org/drawingml/2006/picture">
              <pic:pic>
                <pic:nvPicPr>
                  <pic:cNvPr id="0" name="image.png"/>
                  <pic:cNvPicPr/>
                </pic:nvPicPr>
                <pic:blipFill>
                  <a:blip r:embed="rId5"/>
                  <a:stretch>
                    <a:fillRect/>
                  </a:stretch>
                </pic:blipFill>
                <pic:spPr>
                  <a:xfrm>
                    <a:off x="0" y="0"/>
                    <a:ext cx="1800000" cy="1800000"/>
                  </a:xfrm>
                  <a:prstGeom prst="rect"/>
                </pic:spPr>
              </pic:pic>
            </a:graphicData>
          </a:graphic>
        </wp:inline>
      </w:drawing>
    </w:r>
    <w:r>
      <w:t xml:space="preserve"/>
    </w:r>
  </w:p>
  <w:p>
    <w:pPr>
      <w:pStyle w:val="Normal"/>
      <w:rPr>
        <w:rFonts w:ascii="DejaVu Sans" w:hAnsi="DejaVu Sans"/>
      </w:rPr>
    </w:pPr>
    <w:r>
      <w:rPr/>
    </w:r>
  </w:p>
  <w:sectPr>
    <w:type w:val="nextPage"/>
    <w:pgSz w:w="11906" w:h="16838"/>
    <w:pgMar w:left="1134" w:right="1134" w:header="0" w:top="1134" w:footer="0" w:bottom="1134" w:gutter="0"/>
    <w:pgNumType w:fmt="decimal"/>
    <w:formProt w:val="false"/>
    <w:textDirection w:val="lrTb"/>
    <w:docGrid w:type="default" w:linePitch="240" w:charSpace="0"/>
  </w:sectPr>
</w:body>
"""
