from pathlib import Path

from docx import Document
from docx.oxml.ns import qn
from docx.shared import Inches, Pt


SOURCE = Path("Assessment/2604MSE803_Assessment1_Report_Draft_v3.docx")
OUTPUT = Path("Assessment/2604MSE803_Assessment1_Report_Draft_v4.docx")

FONT_NAME = "Times New Roman"
BODY_SIZE = Pt(12)
HEADING_SIZE = Pt(14)
HEADING_STYLES = {"Title", "TOC Heading", "Heading 1", "Heading 2", "Heading 3"}


def set_run_font(run, size):
    run.font.name = FONT_NAME
    run.font.size = size
    rpr = run._element.get_or_add_rPr()
    rfonts = rpr.get_or_add_rFonts()
    for key in ("ascii", "hAnsi", "eastAsia", "cs"):
        rfonts.set(qn(f"w:{key}"), FONT_NAME)


def format_paragraph(paragraph):
    size = HEADING_SIZE if paragraph.style.name in HEADING_STYLES else BODY_SIZE
    paragraph.paragraph_format.line_spacing = 1.0
    for run in paragraph.runs:
        set_run_font(run, size)


doc = Document(SOURCE)

for style in doc.styles:
    if not hasattr(style, "font"):
        continue
    style.font.name = FONT_NAME
    style.font.size = HEADING_SIZE if style.name in HEADING_STYLES else BODY_SIZE
    if style.element.rPr is not None:
        rfonts = style.element.rPr.get_or_add_rFonts()
        for key in ("ascii", "hAnsi", "eastAsia", "cs"):
            rfonts.set(qn(f"w:{key}"), FONT_NAME)
    if hasattr(style, "paragraph_format"):
        style.paragraph_format.line_spacing = 1.0

for paragraph in doc.paragraphs:
    format_paragraph(paragraph)

for table in doc.tables:
    for row in table.rows:
        for cell in row.cells:
            for paragraph in cell.paragraphs:
                format_paragraph(paragraph)

# APA 7 reference entries: single spaced per the supplied report requirement,
# with a 0.5-inch hanging indent and no extra paragraph spacing.
in_references = False
for paragraph in doc.paragraphs:
    text = paragraph.text.strip()
    if text == "References":
        in_references = True
        continue
    if in_references and paragraph.style.name == "Heading 1":
        break
    if in_references and text:
        paragraph.paragraph_format.left_indent = Inches(0.5)
        paragraph.paragraph_format.first_line_indent = Inches(-0.5)
        paragraph.paragraph_format.space_after = Pt(0)

doc.save(OUTPUT)
print(OUTPUT)
