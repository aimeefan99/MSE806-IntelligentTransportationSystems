from pathlib import Path

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Inches, Pt


SOURCE = Path("Assessment/2604MSE803_Assessment1_Report_Draft_v4.docx")
OUTPUT = Path("Assessment/2604MSE803_Assessment1_Report_Draft_v5.docx")

doc = Document(SOURCE)
in_references = False
for paragraph in doc.paragraphs:
    text = paragraph.text.strip()
    if text == "References":
        in_references = True
        continue
    if in_references and paragraph.style.name == "Heading 1":
        break
    if in_references and text:
        paragraph.alignment = WD_ALIGN_PARAGRAPH.LEFT
        paragraph.paragraph_format.left_indent = Inches(0.5)
        paragraph.paragraph_format.first_line_indent = Inches(-0.5)
        paragraph.paragraph_format.line_spacing = 1.0
        paragraph.paragraph_format.space_after = Pt(0)

doc.save(OUTPUT)
print(OUTPUT)
