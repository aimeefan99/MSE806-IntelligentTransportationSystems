from pathlib import Path

from docx import Document


DOCX = Path(
    "/Users/fanfan/Documents/GitHub/MSE806-ITS/Assessment/"
    "MSE806_Assessment1_Report_Template_Final.docx"
)

REPLACEMENTS = {
    "Figure 4 should map the 4,335 stops actually referenced by Dublin Bus trips together with their route shapes.":
        "Figure 4 maps the 4,335 stops actually referenced by Dublin Bus trips together with their route shapes.",
    "Figure 5 should present the complete hourly distributions rather than only these peaks":
        "Figure 5 presents the complete hourly distributions rather than only these peaks",
    "Figure 6 should therefore plot distance, duration and service volume together.":
        "Figure 6 therefore plots distance, duration and service volume together.",
    "World Bank Group (2011)": "World Bank (2011)",
    "Avci and Koca (2024)": "Avcı and Koca (2024)",
    "(TFI, 2026)": "(Transport for Ireland, n.d.)",
}


def replace_in_paragraph(paragraph):
    original = paragraph.text
    updated = original
    for old, new in REPLACEMENTS.items():
        updated = updated.replace(old, new)
    if updated == original:
        return False

    # All target paragraphs are single-format body text or italic figure notes.
    italic = all(run.italic for run in paragraph.runs if run.text)
    for run in paragraph.runs:
        run.text = ""
    run = paragraph.runs[0] if paragraph.runs else paragraph.add_run()
    run.text = updated
    if italic:
        run.italic = True
    return True


def main():
    doc = Document(DOCX)
    changed = sum(replace_in_paragraph(paragraph) for paragraph in doc.paragraphs)
    if changed != 10:
        raise RuntimeError(f"Expected 10 updated paragraphs, found {changed}")
    doc.save(DOCX)
    print(f"Updated {changed} paragraphs in {DOCX}")


if __name__ == "__main__":
    main()
