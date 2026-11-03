from pathlib import Path

from docx import Document
from docx.oxml import OxmlElement
from docx.oxml.ns import qn


DOCX = Path(
    "/Users/fanfan/Documents/GitHub/MSE806-ITS/Assessment/"
    "MSE806_Assessment1_Report_Template_Final.docx"
)


def main():
    doc = Document(DOCX)

    # The TOC now fits on one page. Remove the redundant manual break in the
    # empty paragraph immediately before Section 1 so it does not create a
    # completely blank page.
    intro_index = next(
        i
        for i, paragraph in enumerate(doc.paragraphs)
        if paragraph.text.strip() == "1 Introduction to ITS and Dublin Bus"
    )
    preceding = doc.paragraphs[intro_index - 1]
    for br in list(preceding._p.xpath(".//w:br")):
        if br.get(qn("w:type")) == "page":
            br.getparent().remove(br)

    # Twelve-point table text needs more vertical space. Keep every logical
    # row intact so no record is split across two pages.
    for table in doc.tables:
        for row in table.rows:
            tr_pr = row._tr.get_or_add_trPr()
            if tr_pr.find(qn("w:cantSplit")) is None:
                tr_pr.append(OxmlElement("w:cantSplit"))

    doc.save(DOCX)
    print("Removed redundant page break and prevented table rows from splitting")


if __name__ == "__main__":
    main()
