from pathlib import Path

from docx import Document
from docx.enum.style import WD_STYLE_TYPE
from docx.oxml.ns import qn
from docx.shared import Pt


DOCX = Path(
    "/Users/fanfan/Documents/GitHub/MSE806-ITS/Assessment/"
    "MSE806_Assessment1_Report_Template_Final.docx"
)
FONT = "Times New Roman"
BODY_SIZE = Pt(12)
HEADING_SIZE = Pt(14)


def set_font(font, size):
    font.name = FONT
    font.size = size
    element = font._element
    rpr = element.get_or_add_rPr() if hasattr(element, "get_or_add_rPr") else element
    rfonts = rpr.rFonts
    if rfonts is None:
        rfonts = rpr._add_rFonts()
    for key in ("ascii", "hAnsi", "eastAsia", "cs"):
        rfonts.set(qn(f"w:{key}"), FONT)


def is_heading_style(style_name):
    return style_name == "Title" or style_name == "TOC Heading" or style_name.startswith("Heading ")


def format_paragraph(paragraph):
    size = HEADING_SIZE if is_heading_style(paragraph.style.name) else BODY_SIZE
    for run in paragraph.runs:
        set_font(run.font, size)


def main():
    doc = Document(DOCX)

    for style in doc.styles:
        if style.type in (WD_STYLE_TYPE.PARAGRAPH, WD_STYLE_TYPE.CHARACTER):
            size = HEADING_SIZE if is_heading_style(style.name) else BODY_SIZE
            set_font(style.font, size)

    for paragraph in doc.paragraphs:
        format_paragraph(paragraph)

    for table in doc.tables:
        for row in table.rows:
            for cell in row.cells:
                for paragraph in cell.paragraphs:
                    format_paragraph(paragraph)

    for section in doc.sections:
        for paragraph in section.header.paragraphs:
            format_paragraph(paragraph)
        for paragraph in section.footer.paragraphs:
            format_paragraph(paragraph)

    doc.save(DOCX)
    print(f"Applied {FONT} 12 pt body and 14 pt headings to {DOCX}")


if __name__ == "__main__":
    main()
