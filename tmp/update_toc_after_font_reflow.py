import re
from pathlib import Path

from docx import Document
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from pypdf import PdfReader


ROOT = Path("/Users/fanfan/Documents/GitHub/MSE806-ITS")
DOCX = ROOT / "Assessment/MSE806_Assessment1_Report_Template_Final.docx"
PDF = Path("/private/tmp/mse806_font_rules_qa2/MSE806_Assessment1_Report_Template_Final.pdf")


def normalise(text):
    return re.sub(r"[^a-z0-9]+", " ", text.lower()).strip()


def ensure_run_font(run):
    rpr = run.find(qn("w:rPr"))
    if rpr is None:
        rpr = OxmlElement("w:rPr")
        run.insert(0, rpr)
    rfonts = rpr.find(qn("w:rFonts"))
    if rfonts is None:
        rfonts = OxmlElement("w:rFonts")
        rpr.insert(0, rfonts)
    for key in ("ascii", "hAnsi", "eastAsia", "cs"):
        rfonts.set(qn(f"w:{key}"), "Times New Roman")
    for name in ("sz", "szCs"):
        element = rpr.find(qn(f"w:{name}"))
        if element is None:
            element = OxmlElement(f"w:{name}")
            rpr.append(element)
        element.set(qn("w:val"), "24")


def main():
    doc = Document(DOCX)
    pdf_pages = [normalise(page.extract_text() or "") for page in PdfReader(PDF).pages]
    updated = 0

    for paragraph in doc.paragraphs:
        if not paragraph.style.name.startswith("toc "):
            continue
        title = paragraph.text.rsplit("\t", 1)[0]
        needle = normalise(title)
        hits = [index + 1 for index, text in enumerate(pdf_pages) if needle in text]
        content_hits = [page for page in hits if page > 2]
        if not content_hits:
            raise RuntimeError(f"Could not locate TOC heading in rendered PDF: {title}")

        hyperlinks = paragraph._p.xpath(".//w:hyperlink")
        if not hyperlinks:
            raise RuntimeError(f"TOC entry has no hyperlink: {title}")
        text_nodes = hyperlinks[0].xpath(".//w:t")
        if len(text_nodes) < 2:
            raise RuntimeError(f"TOC entry has no cached page number: {title}")
        text_nodes[-1].text = str(content_hits[0])

        for run in hyperlinks[0].xpath(".//w:r"):
            ensure_run_font(run)
        updated += 1

    doc.save(DOCX)
    print(f"Updated {updated} TOC entries from the 30-page rendered layout")


if __name__ == "__main__":
    main()
